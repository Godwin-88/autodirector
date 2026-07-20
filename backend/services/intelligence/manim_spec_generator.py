"""ManimSpecGenerator — beat-aware scene spec generator.

Given a scene outline with full voiceover text broken into narration beats,
this generator produces a ManimSceneSpec with:

1. Beat-structured narration (voiceover split into pedagogical beats)
2. Word-count proportional timing (using NarrationTimingService)
3. Rich scene patterns (sigmoid curves, two-panel comparisons, spark cancellations,
   animated tables, time-acceleration plots, side-by-side integrals, etc.)
4. Persistent elements that stay across beats
5. Visual climax effects for dramatic moments
6. Citations drawn from verified sources
"""
from typing import List, Optional, Dict, Any
from schemas.episode_outline import SceneOutlineItem, SceneBeat
from schemas.source import AcademicSource
from schemas.manim_spec import (
    ManimSceneSpec, NarrationBeat, EquationSpec, TextBlockSpec,
    AxesConfig, CurveSpec, AnimationStep, SplitScreenConfig,
    VisualClimaxConfig, PersistentElement, CitationEntry,
)
from services.intelligence.qwen_client import QwenClient, QWEN_MAX
from services.intelligence.narration_timing import NarrationTimingService
from core.logging import get_logger

logger = get_logger("manim_spec_generator")

MANIM_SPEC_PROMPT = """
You are a Manim animation engineer and quant finance educator. Given a scene outline,
full voiceover text broken into beats, and academic sources, generate a structured
Manim scene specification as JSON.

The spec must use the Quantifaya brand animation language:

NARRATIVE FUNCTIONS (one per scene):
- hook: cold open, shocking fact, crisis
- definition: formal definition of a term or equation
- derivation: step-by-step mathematical derivation
- example: concrete numerical example
- comparison: side-by-side two-panel comparison
- critique: Taleb-style takedown of textbook assumptions
- summary: checklist recap of what was covered
- citation: academic source references

SCENE PATTERNS (set suggested_template):
- equation_reveal: show an equation with animated writing
- axes_curve: plot on axes with labelled curves
- two_column: two panels side by side
- quote_box: highlighted quote from Taleb or other authority
- sigmoid_curve: S-curve (e.g. Delta vs S) with tangent lines and labelled points
- two_panel_comparison: two panels (e.g. Long Gamma vs Short Gamma)
- spark_cancellation: two terms highlight, cross out, explode off screen
- animated_table: data table with highlighted rows/columns
- time_acceleration: curve that steepens over time
- pnl_attribution: mathematical P&L breakdown with colour-coded terms
- side_by_side_integrals: two integral forms side by side with difference highlighted
- qq_plot: Q-Q plot with S-curve deviation and labelled tail curl
- multiplication_table: Itô table or similar with glowing key entry
- numbered_list: numbered points appearing one by one with icons

For each beat, the spec must provide BOTH the narration_text AND visual elements
(equations, text_blocks, curves) that appear during that beat, with beat_id set
on each element.

Critical rules:
1. Equations tagged [GRAPH-VERIFIED: eq_name] in the voiceover must use exact LaTeX
2. Every factual claim must cite a source using [N] notation
3. Keep visual complexity appropriate: 1-2 key visual elements per beat
4. Use dramatic visual climax effects (sparks, cross-outs, glowing) only for key moments

Animation types available: Write|FadeIn|Create|Transform|FadeOut|Replace|
CrossOut|Spark|Glow|Pulse|FadeInFromLeft|FadeInFromRight|FadeInFromTop|
FadeInFromBottom|SurroundingRectangle|LaggedStart

Colors: FG|GOLD|RED|GREEN|BLUE_NORM|ORANGE|PURPLE|TEAL

Return valid JSON only. No markdown fences. No preamble.
"""


class ManimSpecGenerator:
    """Generates beat-aware ManimSceneSpec from scene outline + voiceover + sources."""

    def __init__(self, qwen: QwenClient):
        self.qwen = qwen

    def _build_prompt_context(self, scene: SceneOutlineItem,
                               sources: List[AcademicSource]) -> str:
        """Build the user prompt context from scene data."""
        sources_text = "\n".join(
            f"[{s.ref_number}] {s.authors} ({s.year}) '{s.title}' - {s.journal_or_publisher}"
            for s in sources
        )

        citations_text = "\n".join(
            f"[{s.ref_number}: fig {s.scene_usage_note or ''}] {s.authors} ({s.year})"
            for s in sources
        )

        # Build beat-aware scene structure description
        if scene.beats:
            beats_text = "\n".join(
                f"Beat {b.beat_id} (function: {b.function}): {b.narration_text[:100]}..."
                for b in scene.beats
            )
        else:
            beats_text = f"Voiceover hint: {scene.voiceover_hint}"

        return (
            f"Scene {scene.scene_number}: {scene.title}\n"
            f"Scene class: {scene.scene_class_name}\n"
            f"Narrative function: {scene.narrative_function}\n"
            f"Duration target: {scene.duration_target_secs}s\n"
            f"Key equations: {', '.join(scene.key_equations)}\n"
            f"Sources provided:\n{sources_text}\n\n"
            f"Citations to use:\n{citations_text}\n\n"
            f"Scene structure (beats):\n{beats_text}\n\n"
            f"Full voiceover:\n{scene.full_voiceover[:1500]}\n\n"
            "Generate the complete Manim scene spec JSON. "
            "Include all beats with narration_text, beat_id, and function. "
            "Set suggested_template based on the best visual pattern for this scene. "
            "Every equation and text_block must have a beat_id linking it to the beat "
            "it appears in. Use persistent_elements for elements that span multiple beats. "
            "Use visual_climax for the single most dramatic moment in the scene."
        )

    async def generate(self, scene: SceneOutlineItem,
                        sources: List[AcademicSource]) -> ManimSceneSpec:
        """Generate a complete ManimSceneSpec for one scene."""
        messages = [
            {"role": "system", "content": MANIM_SPEC_PROMPT},
            {"role": "user", "content": self._build_prompt_context(scene, sources)},
        ]

        data = await self.qwen.complete_json(QWEN_MAX, messages, temperature=0.4)

        # Override key fields from the scene outline
        data["scene_class_name"] = scene.scene_class_name
        data["scene_title"] = scene.title
        data["scenario_number"] = scene.scene_number
        data["narrative_function"] = scene.narrative_function

        # If beats were provided in the outline, use them as the base for
        # the NarrationBeat objects, augmented with Qwen's visual suggestions
        if scene.beats:
            existing_beats = {b.beat_id: b for b in scene.beats}
            llm_beats = {b.get("beat_id", ""): b for b in data.get("beats", [])}

            merged_beats = []
            for beat_id in sorted(set(list(existing_beats.keys()) + list(llm_beats.keys()))):
                eb = existing_beats.get(beat_id)
                lb = llm_beats.get(beat_id, {})
                if eb:
                    merged_beats.append(NarrationBeat(
                        beat_id=eb.beat_id,
                        narration_text=lb.get("narration_text", eb.narration_text),
                        function=lb.get("function", eb.function),
                    ))
                elif lb:
                    merged_beats.append(NarrationBeat(**lb))
            data["beats"] = [b.model_dump() for b in merged_beats]

        # Build CitationEntry objects from the sources
        data["citations"] = [
            {
                "ref_number": s.ref_number,
                "text": f"{s.authors} ({s.year}). {s.title}. {s.journal_or_publisher}.",
                "doi_or_url": s.doi_or_url,
            }
            for s in sources
        ]

        # Construct the spec
        spec = ManimSceneSpec(**data)

        # Compute word counts and timing
        spec.compute_word_counts()

        logger.info(
            "manim_spec_generated",
            scene=spec.scene_class_name,
            beats=len(spec.beats),
            total_words=spec.total_word_count,
            equations=len(spec.equations),
            text_blocks=len(spec.text_blocks),
            template=spec.suggested_template,
        )
        return spec