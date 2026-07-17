import json
from celery import Task
from workers.celery_app import celery_app
from core.logging import get_logger
from core.config import get_settings

logger = get_logger("tasks")


class EpisodeGraphTask(Task):
    """Base task with Redis progress publishing."""

    def __init__(self):
        self.settings = get_settings()

    def publish_progress(self, episode_id: str, phase: str, node: str,
                         progress_pct: int, message: str):
        """Publish progress event to Redis."""
        import redis as sync_redis
        try:
            r = sync_redis.from_url(self.settings.redis_url)
            r.publish(
                f"episode:{episode_id}:progress",
                json.dumps({
                    "phase": phase,
                    "node": node,
                    "progress_pct": progress_pct,
                    "message": message,
                }),
            )
        except Exception as e:
            logger.warning("publish_progress_failed", error=str(e))


@celery_app.task(bind=True, base=EpisodeGraphTask, max_retries=3)
def run_episode_graph(self, episode_id: str, topic: str,
                      episode_number: int, series: str):
    """Run the full episode generation graph."""
    from orchestration.graph import build_episode_graph
    from schemas.episode_state import EpisodeState

    logger.info("task:run_episode_graph", episode_id=episode_id, topic=topic)

    initial_state: EpisodeState = {
        "episode_id": episode_id,
        "topic": topic,
        "episode_number": episode_number,
        "series": series,
        "outline": None,
        "sources": None,
        "script": None,
        "manim_specs": None,
        "wan_prompt": None,
        "seo_metadata": None,
        "scene_video_paths": None,
        "scene_audio_paths": None,
        "scene_synced_paths": None,
        "wan_clip_path": None,
        "final_video_path": None,
        "youtube_id": None,
        "wan_fallback": False,
        "errors": [],
        "current_phase": "pending",
    }

    try:
        graph = build_episode_graph()
        config = {"configurable": {"thread_id": episode_id}}

        # Stream through graph nodes
        for event in graph.stream(initial_state, config):
            for node_name, state in event.items():
                phase = state.get("current_phase", "unknown")
                self.publish_progress(
                    episode_id, phase, node_name,
                    _get_progress_pct(phase),
                    f"Completed: {node_name}",
                )
                logger.info("graph_node_completed", node=node_name, phase=phase)

        logger.info("task:episode_graph_complete", episode_id=episode_id)

    except Exception as e:
        logger.error("task:episode_graph_failed", episode_id=episode_id, error=str(e))
        self.publish_progress(episode_id, "failed", "error", 0, str(e))
        raise


@celery_app.task(bind=True, base=EpisodeGraphTask, max_retries=3)
def upload_youtube(self, video_path: str, thumbnail_path: str,
                   seo_json: str, channel_id: str):
    """Upload video to YouTube (high priority queue)."""
    from schemas.seo import SEOMetadata
    from services.delivery.youtube_uploader import YouTubeUploader
    import json

    seo = SEOMetadata(**json.loads(seo_json))
    uploader = YouTubeUploader()
    video_id = uploader.upload(video_path, thumbnail_path, seo, channel_id)
    return video_id


def _get_progress_pct(phase: str) -> int:
    """Map phase to progress percentage."""
    mapping = {
        "pending": 0,
        "outlined": 5,
        "sourced": 10,
        "scripted": 20,
        "specs_generated": 30,
        "wan_prompted": 35,
        "seo_generated": 40,
        "audio_synthesized": 50,
        "wan_generated": 60,
        "scenes_rendered": 70,
        "av_aligned": 80,
        "composed": 90,
        "uploaded": 95,
        "delivered": 100,
        "failed": -1,
    }
    return mapping.get(phase, 0)