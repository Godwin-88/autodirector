import { Separator } from "@/components/ui/separator";

export function Header() {
  return (
    <header className="border-b border-border bg-card">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
            <span className="text-lg font-bold text-primary-foreground">Q</span>
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-foreground">
              Quantifaya <span className="text-accent">AutoDirector</span>
            </h1>
            <p className="text-xs text-muted-foreground">
              Autonomous AI Showrunner
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}