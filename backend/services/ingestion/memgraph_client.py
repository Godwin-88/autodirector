"""
Memgraph GraphRAG Client — Production implementation (Phase N).

Queries the actual Memgraph quant finance knowledge graph with schema:
  - 7 node labels: Concept, Formula, Category, QuizQuestion, Strategy, Ticker, Regime
  - 16 relationship types: BELONGS_TO, HAS_FORMULA, PREREQ_OF, DERIVED_FROM, etc.
  - Concept properties: name, definition, category, difficulty, menu_context (optional)
  - Formula properties: id, name, latex, expression, params (list), output
  - No Paper nodes exist — citation retrieval is not possible from Memgraph alone

Memgraph is Neo4j-compatible (uses Bolt protocol).
All queries have 5-second timeouts. Degrades gracefully when MEMGRAPH_ENABLED=false.
"""

import asyncio
import logging
from typing import List, Optional

from core.config import get_settings
from schemas.source import GraphRAGResult, ConceptNode

logger = logging.getLogger(__name__)


class MemgraphClient:
    """
    Production Memgraph/Neo4j client for quant finance knowledge graph.
    Connection configured via MEMGRAPH_URI, MEMGRAPH_USER, MEMGRAPH_PASSWORD env vars.
    All methods return empty results when MEMGRAPH_ENABLED=false.
    """

    def __init__(self):
        self.settings = get_settings()
        self.enabled = getattr(self.settings, "memgraph_enabled", False)
        self._driver = None

    async def connect(self):
        """Initialize the Neo4j/Memgraph driver. Called once in FastAPI lifespan."""
        if not self.enabled:
            logger.info("Memgraph is disabled — skipping connection")
            return
        try:
            from neo4j import AsyncGraphDatabase

            uri = getattr(self.settings, "memgraph_uri", "bolt://localhost:7687")
            user = getattr(self.settings, "memgraph_user", "")
            password = getattr(self.settings, "memgraph_password", "")

            if user and password:
                self._driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
            else:
                self._driver = AsyncGraphDatabase.driver(uri)

            await self._driver.verify_connectivity()
            logger.info("Connected to Memgraph at %s", uri)
        except ImportError:
            logger.warning("neo4j driver not installed, Memgraph unavailable")
            self.enabled = False
        except Exception as e:
            logger.warning("Failed to connect to Memgraph: %s", e)
            self.enabled = False

    async def close(self):
        """Close the driver connection. Called once in FastAPI shutdown."""
        if self._driver:
            await self._driver.close()
            self._driver = None
            logger.info("Memgraph connection closed")

    async def _get_driver(self):
        """Lazy accessor for the driver. Returns None if disabled or not connected."""
        if not self.enabled or self._driver is None:
            return None
        return self._driver

    # ── CONCEPT RETRIEVAL ────────────────────────────────────────────

    async def find_concepts(self, query: str, limit: int = 10) -> List[ConceptNode]:
        """
        Search concepts by name or definition using CONTAINS (no fulltext index available).
        Falls back from exact name match to partial CONTAINS.
        """
        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                # Try CONTAINS on name first (uses label+property index on category, not name)
                result = await session.run(
                    """
                    MATCH (c:Concept)
                    WHERE toLower(c.name) CONTAINS toLower($query)
                       OR toLower(c.definition) CONTAINS toLower($query)
                    RETURN c.name AS name, c.definition AS definition,
                           c.category AS category, c.difficulty AS difficulty
                    LIMIT $limit
                    """,
                    query=query,
                    limit=limit,
                    timeout=5,
                )
                records = await result.data()
                return [
                    ConceptNode(
                        name=r.get("name", ""),
                        definition=r.get("definition"),
                        category=r.get("category"),
                        difficulty=r.get("difficulty"),
                        score=1.0,
                    )
                    for r in records
                ]
        except Exception as e:
            logger.warning("Memgraph find_concepts failed for '%s': %s", query, e)
            return []

    async def get_concept_detail(self, concept_name: str) -> dict:
        """
        Full detail for a single concept: definition, category, formulas, related concepts,
        prerequisites, strategies that use it, and regimes it activates.
        """
        driver = await self._get_driver()
        if not driver:
            return {}

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (c:Concept {name: $name})
                    OPTIONAL MATCH (c)-[:HAS_FORMULA]->(f:Formula)
                    OPTIONAL MATCH (c)-[:BELONGS_TO]->(cat:Category)
                    OPTIONAL MATCH (c)-[:PREREQ_OF]->(next:Concept)
                    OPTIONAL MATCH (prereq:Concept)-[:PREREQ_OF]->(c)
                    OPTIONAL MATCH (c)<-[:DERIVED_FROM]-(s:Strategy)
                    OPTIONAL MATCH (c)-[:ACTIVATED_BY]->(reg:Regime)
                    RETURN c.name AS name,
                           c.definition AS definition,
                           c.category AS category,
                           c.difficulty AS difficulty,
                           cat.name AS category_name,
                           cat.display AS category_display,
                           collect(DISTINCT {
                               id: f.id,
                               name: f.name,
                               latex: f.latex,
                               expression: f.expression,
                               params: f.params,
                               output: f.output
                           }) AS formulas,
                           collect(DISTINCT next.name) AS teaches,
                           collect(DISTINCT prereq.name) AS prerequisites,
                           collect(DISTINCT {
                               name: s.name,
                               description: s.description,
                               status: s.status
                           }) AS strategies,
                           collect(DISTINCT reg.name) AS regimes
                    """,
                    name=concept_name,
                    timeout=5,
                )
                record = await result.single()
                return dict(record) if record else {}
        except Exception as e:
            logger.warning("Memgraph get_concept_detail failed for '%s': %s", concept_name, e)
            return {}

    # ── FORMULA (EQUATION) RETRIEVAL ─────────────────────────────────

    async def get_concept_formulas(self, concept_name: str) -> List[dict]:
        """
        Get verified LaTeX formulas for a concept via :HAS_FORMULA relationship.
        Formula nodes have: id, name, latex, expression, params (list), output.
        """
        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (c:Concept {name: $concept})-[:HAS_FORMULA]->(f:Formula)
                    RETURN f.id AS id, f.name AS name, f.latex AS latex,
                           f.expression AS expression, f.params AS params,
                           f.output AS output
                    ORDER BY f.name
                    """,
                    concept=concept_name,
                    timeout=5,
                )
                records = await result.data()
                return [
                    {
                        "id": r.get("id"),
                        "name": r.get("name"),
                        "latex": r.get("latex"),
                        "expression": r.get("expression"),
                        "params": r.get("params", []),
                        "output": r.get("output"),
                    }
                    for r in records
                ]
        except Exception as e:
            logger.warning("Memgraph get_concept_formulas failed for '%s': %s", concept_name, e)
            return []

    async def get_verified_equations(self, concept_names: List[str]) -> List[dict]:
        """
        Get all verified LaTeX formulas for a list of concept names.
        Used by the script generator to inject graph-verified equations.
        """
        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (c:Concept)-[:HAS_FORMULA]->(f:Formula)
                    WHERE c.name IN $concepts
                    RETURN f.id AS id, f.name AS name,
                           f.latex AS latex, f.expression AS expression,
                           c.name AS concept_name
                    ORDER BY c.name, f.name
                    """,
                    concepts=concept_names,
                    timeout=5,
                )
                records = await result.data()
                return [
                    {
                        "id": r.get("id"),
                        "name": r.get("name"),
                        "latex": r.get("latex"),
                        "expression": r.get("expression"),
                        "concept_name": r.get("concept_name"),
                    }
                    for r in records
                ]
        except Exception as e:
            logger.warning("Memgraph get_verified_equations failed: %s", e)
            return []

    # ── PREREQUISITE CHAIN ──────────────────────────────────────────

    async def get_prerequisite_chain(self, concept_name: str) -> List[str]:
        """
        Returns ordered list of concepts this one REQUIRES (inward PREREQ_OF).
        Used to build the 'Previously on Quantifaya' recap scene.
        """
        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH path = (prereq:Concept)-[:PREREQ_OF*1..5]->(c:Concept {name: $name})
                    WITH prereq, length(path) AS dist
                    RETURN prereq.name AS name, dist
                    ORDER BY dist ASC
                    """,
                    name=concept_name,
                    timeout=5,
                )
                records = await result.data()
                return [r["name"] for r in records]
        except Exception as e:
            logger.warning("Memgraph get_prerequisite_chain failed for '%s': %s", concept_name, e)
            return []

    async def get_teaches_chain(self, concept_name: str) -> List[str]:
        """
        Returns ordered list of concepts this one TEACHES (outward PREREQ_OF).
        Used for 'Next episode' suggestions.
        """
        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH path = (c:Concept {name: $name})-[:PREREQ_OF*1..5]->(next:Concept)
                    WITH next, length(path) AS dist
                    RETURN next.name AS name, dist
                    ORDER BY dist ASC
                    """,
                    name=concept_name,
                    timeout=5,
                )
                records = await result.data()
                return [r["name"] for r in records]
        except Exception as e:
            logger.warning("Memgraph get_teaches_chain failed for '%s': %s", concept_name, e)
            return []

    # ── SUBGRAPH RETRIEVAL ───────────────────────────────────────────

    async def get_concept_subgraph(self, concept_name: str, depth: int = 2) -> dict:
        """
        Get the local subgraph around a concept (Concept nodes only, depth-limited).
        Returns nodes and edges for interactive graph visualisation in the frontend.
        Capped at 50 nodes for UI performance.
        """
        driver = await self._get_driver()
        if not driver:
            return {"nodes": [], "edges": []}

        try:
            async with driver.session() as session:
                # Get all reachable Concept nodes within depth
                result = await session.run(
                    f"""
                    MATCH path = (c:Concept {{name: $name}})-[*1..{depth}]-(related:Concept)
                    UNWIND nodes(path) AS n
                    RETURN DISTINCT n.name AS name, n.definition AS definition,
                           n.category AS category, n.difficulty AS difficulty
                    LIMIT 50
                    """,
                    name=concept_name,
                    timeout=5,
                )
                node_records = await result.data()

                nodes = {}
                for r in node_records:
                    name = r.get("name")
                    if name and name not in nodes:
                        nodes[name] = {
                            "id": name,
                            "name": name,
                            "label": "Concept",
                            "definition": r.get("definition"),
                            "category": r.get("category"),
                            "difficulty": r.get("difficulty"),
                        }

                # Get edges between these nodes
                node_names = list(nodes.keys())
                if len(node_names) < 2:
                    return {"nodes": list(nodes.values()), "edges": []}

                result2 = await session.run(
                    """
                    MATCH (a:Concept)-[r]-(b:Concept)
                    WHERE a.name IN $names AND b.name IN $names
                    RETURN DISTINCT a.name AS source, type(r) AS type, b.name AS target
                    """,
                    names=node_names,
                    timeout=5,
                )
                edge_records = await result2.data()
                edges = [
                    {
                        "source": r.get("source"),
                        "type": r.get("type"),
                        "target": r.get("target"),
                    }
                    for r in edge_records
                ]

                return {"nodes": list(nodes.values()), "edges": edges}
        except Exception as e:
            logger.warning("Memgraph get_concept_subgraph failed for '%s': %s", concept_name, e)
            return {"nodes": [], "edges": []}

    # ── STRATEGY RETRIEVAL ──────────────────────────────────────────

    async def get_strategies_for_concept(self, concept_name: str) -> List[dict]:
        """
        Get trading strategies derived from a concept (via :DERIVED_FROM relationship).
        """
        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (c:Concept {name: $name})<-[:DERIVED_FROM]-(s:Strategy)
                    RETURN s.name AS name, s.description AS description,
                           s.status AS status, s.formula_ref AS formula_ref,
                           s.sizing_formula_ref AS sizing_formula_ref,
                           s.risk_weight AS risk_weight
                    """,
                    name=concept_name,
                    timeout=5,
                )
                records = await result.data()
                return [
                    {
                        "name": r.get("name"),
                        "description": r.get("description"),
                        "status": r.get("status"),
                        "formula_ref": r.get("formula_ref"),
                        "sizing_formula_ref": r.get("sizing_formula_ref"),
                        "risk_weight": r.get("risk_weight"),
                        "params": {k: v for k, v in r.items() if k.startswith("param_")},
                    }
                    for r in records
                ]
        except Exception as e:
            logger.warning("Memgraph get_strategies_for_concept failed for '%s': %s", concept_name, e)
            return []

    # ── REGIME RETRIEVAL ────────────────────────────────────────────

    async def get_regime_for_concept(self, concept_name: str) -> Optional[dict]:
        """
        Get the market regime this concept is activated by (via :ACTIVATED_BY).
        """
        driver = await self._get_driver()
        if not driver:
            return None

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (c:Concept {name: $name})-[:ACTIVATED_BY]->(reg:Regime)
                    RETURN reg.name AS name, reg.description AS description,
                           reg.momentum_score AS momentum_score,
                           reg.vol_level AS vol_level
                    LIMIT 1
                    """,
                    name=concept_name,
                    timeout=5,
                )
                record = await result.single()
                return dict(record) if record else None
        except Exception as e:
            logger.warning("Memgraph get_regime_for_concept failed for '%s': %s", concept_name, e)
            return None

    # ── CATEGORY BROWSING ───────────────────────────────────────────

    async def get_concepts_by_category(self, category: str) -> List[ConceptNode]:
        """
        Get all concepts in a specific category (uses indexed property).
        """
        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (c:Concept {category: $category})
                    RETURN c.name AS name, c.definition AS definition,
                           c.category AS category, c.difficulty AS difficulty
                    ORDER BY c.difficulty, c.name
                    """,
                    category=category,
                    timeout=5,
                )
                records = await result.data()
                return [
                    ConceptNode(
                        name=r.get("name", ""),
                        definition=r.get("definition"),
                        category=r.get("category"),
                        difficulty=r.get("difficulty"),
                        score=1.0,
                    )
                    for r in records
                ]
        except Exception as e:
            logger.warning("Memgraph get_concepts_by_category failed for '%s': %s", category, e)
            return []

    async def get_all_categories(self) -> List[dict]:
        """Get all categories with concept counts."""
        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (cat:Category)<-[:BELONGS_TO]-(c:Concept)
                    RETURN cat.name AS name, cat.display AS display,
                           count(c) AS concept_count
                    ORDER BY concept_count DESC
                    """,
                    timeout=5,
                )
                records = await result.data()
                return records
        except Exception as e:
            logger.warning("Memgraph get_all_categories failed: %s", e)
            return []

    # ── FULL GRAPHRAG RETRIEVAL ──────────────────────────────────────

    async def graphrag_retrieve(self, topic: str, scene_title: str = "") -> GraphRAGResult:
        """
        Primary retrieval method called by SourceRetriever.
        Returns everything the knowledge graph knows about this topic.

        1. find_concepts(topic) → top 5 concepts
        2. For each concept: get formulas
        3. get_concept_subgraph for the primary concept
        4. get_prerequisite_chain for the primary concept
        5. Return unified GraphRAGResult
        """
        driver = await self._get_driver()
        if not driver:
            return GraphRAGResult.empty()

        query = f"{topic} {scene_title}".strip()
        concepts = await self.find_concepts(query, limit=5)
        concept_names = [c.name for c in concepts]

        if not concept_names:
            return GraphRAGResult.empty()

        # Get formulas + subgraph + prereqs in parallel
        equations, subgraph, prereqs = await asyncio.gather(
            self.get_verified_equations(concept_names),
            self.get_concept_subgraph(concept_names[0], depth=2),
            self.get_prerequisite_chain(concept_names[0]),
        )

        return GraphRAGResult(
            topic=topic,
            concepts=concepts,
            equations=equations,  # Formula nodes mapped to EquationNode
            papers=[],  # No Paper nodes in this Memgraph instance
            subgraph=subgraph,
            prerequisite_chain=prereqs,
            concept_names=concept_names,
        )

    # ── RAW QUERY EXECUTION (for source ingestion) ────────────────────

    async def execute_query(self, query: str, params: Optional[dict] = None) -> None:
        """Execute an arbitrary Cypher query against Memgraph.

        Used by SourceExtractor to auto-ingest new Paper nodes and
        BELONGS_TO relationships when a real source is discovered
        that doesn't exist in the graph yet.

        Gracefully handles disabled Memgraph or connection errors.
        """
        driver = await self._get_driver()
        if not driver:
            return
        try:
            async with driver.session() as session:
                await session.run(query, params or {}, timeout=5)
        except Exception as e:
            logger.warning("Memgraph execute_query failed: %s", e)

    # ── CROSS-EPISODE LINKING ────────────────────────────────────────

    async def tag_episode_with_concepts(self, episode_id: str, episode_title: str,
                                        concept_names: List[str]) -> None:
        """
        After successful YouTube upload, write Episode node + COVERS edges
        back into Memgraph. Enables 'See also' cross-linking in YouTube descriptions.
        """
        driver = await self._get_driver()
        if not driver:
            return

        try:
            async with driver.session() as session:
                await session.run(
                    """
                    MERGE (ep:Episode {episode_id: $episode_id})
                    SET ep.title = $title, ep.created_at = timestamp()
                    WITH ep
                    UNWIND $concepts AS concept_name
                    MATCH (c:Concept {name: concept_name})
                    MERGE (ep)-[:COVERS]->(c)
                    """,
                    episode_id=episode_id,
                    title=episode_title,
                    concepts=concept_names,
                    timeout=5,
                )
                logger.info("Tagged episode %s with %d concepts", episode_id, len(concept_names))
        except Exception as e:
            logger.warning("Memgraph tag_episode_with_concepts failed: %s", e)

    async def find_episodes_covering_concept(self, concept_name: str) -> List[dict]:
        """
        Returns episode IDs + titles that cover a given concept.
        Requires Episode:Concept edges added during production.
        """
        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (ep:Episode)-[:COVERS]->(c:Concept {name: $name})
                    RETURN ep.episode_id AS episode_id, ep.title AS title
                    ORDER BY ep.created_at DESC
                    """,
                    name=concept_name,
                    timeout=5,
                )
                records = await result.data()
                return records
        except Exception as e:
            logger.warning("Memgraph find_episodes_covering_concept failed: %s", e)
            return []

    # ── HEALTH ───────────────────────────────────────────────────────

    async def health_check(self) -> dict:
        """Returns connection status, concept count, and graph metadata."""
        driver = await self._get_driver()
        if not driver:
            return {"status": "disabled"}

        try:
            async with driver.session() as session:
                result = await session.run(
                    "MATCH (c:Concept) RETURN count(c) AS concept_count",
                    timeout=5,
                )
                record = await result.single()
                concept_count = record["concept_count"] if record else 0

                # Get relationship stats
                result2 = await session.run(
                    "MATCH ()-[r]->() RETURN type(r) AS rel_type, count(r) AS cnt ORDER BY cnt DESC",
                    timeout=5,
                )
                rel_records = await result2.data()
                rel_summary = {r["rel_type"]: r["cnt"] for r in rel_records}

                return {
                    "status": "connected",
                    "uri": self.settings.memgraph_uri,
                    "concept_count": concept_count,
                    "relationship_counts": rel_summary,
                }
        except Exception as e:
            return {"status": "error", "error": str(e)}