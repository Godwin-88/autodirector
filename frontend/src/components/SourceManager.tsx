import { useState, useCallback, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import * as sourcesApi from '../api/sources';
import type { SourceDocument, IngestProgressEvent } from '../types/sources';

const SOURCE_TYPE_COLORS: Record<string, string> = {
  url: '#4C9BE8',
  pdf: '#FF7A00',
  memgraph: '#7C3AED',
  manual: '#52C41A',
};

const STATUS_COLORS: Record<string, string> = {
  embedded: '#52C41A',
  pending: '#F0B429',
  chunked: '#4C9BE8',
  failed: '#FF4D4F',
};

export function SourceManager() {
  const [sources, setSources] = useState<SourceDocument[]>([]);
  const [totalSources, setTotalSources] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filterType, setFilterType] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // URL ingestion state
  const [urlInput, setUrlInput] = useState('');
  const [urlEpisodeId, setUrlEpisodeId] = useState('');
  const [ingesting, setIngesting] = useState(false);
  const [ingestProgress, setIngestProgress] = useState<IngestProgressEvent | null>(null);

  // PDF ingestion state
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [pdfTitle, setPdfTitle] = useState('');
  const [pdfAuthors, setPdfAuthors] = useState('');
  const [pdfYear, setPdfYear] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Memgraph state
  const [memgraphEnabled, setMemgraphEnabled] = useState<boolean | null>(null);
  const [conceptSearch, setConceptSearch] = useState('');

  const loadSources = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await sourcesApi.listSources(filterType || undefined);
      setSources(data.sources);
      setTotalSources(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load sources');
    } finally {
      setLoading(false);
    }
  }, [filterType]);

  useEffect(() => {
    loadSources();
  }, [loadSources]);

  useEffect(() => {
    sourcesApi.checkMemgraphHealth().then(h => setMemgraphEnabled(h.enabled && h.connected)).catch(() => setMemgraphEnabled(false));
  }, []);

  const handleURLIngest = async () => {
    if (!urlInput.trim()) return;
    setIngesting(true);
    setIngestProgress({ task_id: '', stage: 'pending', progress: 0, message: 'Starting...', timestamp: '' });
    try {
      const result = await sourcesApi.ingestURL(urlInput.trim(), urlEpisodeId || undefined);
      setIngestProgress({ task_id: result.task_id, stage: 'done', progress: 100, message: `Ingested: ${result.document_id}`, timestamp: '' });
      setUrlInput('');
      setUrlEpisodeId('');
      loadSources();
    } catch (err) {
      setIngestProgress({ task_id: '', stage: 'failed', progress: 0, message: err instanceof Error ? err.message : 'Failed', timestamp: '' });
    } finally {
      setIngesting(false);
    }
  };

  const handlePDFSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setPdfFile(file);
      if (!pdfTitle) setPdfTitle(file.name.replace(/\.pdf$/i, ''));
    }
  };

  const handlePDFDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
      if (!pdfTitle) setPdfTitle(file.name.replace(/\.pdf$/i, ''));
    }
  };

  const handlePDFIngest = async () => {
    if (!pdfFile) return;
    setIngesting(true);
    setIngestProgress({ task_id: '', stage: 'extracting', progress: 10, message: 'Uploading PDF...', timestamp: '' });
    try {
      const result = await sourcesApi.ingestPDF(
        pdfFile,
        urlEpisodeId || undefined,
        pdfTitle || undefined,
        pdfAuthors || undefined,
        pdfYear ? parseInt(pdfYear) : undefined,
      );
      setIngestProgress({ task_id: result.task_id, stage: 'done', progress: 100, message: `Ingested: ${result.document_id}`, timestamp: '' });
      setPdfFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      loadSources();
    } catch (err) {
      setIngestProgress({ task_id: '', stage: 'failed', progress: 0, message: err instanceof Error ? err.message : 'Failed', timestamp: '' });
    } finally {
      setIngesting(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await sourcesApi.deleteSource(id);
      loadSources();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Delete failed');
    }
  };

  const filteredSources = searchQuery
    ? sources.filter(s =>
        s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (s.authors || '').toLowerCase().includes(searchQuery.toLowerCase())
      )
    : sources;

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm">
          {error}
          <button onClick={() => setError(null)} className="ml-2 underline">Dismiss</button>
        </div>
      )}

      {/* Two-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Input Panel */}
        <div className="space-y-6">
          <Card className="p-4 bg-[#161B22] border-[#30363D]">
            <h3 className="text-base font-semibold text-[#E6EDF3] mb-3">Add Source URL</h3>
            <div className="space-y-2">
              <Input
                type="url"
                placeholder="https://arxiv.org/abs/1234.5678 or any accessible URL"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                className="bg-[#0D1117] border-[#30363D] text-[#E6EDF3]"
              />
              <Input
                placeholder="Episode ID (optional — assign to specific episode)"
                value={urlEpisodeId}
                onChange={(e) => setUrlEpisodeId(e.target.value)}
                className="bg-[#0D1117] border-[#30363D] text-[#E6EDF3]"
              />
              <Button
                onClick={handleURLIngest}
                disabled={ingesting || !urlInput.trim()}
                className="w-full bg-[#7C3AED] hover:bg-[#6D28D9] text-white"
              >
                {ingesting ? 'Ingesting...' : 'Ingest URL'}
              </Button>
            </div>
          </Card>

          <Card className="p-4 bg-[#161B22] border-[#30363D]">
            <h3 className="text-base font-semibold text-[#E6EDF3] mb-3">Upload PDF</h3>
            <div
              className="border-2 border-dashed border-[#7C3AED] rounded-lg p-6 text-center cursor-pointer hover:border-[#9D4EDD] transition-colors"
              onDrop={handlePDFDrop}
              onDragOver={(e) => e.preventDefault()}
              onClick={() => fileInputRef.current?.click()}
            >
              {pdfFile ? (
                <p className="text-[#E6EDF3]">{pdfFile.name} ({(pdfFile.size / 1024 / 1024).toFixed(1)} MB)</p>
              ) : (
                <p className="text-[#8B949E]">
                  Drop PDF here or <span className="text-[#7C3AED] underline cursor-pointer">browse</span>
                </p>
              )}
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handlePDFSelect}
                className="hidden"
              />
            </div>
            {pdfFile && (
              <div className="mt-3 space-y-2">
                <Input
                  placeholder="Title (auto-detected)"
                  value={pdfTitle}
                  onChange={(e) => setPdfTitle(e.target.value)}
                  className="bg-[#0D1117] border-[#30363D] text-[#E6EDF3]"
                />
                <Input
                  placeholder="Authors (e.g. Black, F. & Scholes, M.)"
                  value={pdfAuthors}
                  onChange={(e) => setPdfAuthors(e.target.value)}
                  className="bg-[#0D1117] border-[#30363D] text-[#E6EDF3]"
                />
                <Input
                  placeholder="Year"
                  type="number"
                  value={pdfYear}
                  onChange={(e) => setPdfYear(e.target.value)}
                  className="bg-[#0D1117] border-[#30363D] text-[#E6EDF3]"
                />
                <Button
                  onClick={handlePDFIngest}
                  disabled={ingesting}
                  className="w-full bg-[#FF7A00] hover:bg-[#E66900] text-white"
                >
                  {ingesting ? 'Uploading & Ingesting...' : 'Upload & Ingest PDF'}
                </Button>
              </div>
            )}
          </Card>

          {/* Memgraph Status */}
          <Card className="p-4 bg-[#161B22] border-[#30363D]">
            <h3 className="text-base font-semibold text-[#E6EDF3] mb-3">Memgraph Knowledge Graph</h3>
            <div className="flex items-center gap-2 mb-3">
              <span className={`w-2 h-2 rounded-full ${memgraphEnabled ? 'bg-[#52C41A]' : 'bg-[#FF4D4F]'}`} />
              <span className="text-sm text-[#8B949E]">
                {memgraphEnabled === null ? 'Checking...' : memgraphEnabled ? 'Connected' : 'Disabled'}
              </span>
            </div>
            {!memgraphEnabled && (
              <p className="text-xs text-[#8B949E]">
                Set MEMGRAPH_ENABLED=true and configure MEMGRAPH_URI to enable
              </p>
            )}
            {memgraphEnabled && (
              <div className="space-y-2">
                <Input
                  placeholder="Search concepts..."
                  value={conceptSearch}
                  onChange={(e) => setConceptSearch(e.target.value)}
                  className="bg-[#0D1117] border-[#30363D] text-[#E6EDF3]"
                />
              </div>
            )}
          </Card>
        </div>

        {/* Right: Source Library */}
        <div className="space-y-3">
          <div className="flex items-center gap-2 mb-3">
            <Input
              placeholder="Search ingested sources..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-[#161B22] border-[#30363D] text-[#E6EDF3] flex-1"
            />
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="bg-[#161B22] border-[#30363D] text-[#E6EDF3] rounded-md px-3 py-2 text-sm"
            >
              <option value="">All types</option>
              <option value="url">URLs</option>
              <option value="pdf">PDFs</option>
              <option value="memgraph">Knowledge Graph</option>
            </select>
          </div>

          {loading && <p className="text-[#8B949E] text-center py-8">Loading sources...</p>}

          {!loading && filteredSources.length === 0 && (
            <p className="text-[#8B949E] text-center py-8">
              {searchQuery || filterType ? 'No matching sources found.' : 'No sources ingested yet. Add a URL or upload a PDF.'}
            </p>
          )}

          {ingestProgress && ingestProgress.stage !== 'done' && (
            <Card className="p-3 bg-[#161B22] border-[#30363D]">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs text-[#8B949E] capitalize">{ingestProgress.stage}</span>
                <span className="text-xs text-[#8B949E]">{ingestProgress.progress}%</span>
              </div>
              <Progress value={ingestProgress.progress} className="h-1" />
              <p className="text-xs text-[#E6EDF3] mt-1">{ingestProgress.message}</p>
            </Card>
          )}

          <div className="space-y-2 max-h-[600px] overflow-y-auto">
            {filteredSources.map((source) => (
              <Card key={source.id} className="p-3 bg-[#161B22] border-[#30363D] hover:border-[#7C3AED] transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-medium text-[#E6EDF3] truncate">{source.title}</h4>
                    <p className="text-xs text-[#8B949E] mt-1">
                      {source.authors && <span>{source.authors}{source.year ? ` (${source.year})` : ''} · </span>}
                      <span>{source.chunk_count} chunks</span>
                    </p>
                  </div>
                  <div className="flex items-center gap-2 ml-2">
                    <Badge
                      style={{
                        backgroundColor: `${SOURCE_TYPE_COLORS[source.source_type]}22`,
                        color: SOURCE_TYPE_COLORS[source.source_type],
                        borderColor: `${SOURCE_TYPE_COLORS[source.source_type]}44`,
                      }}
                      className="text-xs"
                    >
                      {source.source_type}
                    </Badge>
                    <Badge
                      style={{
                        backgroundColor: `${STATUS_COLORS[source.status]}22`,
                        color: STATUS_COLORS[source.status],
                        borderColor: `${STATUS_COLORS[source.status]}44`,
                      }}
                      className="text-xs"
                    >
                      {source.status}
                    </Badge>
                  </div>
                </div>
                {source.origin_url && (
                  <p className="text-xs text-[#7C3AED] truncate mt-1">{source.origin_url}</p>
                )}
                <div className="flex gap-2 mt-2">
                  <Button
                    onClick={() => handleDelete(source.id)}
                    variant="ghost"
                    className="text-xs text-[#FF4D4F] hover:text-[#FF4D4F] hover:bg-red-900/20 px-2 py-1 h-auto"
                  >
                    Delete
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export function EpisodeSourcePanel({ episodeId }: { episodeId: string }) {
  const [sources, setSources] = useState<SourceDocument[]>([]);

  useEffect(() => {
    if (episodeId) {
      sourcesApi.listEpisodeSources(episodeId).then(data => setSources(data.sources)).catch(() => {});
    }
  }, [episodeId]);

  if (!episodeId) return null;

  return (
    <Card className="p-4 bg-[#161B22] border-[#30363D] mt-4">
      <h3 className="text-base font-semibold text-[#E6EDF3] mb-3">Episode Sources ({sources.length})</h3>
      {sources.length === 0 ? (
        <p className="text-sm text-[#8B949E]">No sources assigned to this episode.</p>
      ) : (
        <div className="space-y-2">
          {sources.map(source => (
            <div key={source.id} className="flex items-center justify-between p-2 bg-[#0D1117] rounded">
              <div className="min-w-0 flex-1">
                <p className="text-sm text-[#E6EDF3] truncate">{source.title}</p>
                <p className="text-xs text-[#8B949E]">{source.chunk_count} chunks · {source.source_type}</p>
              </div>
              <Badge
                style={{
                  backgroundColor: `${STATUS_COLORS[source.status]}22`,
                  color: STATUS_COLORS[source.status],
                }}
                className="text-xs ml-2"
              >
                {source.status}
              </Badge>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}