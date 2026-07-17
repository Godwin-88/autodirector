import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface EpisodeFormProps {
  onGenerate: (topic: string, episodeNumber: number) => void;
  disabled: boolean;
}

export function EpisodeForm({ onGenerate, disabled }: EpisodeFormProps) {
  const [topic, setTopic] = useState("");
  const [episodeNumber, setEpisodeNumber] = useState(1);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;
    onGenerate(topic.trim(), episodeNumber);
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
          <Button type="submit" disabled={disabled || !topic.trim()}>
            {disabled ? "Generating..." : "Generate Episode"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}