from pydantic import BaseModel
from typing import List, Optional


class AcademicSource(BaseModel):
    ref_number: int
    authors: str
    year: int
    title: str
    journal_or_publisher: str
    doi_or_url: str = ""
    scene_usage_note: str
    confidence: str = "high"         # high|low — low = flagged for human review
    graph_verified: bool = False     # NEW: True if cross-referenced against Memgraph


class SourcesPackage(BaseModel):
    episode_topic: str
    sources: List[AcademicSource]


# ── Memgraph GraphRAG Schemas ──────────────────────────────────────────────

class ConceptNode(BaseModel):
    name: str
    definition: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    score: float = 1.0


class EquationNode(BaseModel):
    id: str
    latex: str
    description: Optional[str] = None
    source: Optional[str] = None
    concept_name: str


class PaperNode(BaseModel):
    title: str
    authors: str
    year: int
    doi: Optional[str] = None
    journal: Optional[str] = None
    abstract: Optional[str] = None
    covered_concepts: List[str] = []
    concept_count: int = 1


class GraphRAGResult(BaseModel):
    topic: str
    concepts: List[ConceptNode] = []
    equations: List[EquationNode] = []
    papers: List[PaperNode] = []
    subgraph: dict = {"nodes": [], "edges": []}
    prerequisite_chain: List[str] = []
    concept_names: List[str] = []

    @classmethod
    def empty(cls) -> "GraphRAGResult":
        return cls(topic="")

    def has_content(self) -> bool:
        return len(self.concepts) > 0

    def get_verified_latex_for_concept(self, concept_name: str) -> Optional[str]:
        """Return the verified LaTeX string for a concept, if it exists."""
        for eq in self.equations:
            if eq.concept_name.lower() == concept_name.lower():
                return eq.latex
        return None

    def has_paper(self, authors: str, year: int, title: str) -> bool:
        """Check if a paper exists in the graph's paper nodes (fuzzy match)."""
        for p in self.papers:
            if p.year == year and (
                p.authors.lower()[:15] in authors.lower()
                or authors.lower()[:15] in p.authors.lower()
            ):
                return True
        return False

    def to_context_block(self) -> str:
        if not self.has_content():
            return ""
        lines = ["=== MEMGRAPH KNOWLEDGE GRAPH ==="]
        lines.append(f"Primary concepts: {', '.join(self.concept_names)}")
        if self.equations:
            lines.append("\nVERIFIED EQUATIONS (use these LaTeX strings exactly):")
            for eq in self.equations:
                lines.append(f"  [{eq.concept_name}] {eq.latex} — {eq.description or ''}")
        if self.papers:
            lines.append("\nVERIFIED PAPERS (cite these, they are real):")
            for p in self.papers:
                lines.append(f"  {p.authors} ({p.year}). {p.title}. {p.journal or ''}. DOI: {p.doi or 'N/A'}")
        if self.prerequisite_chain:
            lines.append(f"\nPrerequisite concepts (for recap scene): {', '.join(self.prerequisite_chain)}")
        lines.append("=================================")
        return "\n".join(lines)