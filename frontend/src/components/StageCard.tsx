import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
import type { PipelineStage } from "@/types/episode";

interface StageCardProps {
  stage: PipelineStage;
  isLast: boolean;
}

const statusIcon = {
  pending: "⏳",
  running: "🔄",
  done: "✅",
  failed: "❌",
};

const statusBadgeVariant = {
  pending: "outline" as const,
  running: "warning" as const,
  done: "success" as const,
  failed: "destructive" as const,
};

export function StageCard({ stage, isLast }: StageCardProps) {
  const progressValue =
    stage.status === "done"
      ? 100
      : stage.status === "failed"
        ? 0
        : stage.substages.length > 0
          ? Math.round(
              (stage.substages.filter((s) => s.status === "done").length /
                stage.substages.length) *
                100
            )
          : stage.status === "running"
            ? 50
            : 0;

  return (
    <div className="relative">
      <div className="rounded-lg border bg-card p-4 shadow-sm transition-all hover:shadow-md">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="text-lg">{statusIcon[stage.status]}</span>
            <h3 className="font-semibold text-foreground">{stage.label}</h3>
          </div>
          <div className="flex items-center gap-2">
            {stage.elapsed_seconds > 0 && (
              <span className="text-xs text-muted-foreground">
                {stage.elapsed_seconds.toFixed(1)}s
              </span>
            )}
            <Badge variant={statusBadgeVariant[stage.status]}>
              {stage.status === "running"
                ? "Running"
                : stage.status === "done"
                  ? "Complete"
                  : stage.status === "failed"
                    ? "Failed"
                    : "Pending"}
            </Badge>
          </div>
        </div>

        <Progress
          value={progressValue}
          variant={stage.status === "done" ? "success" : "default"}
          className="mb-3"
        />

        {stage.substages.length > 0 && (
          <div className="space-y-1">
            {stage.substages.map((sub) => (
              <div
                key={sub.name}
                className="flex items-center gap-2 text-xs text-muted-foreground"
              >
                <span
                  className={cn(
                    "inline-block",
                    sub.status === "running" && "animate-pulse"
                  )}
                >
                  {statusIcon[sub.status]}
                </span>
                <span
                  className={cn(
                    sub.status === "running" && "text-foreground font-medium"
                  )}
                >
                  {sub.label}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {!isLast && (
        <div className="flex justify-center py-1">
          <div className="h-4 w-[2px] bg-border" />
        </div>
      )}
    </div>
  );
}