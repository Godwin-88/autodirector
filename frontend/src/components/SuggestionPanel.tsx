import { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { getTodaySuggestion, getWeekPreview, produceEpisode, skipEpisode } from "@/api/strategy";
import type { Suggestion } from "@/types/strategy";

const DAY_COLORS: Record<string, string> = {
  monday: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  tuesday: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200",
  wednesday: "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200",
  thursday: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
  friday: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200",
  saturday: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200",
  sunday: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200",
};

function getDayColor(day: string) {
  return DAY_COLORS[day.toLowerCase()] ?? DAY_COLORS.sunday;
}

export function SuggestionPanel() {
  const [today, setToday] = useState<Suggestion | null>(null);
  const [week, setWeek] = useState<Suggestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [producing, setProducing] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const [todayRes, weekRes] = await Promise.all([
        getTodaySuggestion(),
        getWeekPreview(),
      ]);
      setToday(todayRes);
      setWeek(weekRes);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load suggestions");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleProduce = async (episodeId: string) => {
    try {
      setProducing(episodeId);
      await produceEpisode(episodeId);
      await load();
    } catch (err) {
      console.error("Failed to produce:", err);
    } finally {
      setProducing(null);
    }
  };

  const handleSkip = async (episodeId: string) => {
    try {
      await skipEpisode(episodeId);
      await load();
    } catch (err) {
      console.error("Failed to skip:", err);
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Today's Suggestion</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground animate-pulse">Loading...</p>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Today's Suggestion</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-destructive">{error}</p>
          <Button variant="outline" size="sm" className="mt-2" onClick={load}>
            Retry
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Today's Suggestion */}
      <Card
        className={today?.pillar?.color ? "border-l-4" : ""}
        style={today?.pillar?.color ? { borderLeftColor: today.pillar.color } : undefined}
      >
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">Today's Suggestion</CardTitle>
            {today?.day && (
              <Badge className={getDayColor(today.day)}>
                {today.day}
              </Badge>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {today?.suggestion ? (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <Badge style={{ backgroundColor: today.pillar?.color ?? "#888" }}>
                  {today.pillar?.code ?? "?"}
                </Badge>
                <span className="text-sm font-medium text-muted-foreground">
                  {today.pillar?.name}
                </span>
              </div>
              <p className="font-semibold">
                {today.suggestion.suggested_title ?? today.suggestion.topic}
              </p>
              <p className="text-sm text-muted-foreground">
                Episode #{today.suggestion.sequence_number}
              </p>
              <div className="flex gap-2 pt-2">
                <Button
                  size="sm"
                  onClick={() => handleProduce(today.suggestion!.id)}
                  disabled={producing === today.suggestion!.id}
                >
                  {producing === today.suggestion!.id ? "Starting..." : "Produce Now"}
                </Button>
                <Button size="sm" variant="outline" onClick={() => handleSkip(today.suggestion!.id)}>
                  Skip
                </Button>
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">
                {today?.status === "no_matching_pillar"
                  ? "No content scheduled for today"
                  : today?.status === "all_produced"
                    ? "All episodes produced! 🎉"
                    : "No suggestion available"}
              </p>
              {today?.source && (
                <p className="text-xs text-muted-foreground">Source: {today.source}</p>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Week Preview */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Week Preview</CardTitle>
        </CardHeader>
        <CardContent>
          {week.length === 0 ? (
            <p className="text-sm text-muted-foreground">No upcoming episodes scheduled</p>
          ) : (
            <div className="space-y-2">
              {week.map((day, i) => (
                <div key={i} className="flex items-center gap-3 py-1.5">
                  <Badge className={getDayColor(day.day) + " min-w-[80px] justify-center"}>
                    {day.day}
                  </Badge>
                  <div className="flex-1 min-w-0">
                    {day.suggestion ? (
                      <div className="flex items-center gap-2">
                        <span
                          className="inline-block w-2 h-2 rounded-full shrink-0"
                          style={{ backgroundColor: day.pillar?.color ?? "#888" }}
                        />
                        <span className="text-sm truncate">
                          {day.suggestion.suggested_title ?? day.suggestion.topic}
                        </span>
                      </div>
                    ) : (
                      <span className="text-sm text-muted-foreground italic">
                        Rest day / No content
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
