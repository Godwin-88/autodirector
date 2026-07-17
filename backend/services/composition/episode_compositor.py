import asyncio
import json
from pathlib import Path
from typing import List
from core.logging import get_logger

logger = get_logger("episode_compositor")


class EpisodeCompositor:
    async def compose(self, episode_id: str, wan_clip_path: str,
                      synced_scene_paths: List[str],
                      brand_intro_path: str = "",
                      brand_outro_path: str = "",
                      output_path: str = "") -> Path:
        """Compose final episode by concatenating all clips."""
        output = Path(output_path or f"./output/episodes/{episode_id}/quantifaya_ep_final.mp4")
        output.parent.mkdir(parents=True, exist_ok=True)

        # Build concat manifest
        manifest_path = output.parent / "manifest.txt"
        with open(manifest_path, "w") as f:
            if brand_intro_path and Path(brand_intro_path).exists():
                f.write(f"file '{Path(brand_intro_path).resolve()}'\n")
            if wan_clip_path and Path(wan_clip_path).exists():
                f.write(f"file '{Path(wan_clip_path).resolve()}'\n")
            for scene_path in synced_scene_paths:
                if scene_path and Path(scene_path).exists():
                    f.write(f"file '{Path(scene_path).resolve()}'\n")
            if brand_outro_path and Path(brand_outro_path).exists():
                f.write(f"file '{Path(brand_outro_path).resolve()}'\n")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(manifest_path),
            "-c", "copy",
            str(output),
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()

        # Verify output
        info = await self._get_video_info(str(output))
        logger.info("episode_composed", path=str(output), **info)
        return output

    async def _get_video_info(self, path: str) -> dict:
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", path]
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        try:
            data = json.loads(stdout)
            fmt = data.get("format", {})
            streams = data.get("streams", [])
            video = next((s for s in streams if s.get("codec_type") == "video"), {})
            return {
                "width": video.get("width"),
                "height": video.get("height"),
                "fps": eval(video.get("r_frame_rate", "0/1")) if "/" in video.get("r_frame_rate", "") else 0,
                "duration": float(fmt.get("duration", 0)),
                "size_mb": round(float(fmt.get("size", 0)) / (1024 * 1024), 2),
            }
        except (json.JSONDecodeError, ValueError, TypeError):
            return {"error": "could not probe"}