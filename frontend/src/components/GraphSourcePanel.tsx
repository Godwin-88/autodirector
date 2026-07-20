import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

interface SourceEntry {
  ref_number: number;
  authors: string;
  year: number;
  title: string;
  journal_or_publisher: string;
  confidence: string;
  graph_verified: boolean;
  scene_usage_note: string;
}

interface GraphSourcePanelProps {
  sources?: SourceEntry[];
  episodeTopic?: string;
}

export function GraphSourcePanel({ sources, episodeTopic }: GraphSourcePanelProps) {
  if (!sources || sources.length === 0) {
    return (
      <Card>
        <CardHeader className="p-3">
          <CardTitle className="text-sm font-medium text-foreground">
            Sources & Knowledge Graph
          </CardTitle>
        </CardHeader>
        <CardContent className="p-3 pt-0">
          <p className="text-xs text-muted-foreground">
            No sources extracted yet. Generate an episode to see source verification status.
          </p>
        </CardContent>
      </Card>
    );
  }

  const verifiedCount = sources.filter((s) => s.graph_verified).length;
  const ingestedCount = sources.filter((s) => s.confidence === "high" && s.graph_verified).length;

  return (
    <Card>
      <CardHeader className="p-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium text-foreground">
            Sources & Knowledge Graph
          </CardTitle>
          <div className="flex items-center gap-2">
            <Badge
              variant="outline"
              className="text-[10px]"
            >
              {verifiedCount}/{sources.length} verified
            </Badge>
            <Badge
              variant="secondary"
              className="text-[10px]"
            >
              {ingestedCount} ingested
            </Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-3 pt-0 space-y-2">
        {episodeTopic && (
          <p className="text-xs text-muted-foreground">
            Topic: <span className="text-foreground font-medium">{episodeTopic}</span>
          </p>
        )}
        <Separator />
        {sources.map((source) => (
          <div
            key={source.ref_number}
            className={`rounded p-2 text-xs border-l-2 ${
              source.graph_verified
                ? "border-l-green-500 bg-green-500/5"
                : "border-l-yellow-500 bg-yellow-500/5"
            }`}
          >
            <div className="flex items-start justify-between gap-2">
              <div className="min-w-0 flex-1">
                <p className="font-medium text-foreground truncate">
                  [{source.ref_number}] {source.authors} ({source.year})
                </p>
                <p className="text-muted-foreground truncate">{source.title}</p>
                <p className="text-muted-foreground truncate">
                  {source.journal_or_publisher}
                </p>
              </div>
              <div className="flex items-center gap-1 shrink-0">
                {source.graph_verified ? (
                  <Badge
                    variant="outline"
                    className="text-[10px] text-green-500 border-green-500"
                  >
                    ✓ Graph
                  </Badge>
                ) : (
                  <Badge
                    variant="outline"
                    className="text-[10px] text-yellow-500 border-yellow-500"
                  >
                    Unverified
                  </Badge>
                )}
                <Badge
                  variant="secondary"
                  className="text-[10px]"
                >
                  {source.confidence}
                </Badge>
              </div>
            </div>
            <p className="text-muted-foreground mt-1 italic">
              {source.scene_usage_note}
            </p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}