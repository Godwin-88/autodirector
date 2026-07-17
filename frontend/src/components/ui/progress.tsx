import * as React from "react";
import { cn } from "@/lib/utils";

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number;
  variant?: "default" | "success";
}

const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value = 0, variant = "default", ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "relative h-2 w-full overflow-hidden rounded-full bg-secondary",
          className
        )}
        {...props}
      >
        <div
          className={cn(
            "h-full w-full flex-1 transition-all duration-500",
            variant === "default" && "bg-primary",
            variant === "success" && "bg-green-500"
          )}
          style={{ transform: `translateX(-${100 - Math.min(value, 100)}%)` }}
        />
      </div>
    );
  }
);
Progress.displayName = "Progress";

export { Progress };