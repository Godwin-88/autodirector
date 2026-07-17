import type {
  EpisodeResponse,
  EpisodeListItem,
  SSEEvent,
  StageUpdateEvent,
  ScriptChunkEvent,
  VideoReadyEvent,
  ErrorEvent,
} from "@/types/episode";

const BASE_URL = "/api/v1";

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`HTTP ${response.status}: ${errorBody}`);
  }
  return response.json();
}

export async function createEpisode(
  topic: string,
  episodeNumber: number
): Promise<EpisodeResponse> {
  return fetchJSON<EpisodeResponse>(`${BASE_URL}/episodes`, {
    method: "POST",
    body: JSON.stringify({ topic, episode_number: episodeNumber }),
  });
}

export async function getEpisode(id: string): Promise<EpisodeResponse> {
  return fetchJSON<EpisodeResponse>(`${BASE_URL}/episodes/${id}`);
}

export async function listEpisodes(): Promise<{
  status: string;
  data: { episodes: EpisodeListItem[] };
  errors: string[];
  timestamp: string;
}> {
  return fetchJSON(`${BASE_URL}/episodes`);
}

export async function resumeEpisode(id: string): Promise<EpisodeResponse> {
  return fetchJSON<EpisodeResponse>(`${BASE_URL}/episodes/${id}/resume`, {
    method: "POST",
  });
}

export async function deleteEpisode(id: string): Promise<{ status: string }> {
  return fetchJSON(`${BASE_URL}/episodes/${id}`, { method: "DELETE" });
}

export type SSEEventHandler = {
  onStageUpdate?: (event: StageUpdateEvent) => void;
  onScriptChunk?: (event: ScriptChunkEvent) => void;
  onVideoReady?: (event: VideoReadyEvent) => void;
  onError?: (event: ErrorEvent) => void;
  onComplete?: () => void;
};

export function subscribeToProgress(
  episodeId: string,
  handlers: SSEEventHandler
): () => void {
  const eventSource = new EventSource(
    `${BASE_URL}/episodes/${episodeId}/progress`
  );

  eventSource.addEventListener("stage_update", (e: MessageEvent) => {
    const data = JSON.parse(e.data) as StageUpdateEvent;
    handlers.onStageUpdate?.(data);
  });

  eventSource.addEventListener("script_chunk", (e: MessageEvent) => {
    const data = JSON.parse(e.data) as ScriptChunkEvent;
    handlers.onScriptChunk?.(data);
  });

  eventSource.addEventListener("video_ready", (e: MessageEvent) => {
    const data = JSON.parse(e.data) as VideoReadyEvent;
    handlers.onVideoReady?.(data);
  });

  eventSource.addEventListener("error", (e: MessageEvent) => {
    const data = JSON.parse(e.data) as ErrorEvent;
    handlers.onError?.(data);
  });

  eventSource.addEventListener("complete", () => {
    handlers.onComplete?.();
    eventSource.close();
  });

  eventSource.onerror = () => {
    // Reconnect will happen automatically unless we close
    console.warn("SSE connection error, will retry...");
  };

  return () => {
    eventSource.close();
  };
}