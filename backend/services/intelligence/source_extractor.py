"""SourceExtractor — graph-cross-referenced + auto-ingesting source extraction.

When a source is real (high LLM confidence) but missing from Memgraph, it gets
automatically ingested into the graph so the knowledge base grows organically.

Pipeline:
1. LLM generates candidate sources for a scene
2. Each candidate is cross-referenced against Memgraph's paper/concept nodes
3. Sources FOUND in the graph → graph_verified=True, confidence='high'
4. Sources NOT in the graph but with high LLM confidence →
   - Auto-ingested into Memgraph as PaperNode + Concept relationships
   - Marked graph_verified=True (the graph now contains them)
5. Sources with low LLM confidence + not in graph → flagged for human review
"""
from typing import List, Optional
from schemas.episode_outline import SceneOutlineItem
from schemas.source import AcademicSource, SourcesPackage, PaperNode, ConceptNode
from services.intelligence.qwen_client import QwenClient, QWEN_MAX
from services.ingestion.memgraph_client import MemgraphClient
from core.logging import get_logger

logger = get_logger("source_extractor")

SOURCE_EXTRACTOR_PROMPT = """
You are a financial economics research librarian. Your task is to find real, verifiable academic 
sources for a specific scene in a Quantifaya episode.

CRITICAL RULES:
1. Return ONLY real, verifiable academic works. If you are not certain a work exists with 
   this exact author, year, and title, omit it. Do not invent sources.
2. Each source must have a plausible author, year, title, and journal.
3. Return valid JSON only. No markdown fences. No preamble.
"""


class SourceExtractor:
    def __init__(self, qwen: QwenClient, memgraph: Optional[MemgraphClient] = None):
        self.qwen = qwen
        self.memgraph = memgraph

    async def extract(self, scene: SceneOutlineItem, episode_topic: str) -> List[AcademicSource]:
        messages = [
            {"role": "system", "content": SOURCE_EXTRACTOR_PROMPT},
            {"role": "user", "content": (
                f"Episode topic: {episode_topic}\n"
                f"Scene {scene.scene_number}: {scene.title}\n"
                f"Key sources needed: {scene.key_sources}\n"
                f"Voiceover hint: {scene.voiceover_hint}\n\n"
                "Return a JSON object with a 'sources' array. Each source has:\n"
                "- ref_number: int\n"
                "- authors: str\n"
                "- year: int\n"
                "- title: str\n"
                "- journal_or_publisher: str\n"
                "- doi_or_url: str (optional)\n"
                "- scene_usage_note: str\n"
                "- confidence: str ('high' or 'low')\n\n"
                "Return at least 2 and at most 4 sources per scene."
            )},
        ]

        try:
            data = await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.3)
            raw_sources = [AcademicSource(**s) for s in data.get("sources", [])]

            # Cross-reference against Memgraph + auto-ingest missing real sources
            verified_sources = await self._cross_reference_and_ingest(raw_sources, episode_topic, scene)

            # Run self-review for consistency
            sources = await self._self_review(verified_sources, episode_topic, scene)
            return sources
        except Exception as e:
            logger.warning("source_extraction_failed", scene=scene.scene_number, error=str(e))
            return []

    async def _cross_reference_and_ingest(
        self, sources: List[AcademicSource], topic: str, scene: SceneOutlineItem
    ) -> List[AcademicSource]:
        """Cross-reference each source against Memgraph.

        If a source has high LLM confidence but is not in the graph,
        auto-ingest it so the knowledge base grows. This means the graph
        becomes more complete with every episode generated.
        """
        if not self.memgraph or not self.memgraph.enabled:
            # No graph available — trust LLM confidence, no verification mark
            for s in sources:
                s.graph_verified = False
            logger.info(
                "source_extraction_no_graph",
                scene=scene.scene_number,
                source_count=len(sources),
            )
            return sources

        verified_count = 0
        ingested_count = 0

        for source in sources:
            try:
                # Retrieve graph context for the scene topic to check for this paper
                result = await self.memgraph.graphrag_retrieve(
                    topic=topic,
                    scene_title=scene.title,
                )

                found_in_graph = False
                if result and result.has_content():
                    if result.has_paper(source.authors, source.year, source.title):
                        found_in_graph = True

                if found_in_graph:
                    # Source is verified by the knowledge graph
                    source.graph_verified = True
                    source.confidence = "high"
                    verified_count += 1
                    logger.info(
                        "source_found_in_graph",
                        ref=source.ref_number,
                        authors=source.authors,
                        year=source.year,
                    )

                elif source.confidence == "high":
                    # Source is NOT in the graph but LLM says it's real → auto-ingest
                    await self._ingest_source_into_graph(source, topic, scene)
                    source.graph_verified = True
                    source.confidence = "high"
                    ingested_count += 1
                    logger.info(
                        "source_auto_ingested",
                        ref=source.ref_number,
                        authors=source.authors,
                        year=source.year,
                    )

                else:
                    # Source not in graph AND low LLM confidence → flag for review
                    source.graph_verified = False
                    source.confidence = "low"
                    logger.warning(
                        "source_unreviewed",
                        ref=source.ref_number,
                        authors=source.authors,
                        year=source.year,
                        reason="low_confidence_and_not_in_graph",
                    )

            except Exception as e:
                logger.warning(
                    "source_crossref_failed",
                    ref=source.ref_number,
                    error=str(e),
                )
                source.graph_verified = False
                source.confidence = "low"

        logger.info(
            "source_cross_reference_complete",
            scene=scene.scene_number,
            total=len(sources),
            verified=verified_count,
            ingested=ingested_count,
        )
        return sources

    async def _ingest_source_into_graph(
        self, source: AcademicSource, topic: str, scene: SceneOutlineItem
    ) -> None:
        """Ingest a real source into Memgraph so future episodes find it.

        Creates:
        - A :Paper node with the source's metadata
        - Relationships from the paper to relevant :Concept nodes
          extracted from the scene's key_equations and title
        """
        if not self.memgraph or not self.memgraph.enabled:
            return

        try:
            # Extract candidate concept names from the scene context
            concept_names = set()
            concept_names.add(topic.lower().replace(" ", "_"))

            # Add concepts from key equations
            for eq in scene.key_equations:
                # Extract a short concept name from LaTeX (clean the string)
                clean = eq.replace("\\", "").replace("{", "").replace("}", "")
                clean = clean.replace("^", "").replace("_", "")
                # Take first meaningful word as potential concept
                words = clean.split()
                if words:
                    concept_names.add(words[0].lower())

            # Add concepts from scene title
            for word in scene.title.lower().split():
                if len(word) > 3:
                    concept_names.add(word)

            # Ingest into Memgraph via Cypher
            # Create the Paper node if it doesn't exist
            create_paper_query = """
            MERGE (p:Paper {
                title: $title,
                authors: $authors,
                year: $year
            })
            ON CREATE SET
                p.doi = $doi,
                p.journal = $journal,
                p.abstract = $abstract,
                p.concept_count = 0,
                p.ingested_from_episode = true
            RETURN p
            """
            params = {
                "title": source.title,
                "authors": source.authors,
                "year": source.year,
                "doi": source.doi_or_url or "",
                "journal": source.journal_or_publisher,
                "abstract": f"Source for scene '{scene.title}' on topic '{topic}'. Usage: {source.scene_usage_note}",
            }

            await self.memgraph.execute_query(create_paper_query, params)

            # Link paper to relevant concepts via BELONGS_TO relationships
            for concept_name in list(concept_names)[:5]:  # limit to 5 concepts
                link_query = """
                MATCH (c:Concept {name: $concept_name})
                MATCH (p:Paper {title: $title, authors: $authors, year: $year})
                MERGE (p)-[:BELONGS_TO]->(c)
                SET p.concept_count = p.concept_count + 1
                """
                try:
                    await self.memgraph.execute_query(link_query, {
                        "concept_name": concept_name,
                        "title": source.title,
                        "authors": source.authors,
                        "year": source.year,
                    })
                except Exception:
                    # Concept may not exist in graph yet — that's okay
                    pass

            logger.info(
                "source_ingested_into_graph",
                title=source.title[:60],
                authors=source.authors,
                concepts=list(concept_names)[:5],
            )

        except Exception as e:
            logger.warning(
                "source_ingest_failed",
                title=source.title[:60],
                error=str(e),
            )

    async def _self_review(self, sources: List[AcademicSource], topic: str, scene: SceneOutlineItem) -> List[AcademicSource]:
        """Run a self-review Qwen call to check source consistency."""
        review_messages = [
            {"role": "system", "content": "Check each academic source for internal consistency. "
                                          "Author + year + title + journal must all be plausible together. "
                                          "Flag inconsistent sources with confidence: 'low'. Return JSON with sources array."},
            {"role": "user", "content": (
                f"Review these sources for scene '{scene.title}' on topic '{topic}':\n"
                + "\n".join(f"[{s.ref_number}] {s.authors} ({s.year}) '{s.title}' - {s.journal_or_publisher}"
                           for s in sources)
            )},
        ]
        try:
            data = await self.qwen.complete_json(QWEN_MAX, review_messages, temperature=0.2)
            reviewed = data.get("sources", [])
            if reviewed:
                return [AcademicSource(**s) if isinstance(s, dict) else s for s in reviewed]
        except Exception as e:
            logger.warning("source_self_review_failed", error=str(e))

        return sources