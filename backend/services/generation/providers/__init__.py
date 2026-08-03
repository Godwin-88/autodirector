"""Video generation provider abstraction layer.

AutoDirector supports multiple video generation backends behind a common
interface. The active provider is selected via the ``video_gen_provider``
setting, with an optional fallback chain (primary -> fallback -> Manim).

Providers:
    - cogvideox: self-hosted CogVideoX (zero recurring cost)
    - colab:     queue-based GPU worker on Colab T4 (free GPU)
    - wan:       Wan 2.1 via DashScope (legacy, backward compatible)
"""
from typing import Dict, Type

from core.config import get_settings
from core.logging import get_logger

from services.generation.providers.base import VideoGenProvider

logger = get_logger("providers")

# Lazy registry to avoid importing heavy provider deps at module load.
_REGISTRY: Dict[str, Type[VideoGenProvider]] = {}
# Separate flag so that external registration (e.g. tests adding a fake
# provider) does not suppress the lazy import of the real providers.
_IMPORTS_DONE = False


def register_provider(name: str, cls: Type[VideoGenProvider]) -> None:
    """Register a provider class under a config key."""
    _REGISTRY[name] = cls


def _ensure_registry() -> None:
    """Import provider modules lazily so only the configured one is loaded.

    Uses ``importlib.import_module`` (not ``from package import submodule``)
    to avoid a circular import: the submodules themselves import
    ``register_provider`` from this package, which is still partially
    initialized during the first call.
    """
    global _IMPORTS_DONE
    if _IMPORTS_DONE:
        return
    import importlib
    importlib.import_module("services.generation.providers.cogvideox")
    importlib.import_module("services.generation.providers.colab")
    importlib.import_module("services.generation.providers.wan")
    _IMPORTS_DONE = True


def get_video_gen_provider(name: str = "") -> VideoGenProvider:
    """Return the configured video generation provider instance.

    Args:
        name: Optional explicit provider name. Defaults to the
            ``video_gen_provider`` setting.
    """
    _ensure_registry()
    settings = get_settings()
    provider_name = name or settings.video_gen_provider
    if provider_name not in _REGISTRY:
        logger.warning(
            "video_gen_provider_unknown_falling_back_to_wan",
            provider=provider_name,
        )
        provider_name = "wan"
    logger.info("video_gen_provider_selected", provider=provider_name)
    return _REGISTRY[provider_name]()


def get_video_gen_fallback_provider() -> VideoGenProvider:
    """Return the fallback provider (used when the primary fails)."""
    _ensure_registry()
    settings = get_settings()
    fallback = settings.video_gen_fallback_provider
    if fallback not in _REGISTRY:
        logger.warning(
            "video_gen_fallback_unknown_falling_back_to_wan",
            provider=fallback,
        )
        fallback = "wan"
    logger.info("video_gen_fallback_selected", provider=fallback)
    return _REGISTRY[fallback]()