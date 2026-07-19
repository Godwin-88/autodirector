"""
Memgraph GraphRAG Client — Phase E of Source Intelligence Layer.

Queries the existing Memgraph quant finance knowledge graph for:
  - Concept definitions and relationships
  - Verified LaTeX equations
  - Real paper citations (zero hallucination risk)
  - Local subgraph for Manim visualisation

Memgraph is Neo4j-compatible (uses Bolt protocol).
Degrades gracefully when MEMGRAPH_ENABLED=false.
"""

import logging
from typing import List, Optional

from core.config import get_settings

logger = logging.getLogger(__name__)


class MemgraphClient:
    """
    Queries the existing Memgraph quant finance knowledge graph.
    Connection configured via MEMGRAPH_URI, MEMGRAPH_USER, MEMGRAPH_PASSWORD env vars.
    All methods return empty results when MEMGRAPH_ENABLED=false.
    """

    def __init__(self):
        self.settings = get_settings()
        self.enabled = getattr(self.settings, "MEMGRAPH_ENABLED", False)
        self._driver = None

    async def _get_driver(self):
        """Lazy-initialize the Neo4j/Memgraph driver."""
        if not self.enabled:
            return None
        if self._driver is not None:
            return self._driver

        try:
            from neo4j import AsyncGraphDatabase

            uri = getattr(self.settings, "MEMGRAPH_URI", "bolt://localhost:7687")
            user = getattr(self.settings, "MEMGRAPH_USER", "")
            password = getattr(self.settings, "MEMGRAPH_PASSWORD", "")

            if user and password:
                self._driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
            else:
                self._driver = AsyncGraphDatabase.driver(uri)

            logger.info("Connected to Memgraph at %s", uri)
            return self._driver
        except ImportError:
            logger.warning("neo4j driver not installed, Memgraph unavailable")
            self.enabled = False
            return None
        except Exception as e:
            logger.warning("Failed to connect to Memgraph: %s", e)
            self.enabled = False
            return None

    async def health_check(self) -> bool:
        """Check if Memgraph connection is alive."""
        if not self.enabled:
            return False
        driver = await self._get_driver()
        if not driver:
            return False
        try:
            async with driver.session() as session:
                result = await session.run("RETURN 1 AS alive")
                record = await result.single()
                return record is not None and record.get("alive") == 1
        except Exception as e:
            logger.warning("Memgraph health check failed: %s", e)
            return False

    async def query_concept(self, concept: str) -> dict:
        """
        Query a specific concept node with all its relationships.

        MATCH (c:Concept {name: $concept})-[r]-(related)
        RETURN c, type(r) as rel_type, related
        """
        if not self.enabled:
            return {}

        driver = await self._get_driver()
        if not driver:
            return {}

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (c:Concept {name: $concept})-[r]-(related)
                    RETURN c.name AS name, c.definition AS definition,
                           c.equations AS equations,
                           type(r) AS rel_type,
                           related.name AS related_name,
                           labels(related) AS related_labels
                    """,
                    concept=concept,
                )
                records = await result.fetch(100)

                if not records:
                    return {"found": False, "concept": concept}

                concept_data = {
                    "found": True,
                    "name": records[0].get("name"),
                    "definition": records[0].get("definition"),
                    "equations": records[0].get("equations", []),
                    "relationships": [],
                }

                for record in records:
                    concept_data["relationships"].append({
                        "type": record.get("rel_type"),
                        "target_name": record.get("related_name"),
                        "target_labels": record.get("related_labels", []),
                    })

                return concept_data
        except Exception as e:
            logger.warning("Memgraph query_concept failed for '%s': %s", concept, e)
            return {"error": str(e), "concept": concept}

    async def find_related_concepts(self, topic: str, limit: int = 10) -> List[dict]:
        """
        Full-text search or fuzzy match on concept names.

        CALL db.index.fulltext.queryNodes("conceptIndex", $topic) YIELD node, score
        RETURN node.name, node.definition, node.equations, score
        """
        if not self.enabled:
            return []

        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                # Try fulltext index first
                try:
                    result = await session.run(
                        """
                        CALL db.index.fulltext.queryNodes("conceptIndex", $topic)
                        YIELD node, score
                        RETURN node.name AS name, node.definition AS definition,
                               node.equations AS equations, score
                        ORDER BY score DESC
                        LIMIT $limit
                        """,
                        topic=topic,
                        limit=limit,
                    )
                    records = await result.fetch(limit)
                    if records:
                        return [
                            {
                                "name": r.get("name"),
                                "definition": r.get("definition"),
                                "equations": r.get("equations", []),
                                "score": r.get("score"),
                            }
                            for r in records
                        ]
                except Exception:
                    logger.info("Fulltext index not found, falling back to CONTAINS search")

                # Fallback: CONTAINS search
                result = await session.run(
                    """
                    MATCH (c:Concept)
                    WHERE toLower(c.name) CONTAINS toLower($topic)
                    RETURN c.name AS name, c.definition AS definition,
                           c.equations AS equations
                    LIMIT $limit
                    """,
                    topic=topic,
                    limit=limit,
                )
                records = await result.fetch(limit)
                return [
                    {
                        "name": r.get("name"),
                        "definition": r.get("definition"),
                        "equations": r.get("equations", []),
                        "score": 1.0,
                    }
                    for r in records
                ]
        except Exception as e:
            logger.warning("Memgraph find_related_concepts failed for '%s': %s", topic, e)
            return []

    async def get_concept_equations(self, concept: str) -> List[dict]:
        """
        Get verified LaTeX equations for a concept.

        MATCH (c:Concept {name: $concept})-[:HAS_EQUATION]->(e:Equation)
        RETURN e.latex, e.description, e.source
        """
        if not self.enabled:
            return []

        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (c:Concept {name: $concept})-[:HAS_EQUATION]->(e:Equation)
                    RETURN e.latex AS latex, e.description AS description,
                           e.source AS source
                    """,
                    concept=concept,
                )
                records = await result.fetch(50)
                return [
                    {
                        "latex": r.get("latex"),
                        "description": r.get("description"),
                        "source": r.get("source"),
                    }
                    for r in records
                ]
        except Exception as e:
            logger.warning("Memgraph get_concept_equations failed for '%s': %s", concept, e)
            return []

    async def get_concept_papers(self, concept: str) -> List[dict]:
        """
        Get real papers citing this concept from the knowledge graph.

        MATCH (c:Concept {name: $concept})-[:CITED_IN]->(p:Paper)
        RETURN p.title, p.authors, p.year, p.doi, p.journal
        """
        if not self.enabled:
            return []

        driver = await self._get_driver()
        if not driver:
            return []

        try:
            async with driver.session() as session:
                result = await session.run(
                    """
                    MATCH (c:Concept {name: $concept})-[:CITED_IN]->(p:Paper)
                    RETURN p.title AS title, p.authors AS authors,
                           p.year AS year, p.doi AS doi, p.journal AS journal
                    """,
                    concept=concept,
                )
                records = await result.fetch(50)
                return [
                    {
                        "title": r.get("title"),
                        "authors": r.get("authors"),
                        "year": r.get("year"),
                        "doi": r.get("doi"),
                        "journal": r.get("journal"),
                    }
                    for r in records
                ]
        except Exception as e:
            logger.warning("Memgraph get_concept_papers failed for '%s': %s", concept, e)
            return []

    async def get_concept_subgraph(self, concept: str, depth: int = 2) -> dict:
        """
        Get the local subgraph around a concept for Manim visualisation.

        MATCH path = (c:Concept {name: $concept})-[*1..{depth}]-(related)
        Returns nodes and edges for graph rendering.
        """
        if not self.enabled:
            return {"nodes": [], "edges": []}

        driver = await self._get_driver()
        if not driver:
            return {"nodes": [], "edges": []}

        try:
            async with driver.session() as session:
                result = await session.run(
                    f"""
                    MATCH path = (c:Concept {{name: $concept}})-[*1..{depth}]-(related)
                    UNWIND nodes(path) AS n
                    RETURN DISTINCT n.name AS name, labels(n) AS labels,
                           n.definition AS definition
                    """,
                    concept=concept,
                )
                node_records = await result.fetch(200)

                nodes = []
                seen_names = set()
                for r in node_records:
                    name = r.get("name")
                    if name and name not in seen_names:
                        seen_names.add(name)
                        nodes.append({
                            "name": name,
                            "labels": r.get("labels", []),
                            "definition": r.get("definition"),
                        })

                # Get edges
                result2 = await session.run(
                    f"""
                    MATCH path = (c:Concept {{name: $concept}})-[r*1..{depth}]-(related)
                    UNWIND r AS rel
                    RETURN DISTINCT startNode(rel).name AS source,
                           type(rel) AS type,
                           endNode(rel).name AS target
                    """,
                    concept=concept,
                )
                edge_records = await result2.fetch(500)
                edges = [
                    {
                        "source": r.get("source"),
                        "type": r.get("type"),
                        "target": r.get("target"),
                    }
                    for r in edge_records
                ]

                return {"nodes": nodes, "edges": edges}
        except Exception as e:
            logger.warning("Memgraph get_concept_subgraph failed for '%s': %s", concept, e)
            return {"nodes": [], "edges": []}

    async def graphrag_retrieve(self, topic: str, scene_title: str) -> dict:
        """
        Unified GraphRAG retrieval for a topic + scene.

        1. find_related_concepts(topic) → top 5 concepts
        2. For each concept: get_concept_equations + get_concept_papers
        3. get_concept_subgraph for the primary concept
        4. Return unified result
        """
        if not self.enabled:
            return {"concepts": [], "equations": [], "papers": [], "subgraph": {"nodes": [], "edges": []}}

        concepts = await self.find_related_concepts(topic, limit=5)

        all_equations = []
        all_papers = []
        primary_subgraph = {"nodes": [], "edges": []}

        for i, concept in enumerate(concepts):
            name = concept.get("name", "")
            if not name:
                continue

            equations = await self.get_concept_equations(name)
            all_equations.extend(equations)

            papers = await self.get_concept_papers(name)
            all_papers.extend(papers)

            if i == 0:
                primary_subgraph = await self.get_concept_subgraph(name)

        return {
            "concepts": concepts,
            "equations": all_equations,
            "papers": all_papers,
            "subgraph": primary_subgraph,
        }

    async def close(self):
        """Close the driver connection."""
        if self._driver:
            await self._driver.close()
            self._driver = None