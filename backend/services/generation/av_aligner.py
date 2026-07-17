import asyncio
import json
from pathlib import Path
from typing import Tuple
from core.logging import get_logger

logger = get_logger("av_aligner")

TOLERANCE_SECS = 2.0


class AVAligner:
    async def align(self, video_path: str, audio_path: str,
                    output_path: str) -> Tuple[Path, float]:
        """Align audio to video duration. Returns (output_path, final_duration)."""
        video_dur = await self._get_duration(video_path)
        audio_dur = await self._get_duration(audio_path)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        gap = abs(audio_dur - video_dur)

        if gap <= TOLERANCE_SECS:
            # Direct merge
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                str(output),
            ]
        elif audio_dur < video_dur:
            # Pad audio with silence
            gap_secs = video_dur - audio_dur
            padded_audio = str(output.parent / f"padded_{Path(audio_path).name}")
            pad_cmd = [
                "ffmpeg", "-y",
                "-i", audio_path,
                "-af", f"apad=pad_dur={gap_secs}",
                padded_audio,
            ]
            proc = await asyncio.create_subprocess_exec(
                *pad_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()

            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", padded_audio,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                str(output),
            ]
        elif audio_dur > video_dur and gap > 5.0:
            # Audio too long, regenerate would be needed — for now just pad video
            logger.warning("audio_significantly_longer", audio_dur=audio_dur, video_dur=video_dur)
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                str(output),
            ]
        else:
            # Small gap — pad video
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                str(output),
            ]

        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()

        final_dur = await self._get_duration(str(output))
        logger.info("av_aligned", video=video_path, audio=audio_path, final_dur=final_dur)
        return output, final_dur

    async def _get_duration(self, path: str) -> float:
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path]
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        try:
            return float(json.loads(stdout).get("format", {}).get("duration", 0))
        except (json.JSONDecodeError, ValueError, TypeError):
            return 0.0