import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function ArchitectureTab() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">System Architecture</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex justify-center">
          <svg viewBox="0 0 800 480" className="w-full max-w-3xl h-auto">
            {/* Background */}
            <rect width="800" height="480" fill="transparent" />

            {/* Title */}
            <text x="400" y="30" textAnchor="middle" fill="#E6EDF3" fontSize="16" fontWeight="bold" fontFamily="Raleway, sans-serif">
              QUANTIFAYA AUTODIRECTOR — Architecture
            </text>

            {/* Domain 1: Intelligence */}
            <rect x="30" y="50" width="170" height="180" rx="8" fill="#1E1B4B" stroke="#7C3AED" strokeWidth="2" />
            <text x="115" y="75" textAnchor="middle" fill="#7C3AED" fontSize="12" fontWeight="bold" fontFamily="Raleway, sans-serif">DOMAIN 1</text>
            <text x="115" y="95" textAnchor="middle" fill="#E6EDF3" fontSize="14" fontWeight="bold" fontFamily="Raleway, sans-serif">Intelligence</text>
            <text x="50" y="120" fill="#94A3B8" fontSize="11" fontFamily="monospace">Qwen LLM</text>
            <text x="50" y="140" fill="#94A3B8" fontSize="11" fontFamily="monospace">Script Generation</text>
            <text x="50" y="160" fill="#94A3B8" fontSize="11" fontFamily="monospace">Source Mining</text>
            <text x="50" y="180" fill="#94A3B8" fontSize="11" fontFamily="monospace">SEO Writer</text>
            <text x="50" y="200" fill="#94A3B8" fontSize="11" fontFamily="monospace">Storyboard / Wan Prompts</text>
            <text x="50" y="220" fill="#94A3B8" fontSize="11" fontFamily="monospace">Quality Review & Self-Correction</text>

            {/* Arrow 1 → 2 */}
            <line x1="200" y1="140" x2="250" y2="140" stroke="#F0B429" strokeWidth="2" markerEnd="url(#arrowhead)" />

            {/* Domain 2: Generation */}
            <rect x="250" y="50" width="170" height="180" rx="8" fill="#1E1B4B" stroke="#F0B429" strokeWidth="2" />
            <text x="335" y="75" textAnchor="middle" fill="#F0B429" fontSize="12" fontWeight="bold" fontFamily="Raleway, sans-serif">DOMAIN 2</text>
            <text x="335" y="95" textAnchor="middle" fill="#E6EDF3" fontSize="14" fontWeight="bold" fontFamily="Raleway, sans-serif">Generation</text>
            <text x="270" y="120" fill="#94A3B8" fontSize="11" fontFamily="monospace">Wan / HappyHorse Video</text>
            <text x="270" y="140" fill="#94A3B8" fontSize="11" fontFamily="monospace">Manim Math Animations</text>
            <text x="270" y="160" fill="#94A3B8" fontSize="11" fontFamily="monospace">edge-tts Voiceover</text>
            <text x="270" y="180" fill="#94A3B8" fontSize="11" fontFamily="monospace">AV Alignment</text>
            <text x="270" y="200" fill="#94A3B8" fontSize="11" fontFamily="monospace">PIL Thumbnail</text>
            <text x="270" y="220" fill="#94A3B8" fontSize="11" fontFamily="monospace">Wan Fallback (Manim Title)</text>

            {/* Arrow 2 → 3 */}
            <line x1="420" y1="140" x2="470" y2="140" stroke="#22C55E" strokeWidth="2" />

            {/* Domain 3: Orchestration */}
            <rect x="470" y="50" width="150" height="180" rx="8" fill="#1E1B4B" stroke="#22C55E" strokeWidth="2" />
            <text x="545" y="75" textAnchor="middle" fill="#22C55E" fontSize="12" fontWeight="bold" fontFamily="Raleway, sans-serif">DOMAIN 3</text>
            <text x="545" y="95" textAnchor="middle" fill="#E6EDF3" fontSize="14" fontWeight="bold" fontFamily="Raleway, sans-serif">Orchestration</text>
            <text x="485" y="120" fill="#94A3B8" fontSize="11" fontFamily="monospace">LangGraph State Graph</text>
            <text x="485" y="140" fill="#94A3B8" fontSize="11" fontFamily="monospace">Celery Job Queue</text>
            <text x="485" y="160" fill="#94A3B8" fontSize="11" fontFamily="monospace">State Management</text>
            <text x="485" y="180" fill="#94A3B8" fontSize="11" fontFamily="monospace">Error Recovery</text>
            <text x="485" y="200" fill="#94A3B8" fontSize="11" fontFamily="monospace">Human Review Gate</text>
            <text x="485" y="220" fill="#94A3B8" fontSize="11" fontFamily="monospace">Parallel Execution</text>

            {/* Arrow 3 → 4 */}
            <line x1="620" y1="140" x2="660" y2="140" stroke="#F0B429" strokeWidth="2" />

            {/* Domain 4: Delivery */}
            <rect x="660" y="50" width="120" height="180" rx="8" fill="#1E1B4B" stroke="#F0B429" strokeWidth="2" />
            <text x="720" y="75" textAnchor="middle" fill="#F0B429" fontSize="12" fontWeight="bold" fontFamily="Raleway, sans-serif">DOMAIN 4</text>
            <text x="720" y="95" textAnchor="middle" fill="#E6EDF3" fontSize="14" fontWeight="bold" fontFamily="Raleway, sans-serif">Delivery</text>
            <text x="675" y="120" fill="#94A3B8" fontSize="11" fontFamily="monospace">ffmpeg Composition</text>
            <text x="675" y="140" fill="#94A3B8" fontSize="11" fontFamily="monospace">Scene Stitching</text>
            <text x="675" y="160" fill="#94A3B8" fontSize="11" fontFamily="monospace">Subtitle Embedding</text>
            <text x="675" y="180" fill="#94A3B8" fontSize="11" fontFamily="monospace">YouTube Upload</text>
            <text x="675" y="200" fill="#94A3B8" fontSize="11" fontFamily="monospace">Chapter Markers</text>
            <text x="675" y="220" fill="#94A3B8" fontSize="11" fontFamily="monospace">Thumbnail Set</text>

            {/* Data Layer */}
            <rect x="80" y="280" width="640" height="80" rx="8" fill="#0D1117" stroke="#30363D" strokeWidth="1.5" strokeDasharray="5,3" />
            <text x="400" y="305" textAnchor="middle" fill="#8B949E" fontSize="12" fontWeight="bold" fontFamily="Raleway, sans-serif">DATA LAYER</text>

            <rect x="100" y="315" width="120" height="30" rx="4" fill="#161B22" stroke="#30363D" strokeWidth="1" />
            <text x="160" y="335" textAnchor="middle" fill="#58A6FF" fontSize="11" fontFamily="monospace">PostgreSQL</text>

            <rect x="250" y="315" width="100" height="30" rx="4" fill="#161B22" stroke="#30363D" strokeWidth="1" />
            <text x="300" y="335" textAnchor="middle" fill="#58A6FF" fontSize="11" fontFamily="monospace">Redis</text>

            <rect x="380" y="315" width="100" height="30" rx="4" fill="#161B22" stroke="#30363D" strokeWidth="1" />
            <text x="430" y="335" textAnchor="middle" fill="#58A6FF" fontSize="11" fontFamily="monospace">MinIO</text>

            <rect x="510" y="315" width="140" height="30" rx="4" fill="#161B22" stroke="#30363D" strokeWidth="1" />
            <text x="580" y="335" textAnchor="middle" fill="#58A6FF" fontSize="11" fontFamily="monospace">Output Volumes</text>

            {/* API Layer */}
            <rect x="80" y="390" width="640" height="60" rx="8" fill="#0D1117" stroke="#30363D" strokeWidth="1.5" strokeDasharray="5,3" />
            <text x="400" y="415" textAnchor="middle" fill="#8B949E" fontSize="12" fontWeight="bold" fontFamily="Raleway, sans-serif">API & INTERFACE LAYER</text>

            <rect x="100" y="425" width="140" height="20" rx="4" fill="#161B22" stroke="#30363D" strokeWidth="1" />
            <text x="170" y="440" textAnchor="middle" fill="#F0B429" fontSize="10" fontFamily="monospace">FastAPI (REST)</text>

            <rect x="260" y="425" width="120" height="20" rx="4" fill="#161B22" stroke="#30363D" strokeWidth="1" />
            <text x="320" y="440" textAnchor="middle" fill="#F0B429" fontSize="10" fontFamily="monospace">Celery Workers</text>

            <rect x="400" y="425" width="100" height="20" rx="4" fill="#161B22" stroke="#30363D" strokeWidth="1" />
            <text x="450" y="440" textAnchor="middle" fill="#F0B429" fontSize="10" fontFamily="monospace">Flower</text>

            <rect x="520" y="425" width="140" height="20" rx="4" fill="#161B22" stroke="#30363D" strokeWidth="1" />
            <text x="590" y="440" textAnchor="middle" fill="#F0B429" fontSize="10" fontFamily="monospace">React Dashboard</text>

            {/* Arrow markers */}
            <defs>
              <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#F0B429" />
              </marker>
            </defs>
          </svg>
        </div>
      </CardContent>
    </Card>
  );
}