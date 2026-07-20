import json
from typing import List, Dict, Any, Optional
from schemas.episode_outline import EpisodeOutline
from schemas.source import SourcesPackage, AcademicSource, GraphRAGResult
from services.intelligence.qwen_client import QwenClient, QWEN_MAX
from services.intelligence.persona import QUANTIFAYA_PERSONA, PERSONA_SELF_REVIEW_CHECKLIST
from services.intelligence.source_retriever import RetrievalPackage, SceneRetrievalResult
from services.ingestion.memgraph_client import MemgraphClient
from core.logging import get_logger

logger = get_logger("script_generator")

SCRIPT_SYSTEM_PROMPT = QUANTIFAYA_PERSONA + """

You are writing the full voice-over script for a Quantifaya episode.
Each scene must have:
- voiceover_text: The spoken narration (300-500 words per scene)
- stage_directions: List of visual/audio cues for the editor

Return JSON with structure:
{
  "episode_id": str,
  "scenes": [
    {
      "scene_number": int,
      "scene_class": str,
      "voiceover_text": str,
      "stage_directions": [str],
      "citations_used": [int],
      "unverified_claims": [str]
    }
  ]
}

IMPORTANT — GraphRAG RULES:
1. Equations tagged [GRAPH-VERIFIED: eq_name] are EXACT — use the LaTeX verbatim.
2. Concepts listed under '=== MEMGRAPH KNOWLEDGE GRAPH ===' are verified by an academic knowledge base.
3. If you use a graph-verified equation, mark it as [GRAPH-VERIFIED: eq_name] in the voiceover text.
4. Claims not backed by either a VERIFIED SOURCE or the MEMGRAPH KNOWLEDGE GRAPH must be [UNVERIFIED: ...].
"""


class ScriptGenerator:
    def __init__(self, qwen: QwenClient, source_retriever: Optional['SourceRetriever'] = None,
                 memgraph: Optional[MemgraphClient] = None):
        self.qwen = qwen
        self.source_retriever = source_retriever
        self.memgraph = memgraph

    async def generate(
        self,
        outline: EpisodeOutline,
        sources: SourcesPackage,
        retrieval: Optional[RetrievalPackage] = None,
    ) -> dict:
        sources_text = "\n".join(
            f"[{s.ref_number}] {s.authors} ({s.year}) '{s.title}' - {s.journal_or_publisher}"
            for s in sources.sources
        )

        scenes_text = "\n".join(
            f"Scene {s.scene_number} ({s.scene_class_name}): {s.title}\n"
            f"  Duration: {s.duration_target_secs}s\n"
            f"  Key equations: {', '.join(s.key_equations)}\n"
            f"  Voiceover hint: {s.voiceover_hint}"
            for s in outline.scenes
        )

        # Build the context block from retrieved sources
        context_block = ""
        if retrieval and retrieval.context_block:
            context_block = retrieval.context_block
        else:
            context_block = (
                "No verified source material was ingested for this episode. "
                "You may use your training knowledge, but every factual claim must be "
                "marked as [UNVERIFIED: claim description]. This helps the human reviewer "
                "identify claims that need verification before publication."
            )

        # ── GraphRAG Context Injection (Phase T) ──────────────────────
        graphrag_block = ""
        graphrag_concepts: List[str] = []
        if self.memgraph and self.memgraph.enabled:
            try:
                # Retrieve knowledge graph context for the episode topic
                graphrag_result = await self.memgraph.graphrag_retrieve(
                    topic=outline.topic,
                    scene_title=outline.seo_title or "",
                )
                if graphrag_result and graphrag_result.has_content():
                    graphrag_block = graphrag_result.to_context_block()
                    graphrag_concepts = graphrag_result.concept_names
                    logger.info(
                        "graphrag_context_injected",
                        topic=outline.topic,
                        concept_count=len(graphrag_concepts),
                        equation_count=len(graphrag_result.equations),
                    )
            except Exception as e:
                logger.warning("graphrag_retrieval_failed", topic=outline.topic, error=str(e))

        # Store concepts for post-upload tagging
        self._last_graphrag_concepts = graphrag_concepts

        messages = [
            {"role": "system", "content": SCRIPT_SYSTEM_PROMPT},
            {"role": "user", "content": (
                f"Write a full script for episode {outline.episode_number} of Quantifaya.\n"
                f"Topic: {outline.topic}\n"
                f"SEO Title: {outline.seo_title}\n\n"
                f"Available academic sources:\n{sources_text}\n\n"
                f"Scene structure:\n{scenes_text}\n\n"
                f"{context_block}\n\n"
                f"{graphrag_block}\n\n"
                "Write the complete script. Every scene must have voiceover_text and stage_directions. "
                "Include [PAUSE] markers. Include *stage directions* in asterisks. "
                "Quote Taleb at least once with exact source. End with a challenge question.\n\n"
                "CRITICAL: Every factual claim must cite a source from the VERIFIED SOURCE MATERIAL "
                "using [N] notation. If the verified material does not cover a claim, you may use "
                "your training knowledge BUT mark it: [UNVERIFIED: claim description]. "
                "[UNVERIFIED] flags are shown to the human reviewer at the review gate."
            )},
        ]

        data = await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.7)

        # Run self-review checklist
        review_result = await self._self_review(data)
        if review_result.get("fixes_required"):
            logger.info("script_self_review_fixes_needed", fixes=review_result["fixes_required"])
            # Regenerate flagged scenes
            for fix in review_result["fixes_required"]:
                scene_num = fix.get("scene_number")
                if scene_num:
                    data = await self._regenerate_scene(data, scene_num, fix.get("fix", ""))

        # Aggregate unverified claims
        unverified_claims = []
        for scene in data.get("scenes", []):
            claims = scene.get("unverified_claims", [])
            if claims:
                unverified_claims.extend(claims)

        if unverified_claims:
            logger.warning(
                "script_contains_unverified_claims",
                count=len(unverified_claims),
                claims=unverified_claims,
            )
            data["unverified_claims"] = unverified_claims

        return data

    async def _self_review(self, script: dict) -> dict:
        messages = [
            {"role": "system", "content": PERSONA_SELF_REVIEW_CHECKLIST},
            {"role": "user", "content": json.dumps(script)},
        ]
        try:
            return await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.2)
        except Exception as e:
            logger.warning("script_self_review_failed", error=str(e))
            return {"scores": {}, "fixes_required": []}

    async def _regenerate_scene(self, script: dict, scene_number: int, fix_instruction: str) -> dict:
        messages = [
            {"role": "system", "content": QUANTIFAYA_PERSONA},
            {"role": "user", "content": (
                f"Regenerate scene {scene_number} of the following script. "
                f"Fix required: {fix_instruction}\n\n"
                f"Current script: {json.dumps(script)}"
            )},
        ]
        try:
            updated = await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.7)
            if "scenes" in updated:
                for scene in updated["scenes"]:
                    if scene.get("scene_number") == scene_number:
                        for i, s in enumerate(script.get("scenes", [])):
                            if s.get("scene_number") == scene_number:
                                script["scenes"][i] = scene
                                break
        except Exception as e:
            logger.warning("scene_regeneration_failed", scene=scene_number, error=str(e))
        return script