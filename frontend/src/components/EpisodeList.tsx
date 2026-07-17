import { cn } from "@/lib/utils";
import type { EpisodeListItem } from "@/types/episode";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface EpisodeListProps {
  episodes: EpisodeListItem[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}

const statusColor: Record<string, "default" | "secondary" | "destructive" | "success" | "warning" | "outline"> = {
  draft: "outline",
  intelligence_complete: "warning",
  awaiting_review: "warning",
  completed: "success",
  failed: "destructive",
};

export function EpisodeList({
  episodes,
  selectedId,
  onSelect,
  onDelete,
}: EpisodeListProps) {
  if (episodes.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <p className="text-sm">No episodes yet</p>
        <p className="text-xs mt-1">Create one above</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {episodes.map((ep) => (
        <div
          key={ep.id}
          className={cn(
            "flex items-center justify-between p-3 rounded-lg border cursor-pointer transition-colors",
            selectedId === ep.id
              ? "border-primary bg-primary/5"
              : "border-border hover:bg-muted/50"
          )}
          onClick={() => onSelect(ep.id)}
        >
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-mono text-muted-foreground">
                #{ep.episode_number}
              </span>
              <Badge variant={statusColor[ep.status] ?? "outline"}>
                {ep.status.replace(/_/g, " ")}
              </Badge>
            </div>
            <p className="text-sm truncate">{ep.topic}</p>
            <p className="text-xs text-muted-foreground mt-1">
              {new Date(ep.created_at).toLocaleDateString()}
            </p>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onDelete(ep.id);
            }}
            className="text-muted-foreground hover:text-destructive"
          >
            ×
          </Button>
        </div>
      ))}
    </div>
  );
}