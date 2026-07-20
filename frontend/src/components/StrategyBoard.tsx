import { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { getPillars, getPillarDetail } from "@/api/strategy";
import type { Pillar, PlannedEpisode } from "@/types/strategy";

const DAY_ORDER = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];

function PillarProgress({ produced, total }: { produced: number; total: number }) {
  const pct = total > 0 ? Math.round((produced / total) * 100) : 0;
  return (
    <div className="flex items-center gap-2">
      <Progress value={pct} className="h-2 flex-1" />
      <span className="text-xs text-muted-foreground whitespace-nowrap">
        {produced}/{total}
      </span>
    </div>
  );
}

function PillarCard({
  pillar,
  produced,
  total,
  onSelect,
  isSelected,
}: {
  pillar: Pillar;
  produced: number;
  total: number;
  onSelect: (id: string) => void;
  isSelected: boolean;
}) {
  return (
    <Card
      className={`cursor-pointer transition-all hover:shadow-md ${isSelected ? "ring-2 ring-primary" : ""}`}
      style={{ borderLeftColor: pillar.color, borderLeftWidth: 4 }}
      onClick={() => onSelect(pillar.id)}
    >
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <Badge style={{ backgroundColor: pillar.color }}>{pillar.code}</Badge>
          <span className="text-xs text-muted-foreground capitalize">{pillar.publish_day}</span>
        </div>
        <CardTitle className="text-sm mt-2">{pillar.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <PillarProgress produced={produced} total={total} />
      </CardContent>
    </Card>
  );
}

function EpisodeRow({
  episode,
  pillarColor,
}: {
  episode: PlannedEpisode;
  pillarColor: string;
}) {
  const statusColors: Record<string, string> = {
    planned: "bg-gray-200 dark:bg-gray-700",
    scheduled: "bg-blue-200 dark:bg-blue-800",
    in_production: "bg-amber-200 dark:bg-amber-800",
    produced: "bg-emerald-200 dark:bg-emerald-800",
    skipped: "bg-red-200 dark:bg-red-800",
  };

  return (
    <div className="flex items-center gap-3 py-2 px-3 rounded-lg hover:bg-accent/50 transition-colors">
      <span
        className={`inline-block w-2 h-2 rounded-full shrink-0 ${statusColors[episode.status] ?? "bg-gray-300"}`}
        style={{ backgroundColor: episode.status === "planned" ? pillarColor : undefined }}
      />
      <span className="text-xs text-muted-foreground w-8 shrink-0">
        #{episode.sequence_number}
      </span>
      <span className="text-sm flex-1 truncate">
        {episode.suggested_title ?? episode.topic}
      </span>
      <Badge variant="outline" className="text-[10px] capitalize">
        {episode.status.replace("_", " ")}
      </Badge>
    </div>
  );
}

export function StrategyBoard() {
  const [pillars, setPillars] = useState<Pillar[]>([]);
  const [selectedPillarId, setSelectedPillarId] = useState<string | null>(null);
  const [pillarDetail, setPillarDetail] = useState<{
    pillar: Pillar;
    episodes: PlannedEpisode[];
    produced_count: number;
    total_count: number;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);

  const loadPillars = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getPillars();
      setPillars(data);
    } catch (err) {
      console.error("Failed to load pillars:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadPillars();
  }, [loadPillars]);

  const handleSelectPillar = useCallback(async (id: string) => {
    setSelectedPillarId(id);
    setDetailLoading(true);
    try {
      const data = await getPillarDetail(id);
      setPillarDetail(data);
    } catch (err) {
      console.error("Failed to load pillar detail:", err);
    } finally {
      setDetailLoading(false);
    }
  }, []);

  // Compute produced/total per pillar (we don't have per-pillar endpoint for all, just detail)
  // For the overview, we'll use the detail when selected

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Pillar Overview */}
      <div className="lg:col-span-1 space-y-4">
        <h3 className="text-sm font-semibold text-foreground">Content Pillars</h3>
        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="h-24 bg-muted animate-pulse rounded-lg" />
            ))}
          </div>
        ) : (
          <div className="space-y-3">
            {pillars
              .sort((a, b) => DAY_ORDER.indexOf(a.publish_day) - DAY_ORDER.indexOf(b.publish_day))
              .map((p) => (
                <PillarCard
                  key={p.id}
                  pillar={p}
                  produced={0}
                  total={0}
                  onSelect={handleSelectPillar}
                  isSelected={selectedPillarId === p.id}
                />
              ))}
          </div>
        )}
      </div>

      {/* Episode Detail */}
      <div className="lg:col-span-2">
        {selectedPillarId && pillarDetail ? (
          <Card>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <Badge style={{ backgroundColor: pillarDetail.pillar.color }}>
                      {pillarDetail.pillar.code}
                    </Badge>
                    <span className="text-sm text-muted-foreground capitalize">
                      {pillarDetail.pillar.publish_day}
                    </span>
                  </div>
                  <CardTitle className="text-lg">{pillarDetail.pillar.name}</CardTitle>
                  {pillarDetail.pillar.description && (
                    <p className="text-sm text-muted-foreground mt-1">
                      {pillarDetail.pillar.description}
                    </p>
                  )}
                </div>
                <div className="text-right">
                  <PillarProgress
                    produced={pillarDetail.produced_count}
                    total={pillarDetail.total_count}
                  />
                </div>
              </div>
            </CardHeader>
            <CardContent className="max-h-[600px] overflow-y-auto">
              {detailLoading ? (
                <div className="space-y-2">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <div key={i} className="h-10 bg-muted animate-pulse rounded-lg" />
                  ))}
                </div>
              ) : (
                <div className="divide-y">
                  {pillarDetail.episodes.map((ep) => (
                    <EpisodeRow
                      key={ep.id}
                      episode={ep}
                      pillarColor={pillarDetail.pillar.color}
                    />
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-muted-foreground">
                Select a pillar from the left to view its episodes
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
