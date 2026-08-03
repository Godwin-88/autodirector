import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface B2Asset {
  b2_key: string;
  url: string;
  size_bytes: number;
  content_type: string;
}

interface B2Episode {
  episode_id: string;
  uploaded_at: string;
  manifest_url?: string;
  assets: {
    final_video?: B2Asset;
    thumbnail?: B2Asset;
    wan_intro?: B2Asset;
    scenes?: B2Asset[];
    audio?: B2Asset[];
  };
}

interface B2Health {
  status: string;
  bucket?: string;
  endpoint?: string;
  error?: string;
}

export default function MediaLibrary() {
  const [episodes, setEpisodes] = useState<B2Episode[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<B2Episode | null>(null);

  useEffect(() => {
    fetch("/api/v1/media/library")
      .then((r) => r.json())
      .then((data) => {
        setEpisodes(data.episodes || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-foreground">
          🗄️ Media Library
        </h2>
        <p className="text-sm text-muted-foreground mt-1">
          All generated assets stored in Backblaze B2 Cloud Storage
        </p>
      </div>

      <B2StatusBadge />

      {loading && (
        <p className="text-sm text-muted-foreground">Loading from B2...</p>
      )}

      {!loading && episodes.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-3xl mb-2">🎬</p>
            <p className="text-muted-foreground">
              No episodes in B2 yet. Generate an episode to see its assets here.
            </p>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {episodes.map((ep) => (
          <EpisodeMediaCard
            key={ep.episode_id}
            episode={ep}
            onSelect={() => setSelected(ep)}
          />
        ))}
      </div>

      {selected && (
        <MediaDetailModal
          episode={selected}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  );
}

function B2StatusBadge() {
  const [status, setStatus] = useState<B2Health | null>(null);

  useEffect(() => {
    fetch("/api/v1/media/health")
      .then((r) => r.json())
      .then(setStatus)
      .catch(() => setStatus({ status: "error", error: "unreachable" }));
  }, []);

  if (!status) return null;
  const connected = status.status === "connected";

  return (
    <Badge variant={connected ? "success" : "destructive"}>
      <span
        className={`mr-2 inline-block h-2 w-2 rounded-full ${
          connected ? "bg-green-400" : "bg-red-400"
        }`}
      />
      Backblaze B2 —{" "}
      {connected ? `Connected (${status.bucket})` : "Disconnected"}
    </Badge>
  );
}

function EpisodeMediaCard({
  episode,
  onSelect,
}: {
  episode: B2Episode;
  onSelect: () => void;
}) {
  const thumb = episode.assets?.thumbnail?.url;
  const videoUrl = episode.assets?.final_video?.url;
  const sizeGB = episode.assets?.final_video?.size_bytes
    ? (episode.assets.final_video.size_bytes / 1e9).toFixed(2)
    : null;

  return (
    <Card
      className="cursor-pointer overflow-hidden transition-colors hover:border-primary"
      onClick={onSelect}
    >
      <div className="relative aspect-video w-full bg-muted">
        {thumb ? (
          <img
            src={thumb}
            alt=""
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-4xl">
            🎬
          </div>
        )}
        {videoUrl && (
          <span className="absolute bottom-2 right-2 rounded bg-black/80 px-1.5 py-0.5 text-xs text-foreground">
            ▶ B2
          </span>
        )}
      </div>

      <CardContent className="p-4">
        <p className="font-semibold text-foreground">
          {episode.episode_id?.slice(0, 8)}...
        </p>
        <p className="text-xs text-muted-foreground">
          {episode.uploaded_at?.slice(0, 10)}
        </p>

        <div className="mt-3 flex flex-wrap gap-1.5">
          {episode.assets?.final_video && (
            <Badge variant="secondary">
              MP4{sizeGB ? ` · ${sizeGB} GB` : ""}
            </Badge>
          )}
          {episode.assets?.thumbnail && (
            <Badge variant="warning">Thumbnail</Badge>
          )}
          {episode.assets?.wan_intro && (
            <Badge variant="secondary">Wan Intro</Badge>
          )}
          {episode.assets?.scenes && episode.assets.scenes.length > 0 && (
            <Badge variant="secondary">
              {episode.assets.scenes.length} Scenes
            </Badge>
          )}
          {episode.assets?.audio && episode.assets.audio.length > 0 && (
            <Badge variant="secondary">
              {episode.assets.audio.length} Audio
            </Badge>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function MediaDetailModal({
  episode,
  onClose,
}: {
  episode: B2Episode;
  onClose: () => void;
}) {
  const videoUrl = episode.assets?.final_video?.url;
  const manifestUrl = episode.manifest_url;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 p-4"
      onClick={onClose}
    >
      <Card
        className="w-full max-w-2xl border-border"
        onClick={(e) => e.stopPropagation()}
      >
        <CardContent className="p-6">
          <h3 className="mb-4 text-lg font-bold text-foreground">
            Episode Assets — Backblaze B2
          </h3>

          {videoUrl && (
            <video
              controls
              className="mb-4 w-full rounded-lg"
              src={`/api/v1/media/episodes/${episode.episode_id}/stream`}
            />
          )}

          <div className="flex flex-col gap-2">
            {videoUrl && (
              <URLRow label="Final Video (B2)" url={videoUrl} />
            )}
            {episode.assets?.thumbnail?.url && (
              <URLRow label="Thumbnail (B2)" url={episode.assets.thumbnail.url} />
            )}
            {manifestUrl && (
              <URLRow label="Asset Manifest" url={manifestUrl} />
            )}
          </div>

          <Button className="mt-5" onClick={onClose}>
            Close
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

function URLRow({ label, url }: { label: string; url: string }) {
  return (
    <div className="flex items-center justify-between rounded-lg bg-muted px-3 py-2">
      <span className="text-xs text-muted-foreground">{label}</span>
      <div className="flex items-center gap-2">
        <a
          href={url}
          target="_blank"
          rel="noreferrer"
          className="text-xs text-primary hover:underline"
        >
          Open ↗
        </a>
        <Button
          variant="outline"
          size="sm"
          className="h-6 px-2 text-xs"
          onClick={() => navigator.clipboard.writeText(url)}
        >
          Copy
        </Button>
      </div>
    </div>
  );
}