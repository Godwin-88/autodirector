import { useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { SceneData } from "@/types/episode";

interface ScriptPreviewProps {
  scenes: SceneData[];
  streamingText?: string;
}

export function ScriptPreview({ scenes, streamingText }: ScriptPreviewProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [scenes, streamingText]);

  if (scenes.length === 0 && !streamingText) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Script Preview</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground italic">
            Script will appear here as scenes are generated...
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Script Preview</CardTitle>
      </CardHeader>
      <CardContent>
        <div
          ref={scrollRef}
          className="script-scroll max-h-96 overflow-y-auto rounded-md bg-muted p-4 font-mono text-xs leading-relaxed"
        >
          {scenes.map((scene) => (
            <div key={scene.scene_number} className="mb-4 last:mb-0">
              <div className="text-accent font-semibold mb-1">
                [SCENE {scene.scene_number}] — {scene.title}
                <span className="text-muted-foreground ml-2">
                  ({scene.duration_seconds}s)
                </span>
              </div>
              <div className="text-muted-foreground italic mb-1">
                {scene.stage_direction}
              </div>
              <div className="text-foreground">{scene.content}</div>
            </div>
          ))}
          {streamingText && (
            <div className="text-primary animate-pulse">
              {streamingText}
              <span className="inline-block w-1 h-4 bg-primary ml-0.5 animate-pulse" />
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}