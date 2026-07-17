from pathlib import Path
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import asyncio
from services.generation.av_aligner import AVAligner
from core.logging import get_logger

logger = get_logger("scene_syncer")


class SceneSyncer:
    def __init__(self):
        self.aligner = AVAligner()

    async def sync_all(self, scenes: List[Dict[str, str]], episode_id: str) -> List[str]:
        """Sync all scene video/audio pairs in parallel. Returns ordered list of synced paths."""
        output_dir = Path(f"./output/scenes/{episode_id}")
        output_dir.mkdir(parents=True, exist_ok=True)

        synced_paths = []
        tasks = []

        for scene in scenes:
            video = scene.get("video", "")
            audio = scene.get("audio", "")
            scene_num = scene.get("scene_number", 0)
            output_path = str(output_dir / f"scene_{scene_num}_synced.mp4")
            tasks.append(self.aligner.align(video, audio, output_path))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning("scene_sync_failed", scene=i, error=str(result))
                synced_paths.append("")
            else:
                synced_paths.append(str(result[0]))

        return synced_paths