"""LangGraph node implementations for the episode generation pipeline."""
import json
from typing import Any, Dict
from schemas.episode_outline import EpisodeOutline
from schemas.source import SourcesPackage
from schemas.manim_spec import ManimSceneSpec
from schemas.seo import SEOMetadata
from schemas.episode_state import EpisodeState
from services.intelligence.qwen_client import QwenClient
from services.intelligence.outline_generator import OutlineGenerator
from services.intelligence.source_extractor import SourceExtractor
from services.intelligence.script_generator import ScriptGenerator
from services.intelligence.manim_spec_generator import ManimSpecGenerator
from services.intelligence.wan_prompt_generator import WanPromptGenerator
from services.intelligence.seo_generator import SEOGenerator
from services.intelligence.source_retriever import SourceRetriever
from services.ingestion.embedder import ChunkEmbedder
from services.ingestion.memgraph_client import MemgraphClient
from services.generation.wan_client import WanClient
from services.generation.wan_fallback import WanFallback
from services.generation.manim_codegen import ManimCodeGenerator
from services.generation.manim_renderer import ManimRenderer
from services.generation.tts_synthesizer import TTSSynthesizer
from services.generation.av_aligner import AVAligner
from services.composition.scene_syncer import SceneSyncer
from services.composition.episode_compositor import EpisodeCompositor
from services.composition.subtitle_generator import SubtitleGenerator
from services.delivery.thumbnail_generator import ThumbnailGenerator
from services.delivery.youtube_uploader import YouTubeUploader
from core.logging import get_logger

logger = get_logger("orchestration.nodes")

# Initialize services
qwen = QwenClient()
outline_gen = OutlineGenerator(qwen)
source_extractor = SourceExtractor(qwen)
embedder = ChunkEmbedder()
memgraph = MemgraphClient()
source_retriever = SourceRetriever(
    db_session=None,  # Set at runtime via graph context
    memgraph_client=memgraph,
    embedder=embedder,
)
script_gen = ScriptGenerator(qwen, source_retriever=source_retriever)
manim_spec_gen = ManimSpecGenerator(qwen)
wan_prompt_gen = WanPromptGenerator(qwen)
seo_gen = SEOGenerator(qwen)
wan_client = WanClient()
wan_fallback = WanFallback()
manim_codegen = ManimCodeGenerator(qwen)
manim_renderer = ManimRenderer()
tts = TTSSynthesizer()
av_aligner = AVAligner()
scene_syncer = SceneSyncer()
compositor = EpisodeCompositor()
subtitle_gen = SubtitleGenerator()
thumbnail_gen = ThumbnailGenerator()
youtube_uploader = YouTubeUploader()


async def analyze_topic(state: EpisodeState) -> EpisodeState:
    """Node 1: Generate episode outline from topic."""
    logger.info("node:analyze_topic", topic=state["topic"])
    try:
        outline = await outline_gen.generate(
            state["topic"],
            state["episode_number"],
            state["series"],
        )
        state["outline"] = outline.model_dump()
        state["current_phase"] = "outlined"
    except Exception as e:
        state["errors"].append(f"analyze_topic: {e}")
        state["current_phase"] = "failed"
    return state


async def extract_sources(state: EpisodeState) -> EpisodeState:
    """Node 2: Extract academic sources for each scene + run source retrieval."""
    logger.info("node:extract_sources")
    try:
        outline = EpisodeOutline(**state["outline"])
        all_sources = []
        for scene in outline.scenes:
            sources = await source_extractor.extract(scene, outline.topic)
            all_sources.extend(sources)
        state["sources"] = SourcesPackage(
            episode_topic=outline.topic,
            sources=all_sources,
        ).model_dump()

        # Run source retrieval from ingested documents and Memgraph
        try:
            retrieval = await source_retriever.retrieve_for_episode(
                topic=outline.topic,
                outline=outline,
                episode_id=state["episode_id"],
                top_k=5,
            )
            state["retrieval_package"] = retrieval.model_dump()
            state["has_real_sources"] = len(retrieval.vector_chunks) > 0
            if state["has_real_sources"]:
                logger.info(
                    "source_retrieval_found_real_sources",
                    count=retrieval.total_sources,
                )
        except Exception as e:
            logger.warning("source_retrieval_failed", error=str(e))
            state["has_real_sources"] = False

        state["current_phase"] = "sourced"
    except Exception as e:
        state["errors"].append(f"extract_sources: {e}")
    return state


async def generate_script(state: EpisodeState) -> EpisodeState:
    """Node 3: Generate full episode script with source-grounded context."""
    logger.info("node:generate_script")
    try:
        outline = EpisodeOutline(**state["outline"])
        sources = SourcesPackage(**state["sources"])

        # Build retrieval package from state if available
        retrieval = None
        if state.get("retrieval_package"):
            from services.intelligence.source_retriever import RetrievalPackage
            retrieval = RetrievalPackage(**state["retrieval_package"])

        script = await script_gen.generate(outline, sources, retrieval=retrieval)

        # Track unverified claims
        unverified = script.get("unverified_claims", [])
        if unverified:
            logger.warning(
                "script_has_unverified_claims",
                count=len(unverified),
            )
            state["unverified_claims"] = unverified

        state["script"] = script
        state["current_phase"] = "scripted"
    except Exception as e:
        state["errors"].append(f"generate_script: {e}")
    return state


async def generate_manim_specs(state: EpisodeState) -> EpisodeState:
    """Node 4: Generate Manim scene specs."""
    logger.info("node:generate_manim_specs")
    try:
        outline = EpisodeOutline(**state["outline"])
        sources = SourcesPackage(**state["sources"])
        script = state["script"]
        specs = []

        for scene_data in script.get("scenes", []):
            scene_outline = next(
                s for s in outline.scenes
                if s.scene_number == scene_data["scene_number"]
            )
            scene_sources = [s for s in sources.sources if s.ref_number == scene_data["scene_number"]]
            spec = await manim_spec_gen.generate(
                scene_outline,
                scene_data.get("voiceover_text", ""),
                scene_sources,
            )
            specs.append(spec.model_dump())

        state["manim_specs"] = specs
        state["current_phase"] = "specs_generated"
    except Exception as e:
        state["errors"].append(f"generate_manim_specs: {e}")
    return state


async def generate_wan_prompt(state: EpisodeState) -> EpisodeState:
    """Node 5: Generate Wan video prompt."""
    logger.info("node:generate_wan_prompt")
    try:
        outline = EpisodeOutline(**state["outline"])
        prompt = await wan_prompt_gen.generate(outline)
        state["wan_prompt"] = prompt
        state["current_phase"] = "wan_prompted"
    except Exception as e:
        state["errors"].append(f"generate_wan_prompt: {e}")
    return state


async def generate_seo(state: EpisodeState) -> EpisodeState:
    """Node 6: Generate SEO metadata."""
    logger.info("node:generate_seo")
    try:
        outline = EpisodeOutline(**state["outline"])
        seo = await seo_gen.generate(outline)
        state["seo_metadata"] = seo.model_dump()
        state["current_phase"] = "seo_generated"
    except Exception as e:
        state["errors"].append(f"generate_seo: {e}")
    return state


async def synthesize_audio(state: EpisodeState) -> EpisodeState:
    """Node 7: Synthesize TTS audio for each scene."""
    logger.info("node:synthesize_audio")
    try:
        script = state["script"]
        audio_paths = []
        for scene in script.get("scenes", []):
            output_path = f"./output/audio/{state['episode_id']}/scene_{scene['scene_number']}.wav"
            path, duration = await tts.synthesize_scene(
                scene.get("voiceover_text", ""),
                output_path,
            )
            audio_paths.append(str(path))
        state["scene_audio_paths"] = audio_paths
        state["current_phase"] = "audio_synthesized"
    except Exception as e:
        state["errors"].append(f"synthesize_audio: {e}")
    return state


async def generate_wan_clip(state: EpisodeState) -> EpisodeState:
    """Node 8: Generate Wan intro clip (with fallback)."""
    logger.info("node:generate_wan_clip")
    try:
        output_path = f"./output/wan/{state['episode_id']}_intro.mp4"
        try:
            path = await wan_client.generate(
                state.get("wan_prompt", ""),
                WanPromptGenerator.WAN_NEGATIVE_PROMPT,
                output_path,
            )
            state["wan_fallback"] = False
        except Exception as e:
            logger.warning("wan_api_failed_using_fallback", error=str(e))
            path = await wan_fallback.render(
                state["topic"],
                state["episode_id"],
                output_path,
            )
            state["wan_fallback"] = True
        state["wan_clip_path"] = str(path)
        state["current_phase"] = "wan_generated"
    except Exception as e:
        state["errors"].append(f"generate_wan_clip: {e}")
    return state


async def render_manim_scenes(state: EpisodeState) -> EpisodeState:
    """Node 9: Render all Manim scenes."""
    logger.info("node:render_manim_scenes")
    try:
        specs = [ManimSceneSpec(**s) for s in (state.get("manim_specs") or [])]
        if not specs:
            raise ValueError("No manim specs to render")

        # Generate episode file
        script_path = await manim_codegen.generate_episode_file(
            state["episode_id"], specs
        )

        # Render all scenes
        results = await manim_renderer.render_all_scenes(
            str(script_path), specs, state["episode_id"]
        )

        state["scene_video_paths"] = [r.get("path", "") for r in results]
        state["current_phase"] = "scenes_rendered"
    except Exception as e:
        state["errors"].append(f"render_manim_scenes: {e}")
    return state


async def align_av_scenes(state: EpisodeState) -> EpisodeState:
    """Node 10: Align audio and video for each scene."""
    logger.info("node:align_av_scenes")
    try:
        scenes = []
        for i, video_path in enumerate(state.get("scene_video_paths") or []):
            audio_path = (state.get("scene_audio_paths") or [])[i] if i < len(state.get("scene_audio_paths") or []) else ""
            scenes.append({
                "video": video_path,
                "audio": audio_path,
                "scene_number": i + 1,
            })

        synced = await scene_syncer.sync_all(scenes, state["episode_id"])
        state["scene_synced_paths"] = synced
        state["current_phase"] = "av_aligned"
    except Exception as e:
        state["errors"].append(f"align_av_scenes: {e}")
    return state


async def compose_episode(state: EpisodeState) -> EpisodeState:
    """Node 11: Compose final episode video."""
    logger.info("node:compose_episode")
    try:
        output_path = f"./output/episodes/{state['episode_id']}/quantifaya_ep_final.mp4"
        path = await compositor.compose(
            state["episode_id"],
            state.get("wan_clip_path", ""),
            state.get("scene_synced_paths") or [],
            brand_intro_path="./brand/rendered/intro_5s.mp4",
            brand_outro_path="./brand/rendered/outro_5s.mp4",
            output_path=output_path,
        )
        state["final_video_path"] = str(path)
        state["current_phase"] = "composed"
    except Exception as e:
        state["errors"].append(f"compose_episode: {e}")
    return state


async def upload_youtube(state: EpisodeState) -> EpisodeState:
    """Node 12: Upload to YouTube."""
    logger.info("node:upload_youtube")
    try:
        seo = SEOMetadata(**state["seo_metadata"])
        thumbnail_path = f"./output/thumbnails/{state['episode_id']}.jpg"

        # Generate thumbnail
        thumbnail_gen.generate(
            seo.youtube_title[:60],
            "",
            state["episode_number"],
            thumbnail_path,
        )

        # Upload
        video_id = await youtube_uploader.upload(
            state["final_video_path"],
            thumbnail_path,
            seo,
            state.get("youtube_channel_id", ""),
        )
        state["youtube_id"] = video_id
        state["current_phase"] = "uploaded"
    except Exception as e:
        state["errors"].append(f"upload_youtube: {e}")
    return state


async def mark_complete(state: EpisodeState) -> EpisodeState:
    """Node 13: Mark episode as complete."""
    logger.info("node:mark_complete", episode_id=state["episode_id"])
    state["current_phase"] = "delivered"
    return state


async def handle_error(state: EpisodeState) -> EpisodeState:
    """Error handler node."""
    logger.error("node:handle_error", errors=state["errors"])
    state["current_phase"] = "failed"
    return state