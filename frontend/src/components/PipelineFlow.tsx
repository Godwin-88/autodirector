import type { PipelineStage } from "@/types/episode";
import { StageCard } from "./StageCard";

interface PipelineFlowProps {
  stages: PipelineStage[];
}

export function PipelineFlow({ stages }: PipelineFlowProps) {
  if (stages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center text-muted-foreground">
        <span className="text-3xl mb-2">🎬</span>
        <p className="text-sm">Enter a topic and generate an episode to see the pipeline in action.</p>
      </div>
    );
  }

  return (
    <div className="space-y-0">
      {stages.map((stage, index) => (
        <StageCard
          key={stage.name}
          stage={stage}
          isLast={index === stages.length - 1}
        />
      ))}
    </div>
  );
}