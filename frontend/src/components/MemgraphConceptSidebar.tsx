import { useState, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { searchMemgraphConcepts, getMemgraphConcept } from "@/api/sources";
import type { MemgraphConcept, MemgraphConceptDetail } from "@/types/sources";

export function MemgraphConceptSidebar() {
  const [query, setQuery] = useState("");
  const [concepts, setConcepts] = useState<MemgraphConcept[]>([]);
  const [selected, setSelected] = useState<MemgraphConceptDetail | null>(null);
  const [searching, setSearching] = useState(false);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = useCallback(async () => {
    if (!query.trim()) return;
    try {
      setSearching(true);
      setError(null);
      setSelected(null);
      const res = await searchMemgraphConcepts(query);
      setConcepts(res.concepts);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Search failed");
    } finally {
      setSearching(false);
    }
  }, [query]);

  const handleSelect = useCallback(async (name: string) => {
    try {
      setLoadingDetail(true);
      setError(null);
      const res = await getMemgraphConcept(name);
      setSelected(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load concept");
    } finally {
      setLoadingDetail(false);
    }
  }, []);

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Knowledge Graph</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex gap-2">
            <Input
              placeholder="Search concepts..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
            <Button onClick={handleSearch} disabled={searching || !query.trim()} size="sm">
              {searching ? "..." : "Search"}
            </Button>
          </div>

          {error && <p className="text-sm text-destructive">{error}</p>}

          {concepts.length > 0 && !selected && (
            <div className="space-y-1 max-h-[300px] overflow-y-auto">
              {concepts.map((c, i) => (
                <button
                  key={i}
                  className="w-full text-left px-3 py-2 rounded-md text-sm hover:bg-accent transition-colors"
                  onClick={() => handleSelect(c.name)}
                >
                  <span className="font-medium">{c.name}</span>
                  {c.definition && (
                    <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">
                      {c.definition}
                    </p>
                  )}
                  {c.equations.length > 0 && (
                    <div className="flex gap-1 mt-1">
                      {c.equations.map((eq, j) => (
                        <Badge key={j} variant="outline" className="text-[10px]">
                          {eq}
                        </Badge>
                      ))}
                    </div>
                  )}
                </button>
              ))}
            </div>
          )}

          {selected && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h4 className="font-semibold">{selected.name}</h4>
                <Button variant="ghost" size="sm" onClick={() => setSelected(null)}>
                  Back
                </Button>
              </div>

              {selected.definition && (
                <p className="text-sm text-muted-foreground">{selected.definition}</p>
              )}

              {selected.equations.length > 0 && (
                <div>
                  <p className="text-xs font-medium text-muted-foreground mb-1">Equations:</p>
                  <div className="flex flex-wrap gap-1">
                    {selected.equations.map((eq, i) => (
                      <Badge key={i} variant="secondary" className="text-xs font-mono">
                        {eq}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {selected.subgraph?.nodes && selected.subgraph.nodes.length > 0 && (
                <div>
                  <p className="text-xs font-medium text-muted-foreground mb-1">
                    Subgraph ({selected.subgraph.nodes.length} nodes):
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {selected.subgraph.nodes.slice(0, 10).map((n, i) => (
                      <Badge key={i} variant="outline" className="text-[10px]">
                        {n.name}
                      </Badge>
                    ))}
                    {selected.subgraph.nodes.length > 10 && (
                      <span className="text-[10px] text-muted-foreground">
                        +{selected.subgraph.nodes.length - 10} more
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {!concepts.length && !searching && !selected && (
            <p className="text-sm text-muted-foreground">
              Search for Memgraph concepts to explore the knowledge graph
            </p>
          )}

          {loadingDetail && (
            <p className="text-sm text-muted-foreground animate-pulse">Loading concept...</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
