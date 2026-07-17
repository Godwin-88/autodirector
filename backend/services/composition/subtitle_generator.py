from pathlib import Path
from typing import List, Dict, Any
from core.logging import get_logger

logger = get_logger("subtitle_generator")

WPM = 160  # Words per minute for timing estimation


class SubtitleGenerator:
    def generate_srt(self, scenes: List[Dict[str, Any]], episode_id: str) -> str:
        """Generate SRT subtitle content from scene voiceover texts."""
        lines = []
        cue_num = 1
        current_time = 0.0

        for scene in scenes:
            text = scene.get("voiceover_text", "")
            words = len(text.split())
            duration = (words / WPM) * 60  # estimated duration in seconds

            start_ts = self._format_timestamp(current_time)
            end_ts = self._format_timestamp(current_time + duration)

            lines.append(str(cue_num))
            lines.append(f"{start_ts} --> {end_ts}")
            lines.append(text)
            lines.append("")

            current_time += duration
            cue_num += 1

        return "\n".join(lines)

    def save_srt(self, scenes: List[Dict[str, Any]], episode_id: str,
                 output_path: str) -> Path:
        """Generate and save SRT file."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        content = self.generate_srt(scenes, episode_id)
        output.write_text(content, encoding="utf-8")
        logger.info("srt_generated", path=str(output), cues=len(scenes))
        return output

    def _format_timestamp(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format: HH:MM:SS,mmm."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"