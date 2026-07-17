import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface WanPreviewProps {
  thumbnailUrl: string | null;
  isLoading: boolean;
}

export function WanPreview({ thumbnailUrl, isLoading }: WanPreviewProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Character Video</CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading && (
          <div className="flex items-center justify-center h-32 rounded-md bg-muted">
            <div className="flex flex-col items-center gap-2">
              <span className="text-2xl animate-pulse">🎥</span>
              <span className="text-xs text-muted-foreground">
                Generating character video...
              </span>
            </div>
          </div>
        )}
        {!isLoading && !thumbnailUrl && (
          <div className="flex items-center justify-center h-32 rounded-md bg-muted">
            <span className="text-xs text-muted-foreground">
              No character video yet
            </span>
          </div>
        )}
        {thumbnailUrl && (
          <div className="rounded-md overflow-hidden">
            <img
              src={thumbnailUrl}
              alt="Character video thumbnail"
              className="w-full h-auto object-cover"
            />
          </div>
        )}
      </CardContent>
    </Card>
  );
}