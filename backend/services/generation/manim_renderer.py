import subprocess
import asyncio
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
from schemas.manim_spec import ManimSceneSpec
from core.config import get_settings
from core.logging import get_logger

logger = get_logger("manim_renderer")


class ManimRenderTimeout(Exception):
    pass


class ManimRenderError(Exception):
    pass


class ManimRenderer:
    def __init__(self):
        self.settings = get_settings()

    async def render_scene(self, script_path: str, scene_class: str,
                           episode_id: str, scene_number: int) -> Path:
        """Render a single Manim scene class to MP4."""
        output_base = Path(f"./output/scenes/{episode_id}")
        output_base.mkdir(parents=True, exist_ok=True)

        quality = self.settings.manim_quality
        cmd = [
            "manim", f"-pq{quality}",
            script_path,
            scene_class,
            "--fps", "60",
            "--media_dir", str(output_base),
        ]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)
            except asyncio.TimeoutError:
                proc.kill()
                raise ManimRenderTimeout(f"Render of {scene_class} timed out after 300s")

            if proc.returncode != 0:
                raise ManimRenderError(f"Render failed:\n{stderr.decode()}")

            # Find the output MP4
            video_dir = output_base / "videos"
            mp4s = list(video_dir.rglob(f"*.mp4"))
            if not mp4s:
                raise ManimRenderError(f"No MP4 found for {scene_class}")

            # Get the most recent MP4
            output_mp4 = max(mp4s, key=lambda p: p.stat().st_mtime)
            logger.info("scene_rendered", scene_class=scene_class, path=str(output_mp4))
            return output_mp4

        except FileNotFoundError:
            raise ManimRenderError("manim binary not found. Is manim installed?")

    async def render_all_scenes(self, script_path: str,
                                 scenes: List[ManimSceneSpec],
                                 episode_id: str) -> List[dict]:
        """Render all scenes in parallel using ThreadPoolExecutor."""
        loop = asyncio.get_event_loop()
        results = []

        with ThreadPoolExecutor(max_workers=self.settings.manim_workers) as executor:
            tasks = []
            for scene in scenes:
                task = loop.run_in_executor(
                    executor,
                    lambda s=scene: asyncio.run(self.render_scene(
                        script_path, s.scene_class_name,
                        episode_id, s.scene_number if hasattr(s, 'scene_number') else 0,
                    ))
                )
                tasks.append((scene, task))

            for scene, task in tasks:
                try:
                    path = await task
                    # Get duration via ffprobe
                    duration = await self._get_duration(str(path))
                    results.append({
                        "scene_number": scene.scene_number if hasattr(scene, 'scene_number') else 0,
                        "path": str(path),
                        "duration": duration,
                    })
                except (ManimRenderTimeout, ManimRenderError) as e:
                    logger.warning("scene_render_failed", scene=scene.scene_class_name, error=str(e))
                    results.append({
                        "scene_number": scene.scene_number if hasattr(scene, 'scene_number') else 0,
                        "path": "",
                        "duration": 0,
                        "error": str(e),
                    })

        return results

    async def _get_duration(self, video_path: str) -> float:
        """Get video duration in seconds using ffprobe."""
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_streams", "-show_format",
            video_path,
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        try:
            data = json.loads(stdout)
            return float(data.get("format", {}).get("duration", 0))
        except (json.JSONDecodeError, ValueError, TypeError):
            return 0.0