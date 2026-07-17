import tempfile
import py_compile
from typing import Tuple
from services.intelligence.qwen_client import QwenClient, QWEN_MAX
from core.logging import get_logger

logger = get_logger("equation_validator")

TEST_TEMPLATE = """
from manim import MathTex
eq = MathTex(r"{latex}")
"""


async def validate_latex(latex: str) -> Tuple[bool, str]:
    """Validate a LaTeX string by attempting to compile a minimal Manim test."""
    content = TEST_TEMPLATE.format(latex=latex)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(content)
        tmp_path = f.name

    try:
        py_compile.compile(tmp_path, doraise=True)
        return True, ""
    except py_compile.PyCompileError as e:
        return False, str(e)


async def validate_and_fix(latex: str, qwen: QwenClient) -> str:
    """Validate LaTeX and fix if needed. Max 2 rounds."""
    for attempt in range(2):
        valid, error = await validate_latex(latex)
        if valid:
            return latex

        logger.warning("latex_validation_failed", latex=latex, error=error, attempt=attempt + 1)
        messages = [
            {"role": "system", "content": "Fix the following LaTeX equation so it's valid for Manim's MathTex. Return ONLY the fixed LaTeX string, no explanation."},
            {"role": "user", "content": f"Invalid LaTeX: {latex}\nError: {error}\n\nReturn the corrected LaTeX:"},
        ]
        latex = await qwen.complete(QWEN_MAX, messages, temperature=0.2)
        latex = latex.strip().strip("`").strip()

    # If still failing after 2 rounds, return plain text equivalent
    logger.warning("latex_fix_failed_after_retries", latex=latex)
    return latex.replace("\\", "").replace("{", "").replace("}", "")