"""LangGraph episode generation graph definition."""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from schemas.episode_state import EpisodeState
from orchestration.nodes import (
    analyze_topic,
    extract_sources,
    generate_script,
    generate_manim_specs,
    generate_wan_prompt,
    generate_seo,
    synthesize_audio,
    generate_wan_clip,
    render_manim_scenes,
    align_av_scenes,
    compose_episode,
    upload_youtube,
    mark_complete,
    handle_error,
)
from core.config import get_settings
from core.logging import get_logger

logger = get_logger("orchestration.graph")


def build_episode_graph() -> StateGraph:
    """Build the LangGraph episode generation graph."""
    graph = StateGraph(EpisodeState)

    # Add all nodes
    graph.add_node("analyze_topic", analyze_topic)
    graph.add_node("extract_sources", extract_sources)
    graph.add_node("generate_script", generate_script)
    graph.add_node("generate_manim_specs", generate_manim_specs)
    graph.add_node("generate_wan_prompt", generate_wan_prompt)
    graph.add_node("generate_seo", generate_seo)
    graph.add_node("synthesize_audio", synthesize_audio)
    graph.add_node("generate_wan_clip", generate_wan_clip)
    graph.add_node("render_manim_scenes", render_manim_scenes)
    graph.add_node("align_av_scenes", align_av_scenes)
    graph.add_node("compose_episode", compose_episode)
    graph.add_node("upload_youtube", upload_youtube)
    graph.add_node("mark_complete", mark_complete)
    graph.add_node("handle_error", handle_error)

    # Entry point
    graph.set_entry_point("analyze_topic")

    # Intelligence phase (sequential)
    graph.add_edge("analyze_topic", "extract_sources")
    graph.add_edge("extract_sources", "generate_script")
    graph.add_edge("generate_script", "generate_manim_specs")
    graph.add_edge("generate_manim_specs", "generate_wan_prompt")
    graph.add_edge("generate_wan_prompt", "generate_seo")

    # Human review gate — interrupt before generation starts
    graph.add_edge("generate_seo", "synthesize_audio")

    # Generation phase (sequential for now, can be parallelized)
    graph.add_edge("synthesize_audio", "render_manim_scenes")
    graph.add_edge("render_manim_scenes", "generate_wan_clip")
    graph.add_edge("generate_wan_clip", "align_av_scenes")
    graph.add_edge("align_av_scenes", "compose_episode")
    graph.add_edge("compose_episode", "upload_youtube")
    graph.add_edge("upload_youtube", "mark_complete")
    graph.add_edge("mark_complete", END)

    # Error routing
    graph.add_conditional_edges(
        "handle_error",
        lambda s: END if s["errors"] else "analyze_topic"
    )

    settings = get_settings()
    checkpointer = SqliteSaver.from_conn_string("./output/graph_checkpoints.db")

    return graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["synthesize_audio"] if not settings.auto_approve else [],
    )