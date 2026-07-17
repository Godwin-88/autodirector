from pydantic import BaseModel
from typing import List, Optional


class EquationSpec(BaseModel):
    id: str                          # e.g. "eq_001"
    latex: str
    color: str = "FG"                # brand color constant name
    position: str = "center"         # center|top|bottom|left|right
    animation_type: str = "Write"    # Write|FadeIn|Transform


class TextBlockSpec(BaseModel):
    id: str
    content: str
    color: str = "FG"
    font_size: int = 24
    weight: str = "normal"           # normal|BOLD
    slant: str = "normal"            # normal|ITALIC


class AxesConfig(BaseModel):
    x_range: List[float]
    y_range: List[float]
    x_label: str
    y_label: str
    x_length: float = 10.0
    y_length: float = 5.0


class AnimationStep(BaseModel):
    step_number: int
    type: str    # Write|FadeIn|Create|Transform|FadeOut|SurroundingRectangle|wait|FadeInFromLeft
    target_id: str
    duration_secs: float = 0.5
    notes: str = ""


class ManimSceneSpec(BaseModel):
    scene_class_name: str
    equations: List[EquationSpec] = []
    text_blocks: List[TextBlockSpec] = []
    axes_config: Optional[AxesConfig] = None
    animation_sequence: List[AnimationStep]
    cite_string: str = ""
    background_color: str = "#0D1117"