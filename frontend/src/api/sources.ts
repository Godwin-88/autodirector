import type { SourceDocument, SourceChunk, SourceSearchResult, MemgraphConcept, MemgraphConceptDetail } from '../types/sources';

const BASE_URL = '/api/v1';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || `HTTP ${response.status}`);
  }
  return response.json();
}

export async function ingestURL(
  url: string,
  episodeId?: string,
  manualTitle?: string,
  manualAuthors?: string,
  manualYear?: number,
): Promise<{ task_id: string; document_id: string; status: string }> {
  const response = await fetch(`${BASE_URL}/sources/url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, episode_id: episodeId, manual_title: manualTitle, manual_authors: manualAuthors, manual_year: manualYear }),
  });
  return handleResponse(response);
}

export async function ingestPDF(
  file: File,
  episodeId?: string,
  title?: string,
  authors?: string,
  year?: number,
): Promise<{ task_id: string; document_id: string; status: string }> {
  const formData = new FormData();
  formData.append('file', file);
  if (episodeId) formData.append('episode_id', episodeId);
  if (title) formData.append('title', title);
  if (authors) formData.append('authors', authors);
  if (year) formData.append('year', String(year));

  const response = await fetch(`${BASE_URL}/sources/pdf`, {
    method: 'POST',
    body: formData,
  });
  return handleResponse(response);
}

export async function listSources(
  sourceType?: string,
  status?: string,
  limit = 50,
  offset = 0,
): Promise<{ total: number; offset: number; limit: number; sources: SourceDocument[] }> {
  const params = new URLSearchParams();
  if (sourceType) params.set('source_type', sourceType);
  if (status) params.set('status', status);
  params.set('limit', String(limit));
  params.set('offset', String(offset));

  const response = await fetch(`${BASE_URL}/sources?${params}`);
  return handleResponse(response);
}

export async function getSource(id: string): Promise<SourceDocument> {
  const response = await fetch(`${BASE_URL}/sources/${id}`);
  return handleResponse(response);
}

export async function deleteSource(id: string): Promise<{ status: string; id: string }> {
  const response = await fetch(`${BASE_URL}/sources/${id}`, { method: 'DELETE' });
  return handleResponse(response);
}

export async function assignSourceToEpisode(sourceId: string, episodeId: string): Promise<{ status: string }> {
  const response = await fetch(`${BASE_URL}/sources/${sourceId}/assign?episode_id=${episodeId}`, {
    method: 'POST',
  });
  return handleResponse(response);
}

export async function getSourceChunks(
  sourceId: string,
  page = 1,
  pageSize = 20,
): Promise<{ total: number; page: number; page_size: number; chunks: SourceChunk[] }> {
  const response = await fetch(`${BASE_URL}/sources/${sourceId}/chunks?page=${page}&page_size=${pageSize}`);
  return handleResponse(response);
}

export async function searchSources(
  query: string,
  episodeId?: string,
  topK = 5,
): Promise<{ query: string; results: SourceSearchResult[] }> {
  const response = await fetch(`${BASE_URL}/sources/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, episode_id: episodeId, top_k: topK }),
  });
  return handleResponse(response);
}

// Episode-source associations
export async function listEpisodeSources(episodeId: string): Promise<{ episode_id: string; sources: SourceDocument[] }> {
  const response = await fetch(`${BASE_URL}/episodes/${episodeId}/sources`);
  return handleResponse(response);
}

export async function removeEpisodeSource(episodeId: string, sourceId: string): Promise<{ status: string }> {
  const response = await fetch(`${BASE_URL}/episodes/${episodeId}/sources/${sourceId}`, {
    method: 'DELETE',
  });
  return handleResponse(response);
}

// Memgraph endpoints
export async function checkMemgraphHealth(): Promise<{ enabled: boolean; connected: boolean }> {
  const response = await fetch(`${BASE_URL}/memgraph/health`);
  return handleResponse(response);
}

export async function getMemgraphConcept(name: string): Promise<MemgraphConceptDetail> {
  const response = await fetch(`${BASE_URL}/memgraph/concept/${encodeURIComponent(name)}`);
  return handleResponse(response);
}

export async function searchMemgraphConcepts(
  query: string,
  limit = 10,
): Promise<{ query: string; concepts: MemgraphConcept[] }> {
  const response = await fetch(`${BASE_URL}/memgraph/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, limit }),
  });
  return handleResponse(response);
}