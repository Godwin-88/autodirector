"""NarrationTimingService — word-count proportional timing engine.

This service eliminates the manual self.wait() calibration that the hand-crafted
episodes require. Instead, it:

1. Takes a scene spec with NarrationBeat objects containing full voiceover text
2. Computes word counts per beat
3. After TTS generation provides actual audio durations, distributes the
   total duration across beats proportionally to word count
4. Subtracts the declared animation budget (sum of self.play() durations)
   to compute the required self.wait() per beat
"""
from typing import List, Optional
from schemas.manim_spec import ManimSceneSpec, NarrationBeat
from core.logging import get_logger

logger = get_logger("narration_timing")


class NarrationTimingService:
    """Computes word-count proportional timing for scene narration beats."""

    @staticmethod
    def compute_word_counts_from_beats(beats: List[NarrationBeat]) -> int:
        """Sum word counts across all beats in a list."""
        total = 0
        for beat in beats:
            beat.word_count = len(beat.narration_text.split())
            total += beat.word_count
        return total

    @staticmethod
    def compute_word_counts(scene: ManimSceneSpec) -> int:
        """Compute word counts for all beats in a scene spec."""
        return NarrationTimingService.compute_word_counts_from_beats(scene.beats)

    @staticmethod
    def distribute_timing(scene: ManimSceneSpec) -> ManimSceneSpec:
        """Distribute audio duration across beats proportional to word count.

        Call this AFTER TTS has generated audio and the total_audio_duration_secs
        has been filled in the scene spec.

        For each beat:
        - proportion = beat.word_count / total_word_count
        - beat.audio_duration_secs = proportion * total_audio_secs
        - beat.wait_secs = max(0, beat.audio_duration_secs - beat.animation_budget_secs)
        """
        total_words = NarrationTimingService.compute_word_counts(scene)
        if total_words == 0:
            logger.warning("narration_timing_zero_words", scene=scene.scene_class_name)
            return scene

        total_audio = scene.total_audio_duration_secs
        if total_audio <= 0:
            logger.warning("narration_timing_zero_audio", scene=scene.scene_class_name)
            return scene

        for beat in scene.beats:
            proportion = beat.word_count / total_words
            beat.audio_duration_secs = proportion * total_audio
            beat.wait_secs = max(0.0, beat.audio_duration_secs - beat.animation_budget_secs)

        scene.timing_validated = True
        logger.info(
            "narration_timing_distributed",
            scene=scene.scene_class_name,
            beats=len(scene.beats),
            total_audio=round(total_audio, 2),
            total_words=total_words,
        )
        return scene

    @staticmethod
    def compute_animation_budget(scene: ManimSceneSpec) -> float:
        """Sum the declared animation durations across all beats.

        This provides a rough estimate of total animation time per beat.
        For precise timing, each beat's animation_budget_secs should be set
        explicitly by the code generator based on actual self.play() run_times.
        """
        budget_by_beat: dict = {}
        for step in scene.animation_sequence:
            beat_id = step.beat_id or "A"
            if beat_id not in budget_by_beat:
                budget_by_beat[beat_id] = 0.0
            budget_by_beat[beat_id] += step.duration_secs

        for beat in scene.beats:
            beat.animation_budget_secs = budget_by_beat.get(beat.beat_id, 0.0)

        return sum(budget_by_beat.values())

    @staticmethod
    def generate_wait_code(scene: ManimSceneSpec) -> List[str]:
        """Generate the self.wait() calls for each beat.

        Returns a list of strings like:
        'self.wait(38.5)  # Beat-A: derivation (38.5s remaining)'
        """
        if not scene.timing_validated:
            NarrationTimingService.distribute_timing(scene)

        lines = []
        for beat in scene.beats:
            wait = round(beat.wait_secs, 2)
            if wait < 0:
                wait = 0.0
            lines.append(
                f"self.wait({wait})  # Beat-{beat.beat_id}: {beat.function} "
                f"({wait}s audio remaining after {round(beat.animation_budget_secs, 1)}s anim)"
            )
        return lines

    @staticmethod
    def beats_to_code(scene: ManimSceneSpec, indentation: str = "        ") -> str:
        """Generate the full code block for beat-level timing in a Manim scene.

        This produces the pattern:
            # ── BEAT A: derivation (56.6s | anim≈8s | wait=48s) ──
            self.add_sound(f"{{AUDIO_DIR}}/scene1_beat_a.mp3")
            [animation code]
            self.wait(48)
        """
        if not scene.timing_validated:
            NarrationTimingService.distribute_timing(scene)
            NarrationTimingService.compute_animation_budget(scene)

        lines = []
        for beat in scene.beats:
            anim_budget = round(beat.animation_budget_secs, 1)
            wait = round(beat.wait_secs, 1)
            total = round(beat.audio_duration_secs, 1)

            lines.append("")
            lines.append(
                f"{indentation}# ── BEAT {beat.beat_id}: {beat.function} "
                f"({total}s | anim≈{anim_budget}s | wait={wait}s) ──"
            )

        return "\n".join(lines)