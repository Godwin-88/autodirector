import type { Pillar, PlannedEpisode, Suggestion } from "../types/strategy";

const BASE = "http://localhost:8000/api/v1/strategy";

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function getTodaySuggestion(series = "quantifaya"): Promise<Suggestion> {
  return fetchJson<Suggestion>(`${BASE}/today?series=${series}`);
}

export async function getWeekPreview(series = "quantifaya"): Promise<Suggestion[]> {
  return fetchJson<Suggestion[]>(`${BASE}/week?series=${series}`);
}

export async function getPillars(series = "quantifaya"): Promise<Pillar[]> {
  return fetchJson<Pillar[]>(`${BASE}/pillars?series=${series}`);
}

export async function getPillarDetail(pillarId: string): Promise<{
  pillar: Pillar;
  episodes: PlannedEpisode[];
  produced_count: number;
  total_count: number;
}> {
  return fetchJson(`${BASE}/pillars/${pillarId}`);
}

export async function getEpisodes(pillarId?: string, status?: string): Promise<PlannedEpisode[]> {
  const params = new URLSearchParams();
  if (pillarId) params.set("pillar_id", pillarId);
  if (status) params.set("status", status);
  const qs = params.toString();
  return fetchJson<PlannedEpisode[]>(`${BASE}/episodes${qs ? `?${qs}` : ""}`);
}

export async function createEpisode(pillarId: string, topic: string, suggestedTitle?: string) {
  return fetchJson(`${BASE}/episodes`, {
    method: "POST",
    body: JSON.stringify({ pillar_id: pillarId, topic, suggested_title: suggestedTitle }),
  });
}

export async function skipEpisode(episodeId: string) {
  return fetchJson(`${BASE}/episodes/${episodeId}/skip`, { method: "POST" });
}

export async function produceEpisode(episodeId: string, autoApprove = false) {
  return fetchJson(`${BASE}/episodes/${episodeId}/produce`, {
    method: "POST",
    body: JSON.stringify({ auto_approve: autoApprove }),
  });
}

export async function reorderEpisodes(pillarId: string, episodeIds: string[]) {
  return fetchJson(`${BASE}/episodes/reorder`, {
    method: "POST",
    body: JSON.stringify({ pillar_id: pillarId, episode_ids: episodeIds }),
  });
}

export async function overrideSchedule(targetDate: string, plannedEpisodeId: string, reason?: string) {
  return fetchJson(`${BASE}/schedule/${targetDate}/override`, {
    method: "POST",
    body: JSON.stringify({ planned_episode_id: plannedEpisodeId, reason }),
  });
}

export async function getCalendar(series = "quantifaya", weeks = 4) {
  return fetchJson(`${BASE}/calendar?series=${series}&weeks=${weeks}`);
}