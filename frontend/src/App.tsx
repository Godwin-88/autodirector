import { useState, useEffect, useCallback, useRef } from "react";
import { Header } from "@/components/Header";
import { EpisodeForm } from "@/components/EpisodeForm";
import { PipelineFlow } from "@/components/PipelineFlow";
import { ScriptPreview } from "@/components/ScriptPreview";
import { WanPreview } from "@/components/WanPreview";
import { VideoPlayer } from "@/components/VideoPlayer";
import { ArchitectureTab } from "@/components/ArchitectureTab";
import { EpisodeList } from "@/components/EpisodeList";
import { SourceManager, EpisodeSourcePanel } from "@/components/SourceManager";
import { SuggestionPanel } from "@/components/SuggestionPanel";
import { StrategyBoard } from "@/components/StrategyBoard";
import { UniversalPasteArea } from "@/components/UniversalPasteArea";
import { MemgraphConceptSidebar } from "@/components/MemgraphConceptSidebar";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import {
  createEpisode,
  listEpisodes,
  getEpisode,
  deleteEpisode,
  subscribeToProgress,
} from "@/api/episodes";
import type {
  PipelineStage,
  SceneData,
  EpisodeListItem,
  StageUpdateEvent,
  ScriptChunkEvent,
} from "@/types/episode";

const INITIAL_STAGES: PipelineStage[] = [
  {
    name: "intelligence",
    label: "Intelligence",
    status: "pending",
    elapsed_seconds: 0,
    substages: [
      { name: "outline", label: "Outline Generation", status: "pending" },
      { name: "script", label: "Script Generation", status: "pending" },
      { name: "sources", label: "Source Extraction", status: "pending" },
      { name: "manim_specs", label: "Manim Specs", status: "pending" },
      { name: "wan_prompts", label: "Wan Prompts", status: "pending" },
      { name: "seo", label: "SEO Metadata", status: "pending" },
    ],
  },
  {
    name: "generation",
    label: "Generation",
    status: "pending",
    elapsed_seconds: 0,
    substages: [
      { name: "wan_video", label: "Wan Video", status: "pending" },
      { name: "manim_render", label: "Manim Render", status: "pending" },
      { name: "tts", label: "Voice Synthesis", status: "pending" },
      { name: "av_align", label: "AV Alignment", status: "pending" },
    ],
  },
  {
    name: "composition",
    label: "Composition",
    status: "pending",
    elapsed_seconds: 0,
    substages: [
      { name: "scene_sync", label: "Scene Sync", status: "pending" },
      { name: "episode_compose", label: "Episode Compose", status: "pending" },
      { name: "subtitles", label: "Subtitles", status: "pending" },
    ],
  },
  {
    name: "delivery",
    label: "Delivery",
    status: "pending",
    elapsed_seconds: 0,
    substages: [
      { name: "thumbnail", label: "Thumbnail", status: "pending" },
      { name: "youtube_upload", label: "YouTube Upload", status: "pending" },
    ],
  },
];

export default function App() {
  const [episodes, setEpisodes] = useState<EpisodeListItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [stages, setStages] = useState<PipelineStage[]>(INITIAL_STAGES);
  const [scenes, setScenes] = useState<SceneData[]>([]);
  const [streamingText, setStreamingText] = useState<string | undefined>();
  const [wanLoading, setWanLoading] = useState(false);
  const [wanThumbnail, setWanThumbnail] = useState<string | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [videoReady, setVideoReady] = useState(false);
  const [activeTab, setActiveTab] = useState("pipeline");
  const unsubscribeRef = useRef<(() => void) | null>(null);

  const loadEpisodes = useCallback(async () => {
    try {
      const res = await listEpisodes();
      setEpisodes(res.data.episodes);
    } catch (err) {
      console.error("Failed to load episodes:", err);
    }
  }, []);

  useEffect(() => {
    loadEpisodes();
  }, [loadEpisodes]);

  const handleSelectEpisode = useCallback(async (id: string) => {
    setSelectedId(id);
    setScenes([]);
    setStreamingText(undefined);
    setWanThumbnail(null);
    setVideoUrl(null);
    setVideoReady(false);
    setStages(INITIAL_STAGES);

    // Unsubscribe from previous SSE
    if (unsubscribeRef.current) {
      unsubscribeRef.current();
    }

    try {
      const res = await getEpisode(id);
      const ep = res.data;

      // If already completed, show video
      if (ep.status === "completed" && ep.video_path) {
        setVideoUrl(`/output/episodes/${id}/${ep.video_path}`);
        setVideoReady(true);
        setStages((prev) =>
          prev.map((s) => ({ ...s, status: "done" as const }))
        );
      }

      // If has script, show it
      if (ep.script?.scenes) {
        setScenes(ep.script.scenes);
      }

      // Subscribe to SSE for active episodes
      if (
        !["completed", "failed", "draft"].includes(ep.status)
      ) {
        setIsGenerating(true);
        unsubscribeRef.current = subscribeToProgress(id, {
          onStageUpdate: (event: StageUpdateEvent) => {
            setStages((prev) =>
              prev.map((stage) => {
                if (stage.name === event.stage) {
                  const updatedSubstages = stage.substages.map((sub) =>
                    sub.name === event.substage
                      ? { ...sub, status: event.status }
                      : sub
                  );
                  const allDone = updatedSubstages.every(
                    (s) => s.status === "done"
                  );
                  const anyFailed = updatedSubstages.some(
                    (s) => s.status === "failed"
                  );
                  return {
                    ...stage,
                    status: allDone ? "done" : anyFailed ? "failed" : event.status,
                    substages: updatedSubstages,
                    elapsed_seconds: event.elapsed_seconds,
                  };
                }
                return stage;
              })
            );
          },
          onScriptChunk: (event: ScriptChunkEvent) => {
            setStreamingText(event.text);
            setScenes((prev) => {
              const existing = prev.find(
                (s) => s.scene_number === event.scene_index
              );
              if (existing) {
                return prev.map((s) =>
                  s.scene_number === event.scene_index
                    ? { ...s, content: s.content + event.text }
                    : s
                );
              }
              return [
                ...prev,
                {
                  scene_number: event.scene_index,
                  title: `Scene ${event.scene_index}`,
                  content: event.text,
                  stage_direction: "",
                  duration_seconds: 120,
                },
              ];
            });
          },
          onVideoReady: (event) => {
            setVideoUrl(event.url);
            setVideoReady(true);
          },
          onError: (event) => {
            console.error("Pipeline error:", event);
            setStages((prev) =>
              prev.map((s) =>
                s.name === event.stage ? { ...s, status: "failed" as const } : s
              )
            );
          },
          onComplete: () => {
            setIsGenerating(false);
            loadEpisodes();
          },
        });
      }
    } catch (err) {
      console.error("Failed to load episode:", err);
    }
  }, [loadEpisodes]);

  const handleGenerate = useCallback(
    async (topic: string, episodeNumber: number) => {
      setIsGenerating(true);
      setScenes([]);
      setStreamingText(undefined);
      setWanThumbnail(null);
      setVideoUrl(null);
      setVideoReady(false);
      setStages(INITIAL_STAGES);

      try {
        const res = await createEpisode(topic, episodeNumber);
        const episodeId = res.data.id;
        setSelectedId(episodeId);
        await loadEpisodes();

        // Subscribe to SSE
        unsubscribeRef.current = subscribeToProgress(episodeId, {
          onStageUpdate: (event: StageUpdateEvent) => {
            setStages((prev) =>
              prev.map((stage) => {
                if (stage.name === event.stage) {
                  const updatedSubstages = stage.substages.map((sub) =>
                    sub.name === event.substage
                      ? { ...sub, status: event.status }
                      : sub
                  );
                  const allDone = updatedSubstages.every(
                    (s) => s.status === "done"
                  );
                  const anyFailed = updatedSubstages.some(
                    (s) => s.status === "failed"
                  );
                  return {
                    ...stage,
                    status: allDone ? "done" : anyFailed ? "failed" : event.status,
                    substages: updatedSubstages,
                    elapsed_seconds: event.elapsed_seconds,
                  };
                }
                return stage;
              })
            );
          },
          onScriptChunk: (event: ScriptChunkEvent) => {
            setStreamingText(event.text);
            setScenes((prev) => {
              const existing = prev.find(
                (s) => s.scene_number === event.scene_index
              );
              if (existing) {
                return prev.map((s) =>
                  s.scene_number === event.scene_index
                    ? { ...s, content: s.content + event.text }
                    : s
                );
              }
              return [
                ...prev,
                {
                  scene_number: event.scene_index,
                  title: `Scene ${event.scene_index}`,
                  content: event.text,
                  stage_direction: "",
                  duration_seconds: 120,
                },
              ];
            });
          },
          onVideoReady: (event) => {
            setVideoUrl(event.url);
            setVideoReady(true);
          },
          onError: (event) => {
            console.error("Pipeline error:", event);
            setStages((prev) =>
              prev.map((s) =>
                s.name === event.stage
                  ? { ...s, status: "failed" as const }
                  : s
              )
            );
          },
          onComplete: () => {
            setIsGenerating(false);
            loadEpisodes();
          },
        });
      } catch (err) {
        console.error("Failed to create episode:", err);
        setIsGenerating(false);
      }
    },
    [loadEpisodes]
  );

  const handleDelete = useCallback(
    async (id: string) => {
      try {
        await deleteEpisode(id);
        if (selectedId === id) {
          setSelectedId(null);
          setScenes([]);
          setVideoUrl(null);
          setVideoReady(false);
          setStages(INITIAL_STAGES);
        }
        await loadEpisodes();
      } catch (err) {
        console.error("Failed to delete episode:", err);
      }
    },
    [selectedId, loadEpisodes]
  );

  // Cleanup SSE on unmount
  useEffect(() => {
    return () => {
      if (unsubscribeRef.current) {
        unsubscribeRef.current();
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <EpisodeForm
              onGenerate={handleGenerate}
              disabled={isGenerating}
            />
            <div>
              <h2 className="text-sm font-semibold text-foreground mb-3">
                Episodes
              </h2>
              <EpisodeList
                episodes={episodes}
                selectedId={selectedId}
                onSelect={handleSelectEpisode}
                onDelete={handleDelete}
              />
            </div>
          </div>

          {/* Main content */}
          <div className="lg:col-span-3 space-y-6">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList>
                <TabsTrigger value="pipeline">Pipeline</TabsTrigger>
                <TabsTrigger value="sources">Sources</TabsTrigger>
                <TabsTrigger value="strategy">Strategy</TabsTrigger>
                <TabsTrigger value="architecture">Architecture</TabsTrigger>
              </TabsList>

              <TabsContent value="pipeline">
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                  <div className="space-y-6">
                    <PipelineFlow stages={stages} />
                    <WanPreview
                      thumbnailUrl={wanThumbnail}
                      isLoading={wanLoading}
                    />
                  </div>
                  <div className="space-y-6">
                    <ScriptPreview
                      scenes={scenes}
                      streamingText={streamingText}
                    />
                    <VideoPlayer
                      videoUrl={videoUrl}
                      isReady={videoReady}
                    />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="sources">
                <SourceManager />
                {selectedId && <EpisodeSourcePanel episodeId={selectedId} />}
              </TabsContent>

              <TabsContent value="strategy">
                <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                  <div className="xl:col-span-1 space-y-6">
                    <SuggestionPanel />
                    <MemgraphConceptSidebar />
                  </div>
                  <div className="xl:col-span-2 space-y-6">
                    <StrategyBoard />
                    <UniversalPasteArea />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="architecture">
                <ArchitectureTab />
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </main>
    </div>
  );
}