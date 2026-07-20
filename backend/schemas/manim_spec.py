from pydantic import BaseModel
from typing import List, Optional


class NarrationBeat(BaseModel):
    """A single narrative beat within a scene — the atomic unit of pedagogy.

    Each beat has:
    - A narration paragraph (full voiceover text for this beat)
    - A pedagogical function (hook | definition | derivation | example |
      comparison | critique | summary | citation | challenge)
    - Word-count aware timing (computed by NarrationTimingService downstream)
    """
    beat_id: str                            # e.g. "A", "B", "C_1"
    narration_text: str                     # full voiceover for this beat
    function: str = "derivation"            # hook|definition|derivation|example|comparison|critique|summary|citation|challenge
    word_count: int = 0                     # computed automatically
    audio_duration_secs: float = 0.0        # filled after TTS generation
    animation_budget_secs: float = 0.0      # how much anim time this beat has
    wait_secs: float = 0.0                  # audio_duration - animation_budget


class SplitScreenConfig(BaseModel):
    """Split-screen layout with left/right panels and optional divider."""
    left_content: List[str] = []            # target_ids on left
    right_content: List[str] = []           # target_ids on right
    divider: bool = True
    left_title: str = ""
    right_title: str = ""


class VisualClimaxConfig(BaseModel):
    """Dramatic animation effects for key moments."""
    style: str = "pulse"                    # pulse|sparks|cancellation|cross_out|glow|explode
    target_ids: List[str] = []
    glow_color: str = "GOLD"
    duration_secs: float = 2.0
    label_text: str = ""


class PersistentElement(BaseModel):
    """An element that stays on screen across multiple beats."""
    element_id: str                         # target_id of the element
    fade_in_at_beat: str = "A"              # beat when it appears
    fade_out_at_beat: Optional[str] = None  # beat when it disappears
    initial_position: str = "center"


class EquationSpec(BaseModel):
    id: str                          # e.g. "eq_001"
    latex: str
    color: str = "FG"                # brand color constant name
    position: str = "center"         # center|top|bottom|left|right
    animation_type: str = "Write"    # Write|FadeIn|Transform
    font_size: int = 34
    beat_id: str = ""                # which narration beat this belongs to


class TextBlockSpec(BaseModel):
    id: str
    content: str
    color: str = "FG"
    font_size: int = 24
    weight: str = "normal"           # normal|BOLD
    slant: str = "normal"            # normal|ITALIC
    position: str = "center"
    beat_id: str = ""


class AxesConfig(BaseModel):
    x_range: List[float]
    y_range: List[float]
    x_label: str
    y_label: str
    x_length: float = 10.0
    y_length: float = 5.0
    beat_id: str = ""


class CurveSpec(BaseModel):
    id: str
    function_description: str        # LaTeX or human-readable description
    color: str = "BLUE_NORM"
    stroke_width: float = 3.0
    x_range: Optional[List[float]] = None
    beat_id: str = ""


class AnimationStep(BaseModel):
    step_number: int
    type: str    # Write|FadeIn|Create|Transform|FadeOut|SurroundingRectangle|
                 # wait|FadeInFromLeft|FadeInFromRight|FadeInFromTop|FadeInFromBottom|
                 # CrossOut|Spark|Glow|Pulse|ReplacementTransform|LaggedStart|
                 # Parallel|SplitScreenEnter|SplitScreenExit
    target_id: str
    duration_secs: float = 0.5
    beat_id: str = ""                # which beat this step belongs to
    notes: str = ""
    position: str = "center"         # where to place the target
    persistent: bool = False         # stays on screen across beats
    visual_climax: bool = False      # triggers special effects if True


class CitationEntry(BaseModel):
    """A single academic citation for on-screen display."""
    ref_number: int
    text: str                        # "Authors (Year), Journal, pp.X–Y"
    doi_or_url: str = ""


class ManimSceneSpec(BaseModel):
    """Complete specification for a single Manim scene.

    Now includes beat-structured narration, split-screen layouts,
    persistent elements, visual climax effects, and narrative function metadata.
    This is what the upgraded manim_spec_generator produces.
    """
    scene_class_name: str
    scene_title: str = ""
    scenario_number: int = 0
    narrative_function: str = "derivation"  # hook|definition|derivation|example|comparison|critique|summary|citation|challenge

    # — Beat structure —
    beats: List[NarrationBeat] = []
    total_word_count: int = 0             # computed from beats
    total_audio_duration_secs: float = 0.0  # computed after TTS

    # — Visual elements —
    equations: List[EquationSpec] = []
    text_blocks: List[TextBlockSpec] = []
    curves: List[CurveSpec] = []
    axes_config: Optional[AxesConfig] = None

    # — Layout —
    split_screen: Optional[SplitScreenConfig] = None
    persistent_elements: List[PersistentElement] = []
    visual_climax: Optional[VisualClimaxConfig] = None

    # — Animation —
    animation_sequence: List[AnimationStep]

    # — Academic context —
    citations: List[CitationEntry] = []
    cite_string: str = ""

    # — Brand —
    background_color: str = "#0D1117"

    # — Timing (computed by NarrationTimingService) —
    timing_validated: bool = False

    # — Template hints (for manim_codegen) —
    suggested_template: str = "auto"  # auto|equation_reveal|axes_curve|two_column|quote_box|
                                      # sigmoid_curve|two_panel_comparison|spark_cancellation|
                                      # animated_table|time_acceleration|pnl_attribution|
                                      # side_by_side_integrals|qq_plot|multiplication_table|
                                      # numbered_list|narrative_beat_sequence

    def compute_word_counts(self) -> None:
        """Sum word counts across all beats."""
        total = 0
        for beat in self.beats:
            beat.word_count = len(beat.narration_text.split())
            total += beat.word_count
        self.total_word_count = total

    def compute_timing(self, total_audio_secs: float) -> None:
        """Distribute audio duration across beats proportional to word count."""
        self.compute_word_counts()
        if self.total_word_count == 0:
            return
        for beat in self.beats:
            proportion = beat.word_count / self.total_word_count
            beat.audio_duration_secs = proportion * total_audio_secs
            # beat.wait_secs is computed by NarrationTimingService
            # which subtracts the actual animation time from the audio budget
        self.total_audio_duration_secs = total_audio_secs
        self.timing_validated = True