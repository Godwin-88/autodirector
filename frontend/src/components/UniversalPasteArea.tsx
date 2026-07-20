import { useState, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { classifyPaste, ingestFromUrl } from "@/api/sources";
import type { MemgraphConcept } from "@/types/sources";

type ClassificationResult = {
  source_type: string;
  confidence: number;
  content_preview: string;
  action: string;
  doi?: string;
  url?: string;
};

export function UniversalPasteArea({ onConceptsFound }: { onConceptsFound?: (concepts: MemgraphConcept[]) => void }) {
  const [input, setInput] = useState("");
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleClassify = useCallback(async () => {
    if (!input.trim()) return;

    try {
      setProcessing(true);
      setError(null);
      setResult(null);

      const res = await classifyPaste(input);
      setResult(res);

      // If it's a URL, auto-ingest
      if (res.action === "scrape_url" && res.url) {
        const ingestRes = await ingestFromUrl(res.url);
        console.log("Ingestion started:", ingestRes);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Classification failed");
    } finally {
      setProcessing(false);
    }
  }, [input]);

  const handleClear = useCallback(() => {
    setInput("");
    setResult(null);
    setError(null);
  }, []);

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">Smart Paste</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <Textarea
          placeholder="Paste a URL, DOI, BibTeX entry, or research text here..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={4}
          className="resize-none"
        />
        <div className="flex gap-2">
          <Button onClick={handleClassify} disabled={processing || !input.trim()}>
            {processing ? "Analyzing..." : "Classify & Ingest"}
          </Button>
          <Button variant="outline" onClick={handleClear} disabled={!input.trim()}>
            Clear
          </Button>
        </div>

        {error && (
          <p className="text-sm text-destructive">{error}</p>
        )}

        {result && (
          <div className="space-y-2 p-3 bg-muted rounded-lg">
            <div className="flex items-center gap-2">
              <Badge variant="outline">{result.source_type}</Badge>
              <span className="text-xs text-muted-foreground">
                {(result.confidence * 100).toFixed(0)}% confidence
              </span>
            </div>
            <p className="text-sm text-muted-foreground line-clamp-2">
              {result.content_preview}
            </p>
            {result.doi && (
              <p className="text-xs text-muted-foreground">
                DOI: <code className="bg-background px-1 rounded">{result.doi}</code>
              </p>
            )}
            {result.url && (
              <p className="text-xs text-muted-foreground truncate">
                URL: {result.url}
              </p>
            )}
            <Badge className="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-xs">
              Action: {result.action.replace("_", " ")}
            </Badge>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
