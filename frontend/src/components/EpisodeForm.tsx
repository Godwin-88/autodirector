import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export type VideoGenProvider = "wan" | "cogvideox" | "colab" | "manim";

const PROVIDER_OPTIONS: { value: VideoGenProvider; label: string; hint: string }[] = [
  { value: "wan", label: "Wan + Manim", hint: "API-based (DashScope) with Manim fallback" },
  { value: "cogvideox", label: "CogVideoX", hint: "Self-hosted / Colab GPU (free)" },
  { value: "colab", label: "Colab Worker", hint: "Queue to a running Colab T4 notebook" },
  { value: "manim", label: "Manim Only", hint: "No video-gen — Manim title card only" },
];

interface EpisodeFormProps {
  onGenerate: (
    topic: string,
    episodeNumber: number,
    videoGenProvider: VideoGenProvider
  ) => void;
  disabled: boolean;
}

export function EpisodeForm({ onGenerate, disabled }: EpisodeFormProps) {
  const [topic, setTopic] = useState("");
  const [episodeNumber, setEpisodeNumber] = useState(1);
  const [videoGenProvider, setVideoGenProvider] =
    useState<VideoGenProvider>("wan");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;
    onGenerate(topic.trim(), episodeNumber, videoGenProvider);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">New Episode</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <label
              htmlFor="topic"
              className="text-sm font-medium text-foreground"
            >
              Topic
            </label>
            <Input
              id="topic"
              placeholder="e.g., Why the Normal Distribution Fails in Finance"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              disabled={disabled}
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label
              htmlFor="episode"
              className="text-sm font-medium text-foreground"
            >
              Episode Number
            </label>
            <Input
              id="episode"
              type="number"
              min={1}
              value={episodeNumber}
              onChange={(e) => setEpisodeNumber(Number(e.target.value))}
              disabled={disabled}
              className="w-32"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label
              htmlFor="video-gen-provider"
              className="text-sm font-medium text-foreground"
            >
              Video Generation Tool
            </label>
            <select
              id="video-gen-provider"
              value={videoGenProvider}
              onChange={(e) =>
                setVideoGenProvider(e.target.value as VideoGenProvider)
              }
              disabled={disabled}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {PROVIDER_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
            <p className="text-xs text-muted-foreground">
              {
                PROVIDER_OPTIONS.find((o) => o.value === videoGenProvider)
                  ?.hint
              }
            </p>
          </div>
          <Button type="submit" disabled={disabled || !topic.trim()}>
            {disabled ? "Generating..." : "Generate Episode"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}