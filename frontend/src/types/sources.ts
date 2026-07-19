export interface SourceDocument {
  id: string;
  title: string;
  authors: string | null;
  year: number | null;
  source_type: 'url' | 'pdf' | 'memgraph' | 'manual';
  origin_url: string | null;
  file_path: string | null;
  chunk_count: number;
  status: 'pending' | 'chunked' | 'embedded' | 'failed';
  ingested_at: string | null;
  metadata?: Record<string, unknown>;
}

export interface SourceChunk {
  id: string;
  chunk_index: number;
  text: string;
  token_count: number | null;
  created_at: string | null;
}

export interface SourceSearchResult {
  chunk_id: string;
  text: string;
  title: string;
  authors: string | null;
  year: number | null;
  source_type: string;
  origin_url: string | null;
  distance: number;
}

export interface IngestProgressEvent {
  task_id: string;
  stage: 'pending' | 'scraping' | 'extracting' | 'chunking' | 'embedding' | 'done' | 'failed';
  progress: number;
  message: string;
  timestamp: string;
}

export interface MemgraphConcept {
  name: string;
  definition: string | null;
  equations: string[];
  score: number;
}

export interface MemgraphConceptDetail {
  found: boolean;
  name: string;
  definition: string | null;
  equations: string[];
  relationships: Array<{
    type: string;
    target_name: string;
    target_labels: string[];
  }>;
  subgraph: {
    nodes: Array<{ name: string; labels: string[]; definition: string | null }>;
    edges: Array<{ source: string; type: string; target: string }>;
  };
}