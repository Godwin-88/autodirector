import re
import edge_tts
import asyncio
import json
from pathlib import Path
from typing import Tuple
from core.logging import get_logger

logger = get_logger("tts_synthesizer")

LATEX_TO_SPEECH = {
    r"\Delta": "Delta",
    r"\Gamma": "Gamma",
    r"\sigma": "sigma",
    r"\mu": "mu",
    r"\partial": "partial",
    r"\frac{1}{2}": "one half",
    r"\sqrt{T}": "root T",
    r"\infty": "infinity",
    r"N(d_1)": "N of d one",
    r"N(d_2)": "N of d two",
    r"\mathbb{E}": "the expected value of",
    r"\mathbb{P}": "the probability",
    r"dB": "d B",
    r"dS": "d S",
    r"dt": "d t",
    r"\Rightarrow": "which gives us",
    r"\approx": "approximately equals",
    r"\geq": "greater than or equal to",
    r"\leq": "less than or equal to",
}


class TTSSynthesizer:
    VOICE = "en-US-GuyNeural"
    RATE = "-10%"

    def preprocess(self, text: str) -> str:
        """Clean text for TTS: remove stage directions, replace LaTeX."""
        # Remove [PAUSE] markers
        text = text.replace("[PAUSE]", "")

        # Remove *italic stage directions* (but keep content between ***bold*** etc)
        text = re.sub(r'\*[^*]+\*', '', text)

        # Apply LaTeX substitutions
        for latex, speech in LATEX_TO_SPEECH.items():
            text = text.replace(latex, speech)

        # Remove inline citation tags [A1], [T2], [BS73] etc.
        text = re.sub(r'\[[A-Z0-9]+\]', '', text)

        # Remove LaTeX math delimiters
        text = text.replace("$", "").replace("$$", "")

        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    async def synthesize_scene(self, voiceover_text: str,
                                output_path: str) -> Tuple[Path, float]:
        """Synthesize TTS for a scene. Returns (path, duration_secs)."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        text = self.preprocess(voiceover_text)
        if not text.strip():
            # Create silent audio
            from pathlib import Path
            output.write_bytes(b'')
            return output, 0.0

        communicate = edge_tts.Communicate(text, voice=self.VOICE, rate=self.RATE)
        await communicate.save(str(output))

        # Get duration via ffprobe
        duration = await self._get_duration(str(output))
        logger.info("tts_synthesized", path=str(output), duration=duration, chars=len(text))
        return output, duration

    async def _get_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds using ffprobe."""
        import asyncio
        import json

        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            audio_path,
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