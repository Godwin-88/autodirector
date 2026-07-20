import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import type { SceneData } from "@/types/episode";

/** Beat-level detail shown inside a scene card */
interface BeatDetail {
  beat_id: string;
  narration_text: string;
  function: string;
  word_count: number;
  audio_duration_secs: number;
  animation_budget_secs: number;
  wait_secs: number;
}

interface BeatEditorProps {
  scenes: SceneData[];
  beats?: Record<number, BeatDetail[]>;
  streamingText?: string;
}

export function BeatEditor({ scenes, beats, streamingText }: BeatEditorProps) {
  const [expandedScene, setExpandedScene] = useState<number | null>(null);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-foreground">
          Script & Beat Timing
        </h3>
        {beats && (
          <Badge variant="outline" className="text-xs">
            Beat-aware timing active
          </Badge>
        )}
      </div>

      {scenes.length === 0 && streamingText && (
        <Card className="border-orange-500/30">
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground whitespace-pre-wrap font-mono">
              {streamingText}
            </p>
          </CardContent>
        </Card>
      )}

      {scenes.map((scene) => {
        const isExpanded = expandedScene === scene.scene_number;
        const sceneBeats = beats?.[scene.scene_number];

        return (
          <Card
            key={scene.scene_number}
            className="border-l-4 border-l-blue-500/50 cursor-pointer hover:bg-muted/30 transition-colors"
            onClick={() =>
              setExpandedScene(isExpanded ? null : scene.scene_number)
            }
          >
            <CardHeader className="p-3 pb-0">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm font-medium text-foreground flex items-center gap-2">
                  <span className="text-blue-400">Scene {scene.scene_number}</span>
                  <span className="text-muted-foreground font-normal">
                    {scene.title}
                  </span>
                </CardTitle>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="text-xs">
                    {scene.duration_seconds}s
                  </Badge>
                  {sceneBeats && (
                    <Badge variant="outline" className="text-xs">
                      {sceneBeats.length} beats
                    </Badge>
                  )}
                </div>
              </div>
            </CardHeader>

            {isExpanded && (
              <CardContent className="p-3 pt-2 space-y-3">
                <Separator />

                {/* Full voiceover */}
                <div>
                  <p className="text-xs text-muted-foreground mb-1 font-medium">
                    Voiceover
                  </p>
                  <p className="text-sm text-foreground whitespace-pre-wrap font-mono leading-relaxed">
                    {scene.content}
                  </p>
                </div>

                {/* Stage directions */}
                {scene.stage_direction && (
                  <div>
                    <p className="text-xs text-muted-foreground mb-1 font-medium">
                      Stage Direction
                    </p>
                    <p className="text-xs text-orange-400 italic">
                      {scene.stage_direction}
                    </p>
                  </div>
                )}

                {/* Beat-level timing breakdown */}
                {sceneBeats && sceneBeats.length > 0 && (
                  <div>
                    <p className="text-xs text-muted-foreground mb-2 font-medium">
                      Beat Timing (word-proportional)
                    </p>
                    <div className="space-y-1.5">
                      {sceneBeats.map((beat) => (
                        <div
                          key={beat.beat_id}
                          className="flex items-center gap-3 bg-muted/50 rounded p-2 text-xs"
                        >
                          <Badge
                            variant="outline"
                            className="text-[10px] px-1.5 py-0 min-w-[2rem] justify-center"
                          >
                            {beat.beat_id}
                          </Badge>
                          <Badge
                            variant="secondary"
                            className="text-[10px] px-1.5 py-0"
                          >
                            {beat.function}
                          </Badge>
                          <span className="text-muted-foreground">
                            {beat.word_count}w
                          </span>
                          <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                            <div
                              className="h-full bg-blue-500 rounded-full"
                              style={{
                                width: `${Math.min(
                                  100,
                                  (beat.animation_budget_secs /
                                    Math.max(beat.audio_duration_secs, 1)) *
                                    100
                                )}%`,
                              }}
                            />
                          </div>
                          <span className="text-muted-foreground font-mono w-20 text-right">
                            {beat.audio_duration_secs.toFixed(1)}s
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            )}
          </Card>
        );
      })}
    </div>
  );
}