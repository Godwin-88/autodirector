import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface VideoPlayerProps {
  videoUrl: string | null;
  isReady: boolean;
}

export function VideoPlayer({ videoUrl, isReady }: VideoPlayerProps) {
  if (!isReady && !videoUrl) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Final Episode</CardTitle>
      </CardHeader>
      <CardContent>
        {isReady && videoUrl ? (
          <video
            controls
            className="w-full rounded-md"
            preload="metadata"
          >
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        ) : (
          <div className="flex items-center justify-center h-32 rounded-md bg-muted">
            <div className="flex flex-col items-center gap-2">
              <span className="text-2xl animate-pulse">⏳</span>
              <span className="text-xs text-muted-foreground">
                Composition in progress...
              </span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}