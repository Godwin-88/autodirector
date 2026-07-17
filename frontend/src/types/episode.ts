export interface EpisodeResponse {
  status: string;
  data: EpisodeData;
  errors: string[];
  timestamp: string;
}

export interface EpisodeData {
  id: string;
  episode_number: number;
  topic: string;
  status: EpisodeStatus;
  script: ScriptData | null;
  seo_metadata: SEOMetadata | null;
  youtube_id: string | null;
  video_path: string | null;
  created_at: string;
  updated_at: string;
}

export type EpisodeStatus =
  | "draft"
  | "outline_generating"
  | "outline_complete"
  | "script_generating"
  | "script_complete"
  | "sources_generating"
  | "sources_complete"
  | "manim_specs_generating"
  | "manim_specs_complete"
  | "wan_prompts_generating"
  | "wan_prompts_complete"
  | "seo_generating"
  | "seo_complete"
  | "intelligence_complete"
  | "awaiting_review"
  | "generating"
  | "composing"
  | "completed"
  | "failed";

export interface ScriptData {
  scenes: SceneData[];
}

export interface SceneData {
  scene_number: number;
  title: string;
  content: string;
  stage_direction: string;
  duration_seconds: number;
}

export interface SEOMetadata {
  youtube_title: string;
  youtube_description: string;
  tags: string[];
  chapters: ChapterMark[];
}

export interface ChapterMark {
  timestamp_seconds: number;
  title: string;
}

export interface PipelineStage {
  name: string;
  label: string;
  status: "pending" | "running" | "done" | "failed";
  substages: PipelineSubstage[];
  elapsed_seconds: number;
}

export interface PipelineSubstage {
  name: string;
  label: string;
  status: "pending" | "running" | "done" | "failed";
}

export interface SSEEvent {
  event: string;
  data: string;
}

export interface StageUpdateEvent {
  stage: string;
  substage: string;
  status: "pending" | "running" | "done" | "failed";
  elapsed_seconds: number;
}

export interface ScriptChunkEvent {
  scene_index: number;
  text: string;
}

export interface VideoReadyEvent {
  url: string;
}

export interface ErrorEvent {
  stage: string;
  message: string;
}

export interface EpisodeListItem {
  id: string;
  episode_number: number;
  topic: string;
  status: EpisodeStatus;
  created_at: string;
}