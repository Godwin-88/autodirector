"""Tests for the equation validator."""
import pytest
from services.generation.equation_validator import validate_latex


@pytest.mark.asyncio
async def test_valid_latex():
    """Test that valid LaTeX passes validation."""
    valid, error = await validate_latex(r"\frac{\partial C}{\partial S} = N(d_1)")
    assert valid is True
    assert error == ""


@pytest.mark.asyncio
async def test_invalid_latex():
    """Test that invalid LaTeX fails validation."""
    valid, error = await validate_latex(r"\frac{1}{0}{\sin}")
    # This may parse differently, but should be marked invalid
    assert valid is False or error != ""