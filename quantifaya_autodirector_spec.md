# QUANTIFAYA AUTODIRECTOR
## Production Specification — Qwen Cloud Hackathon Track 2
### "Autonomous AI Showrunner for Financial Engineering Education"

**Version:** 1.0  
**Date:** July 2026  
**Author:** Quantifaya Engineering  
**Hackathon:** Qwen Cloud Hackathon — Track 2: AI Short Drama / Video Generation  
**Deadline:** July 20, 2026  
**Framework:** Digital Capability Canvas (Strategic → Execution)

---

## PART I: DIGITAL CAPABILITY CANVAS

---

### 1. STRATEGIC INTENT

**Vision:** The world's first autonomous AI showrunner for quantitative finance education — a system that takes a topic as input and returns a publication-ready YouTube video as output, with zero human intervention between intent and render.

**Mission:** Demonstrate that the Qwen Cloud model stack can orchestrate multimodal AI pipelines — combining narrative AI (LLM scriptwriting), generative video (Wan character footage), programmatic animation (Manim), and voice synthesis (edge-tts) — into a single agentic loop that produces content of genuine educational and commercial value.

**Hackathon Winning Thesis:** Most Track 2 submissions will chain Wan calls to generate drama clips. Quantifaya AutoDirector combines Wan-generated character footage with Manim-generated mathematical precision — the drama layer makes it Track 2 compliant; the math layer makes it defensible and genuinely novel. No diffusion model can render correct LaTeX. We can. That is the moat.

**Post-Hackathon Value:** A production pipeline that generates one Quantifaya episode per day, fully automated, with human review as the only gate before upload.

---

### 2. USER SEGMENTS

| Segment | Need | How AutoDirector Serves Them |
|---|---|---|
| **Content Creator (G — Primary)** | Daily video production without per-episode manual effort | Full automation from topic → rendered video |
| **Hackathon Judges** | Demonstrate Qwen Cloud API capabilities at depth | Multi-model orchestration: LLM + Wan + Manim pipeline |
| **YouTube Audience** | Finance-literate education with visual rigour | Accurate math + cinematic character intro sequences |
| **Future Licensees** | White-label education pipeline | Modular, API-driven, configurable per brand |

---

### 3. VALUE PROPOSITION

**For the hackathon:** A live demonstration that a Qwen-orchestrated agent can autonomously produce a 25-minute educational video — writing the script, generating character footage, rendering mathematical animations, synthesizing voice-over, and stitching everything into a single deliverable — from a single text prompt.

**For Quantifaya:** Elimination of manual scripting labour (currently ~8 hours per episode). Target: topic → render-ready video in under 60 minutes of wall-clock time.

**Differentiation from competitors:**
1. **Mathematical accuracy:** Wan-generated footage cannot render verified LaTeX. Manim can. We ship both.
2. **Persona fidelity:** Qwen writes in the Taylor+Axe+Taleb persona — not generic AI narration.
3. **Academic sourcing:** The LLM extracts and cites real academic sources per scene, not hallucinated references.
4. **Production system:** This is not a demo. It produces real episodes for a real YouTube channel.

---

### 4. CAPABILITY DOMAINS

```
┌─────────────────────────────────────────────────────────────────────┐
│                    QUANTIFAYA AUTODIRECTOR                          │
│                    Capability Architecture                          │
├──────────────┬──────────────┬──────────────┬────────────────────────┤
│ DOMAIN 1     │ DOMAIN 2     │ DOMAIN 3     │ DOMAIN 4               │
│ Intelligence │ Generation   │ Orchestration│ Delivery               │
├──────────────┼──────────────┼──────────────┼────────────────────────┤
│ Qwen LLM     │ Wan Video    │ LangGraph    │ ffmpeg Compositor      │
│ Script Gen   │ Manim Math   │ Job Queue    │ YouTube Upload API     │
│ Source Mining│ edge-tts     │ State Mgmt   │ Metadata Generator     │
│ SEO Writer   │ Thumbnail Gen│ Error Recov  │ Chapter Writer         │
└──────────────┴──────────────┴──────────────┴────────────────────────┘
```

**Domain 1 — Intelligence Layer (Qwen Cloud)**
- Script generation per Quantifaya persona
- Scene-by-scene academic source extraction
- SEO metadata (title, description, tags, chapters)
- Storyboard generation for Wan prompts
- Quality review and self-correction loop

**Domain 2 — Generation Layer (Multi-modal)**
- Wan/HappyHorse: character intro footage (5–15s per episode)
- Manim: mathematical animation per scene (deterministic, verified)
- edge-tts: voice-over synthesis per scene block
- PIL/Pillow: thumbnail generation

**Domain 3 — Orchestration Layer (LangGraph)**
- Directed graph of generation tasks
- Parallel execution where possible (Manim + Wan simultaneously)
- Retry logic and fallback handling
- Human-in-the-loop checkpoint (pre-render review gate)

**Domain 4 — Delivery Layer**
- ffmpeg: audio-visual sync, scene stitching, intro prepend
- YouTube Data API v3: auto-upload with metadata
- PostgreSQL: episode persistence and production history
- Redis: job queue and progress tracking

---

### 5. PROCESS ARCHITECTURE

```
INPUT: Topic string
  │
  ▼
┌─────────────────────────────────────────────────────────┐
│ PHASE 1: INTELLIGENCE (Qwen Cloud)             ~5 min   │
│                                                          │
│  1.1 Topic Analysis → Episode outline                   │
│  1.2 Source Mining → Academic references list           │
│  1.3 Script Generation → Full voice-over script         │
│  1.4 Scene Decomposition → Manim scene specs            │
│  1.5 Storyboard → Wan video prompts per scene           │
│  1.6 SEO Generation → Title, desc, tags, chapters       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ HUMAN REVIEW GATE    │ ← approve/edit script
              │ (optional in prod,   │
              │  mandatory in demo)  │
              └──────────┬───────────┘
                         │
  ┌──────────────────────▼──────────────────────────────┐
  │ PHASE 2: PARALLEL GENERATION              ~25 min   │
  │                                                      │
  │  [Thread A] Wan API calls → character footage clips  │
  │  [Thread B] Manim render → scene MP4s per class     │
  │  [Thread C] edge-tts synthesis → scene WAV files    │
  └──────────────────────┬──────────────────────────────┘
                         │
  ┌──────────────────────▼──────────────────────────────┐
  │ PHASE 3: COMPOSITION (ffmpeg)             ~10 min   │
  │                                                      │
  │  3.1 Sync audio to each Manim scene (per-scene)     │
  │  3.2 Prepend Wan character intro clip               │
  │  3.3 Add brand intro/outro (static Manim renders)   │
  │  3.4 Add chapter markers and subtitles              │
  │  3.5 Export final MP4 (1080p60)                    │
  └──────────────────────┬──────────────────────────────┘
                         │
  ┌──────────────────────▼──────────────────────────────┐
  │ PHASE 4: DELIVERY                          ~2 min   │
  │                                                      │
  │  4.1 Generate thumbnail (PIL)                       │
  │  4.2 Upload to YouTube (Data API v3)                │
  │  4.3 Set metadata: title, desc, tags, chapters      │
  │  4.4 Log to PostgreSQL episode table                │
  └─────────────────────────────────────────────────────┘

OUTPUT: Published YouTube video with full metadata
```

---

### 6. DATA & INTELLIGENCE LAYER

**Qwen Cloud Models Used:**

| Model | Purpose | Call Type |
|---|---|---|
| `qwen-max` | Full script generation, persona writing | Long-context completion |
| `qwen-turbo` | SEO metadata, chapter generation | Fast completion |
| `qwen-vl` | Storyboard image analysis, thumbnail review | Multimodal |
| Wan API | Character video generation | Video generation endpoint |

**Data Schemas:**

```sql
-- Episode table
CREATE TABLE episodes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic           TEXT NOT NULL,
    episode_number  INTEGER,
    series          TEXT DEFAULT 'quantifaya',
    status          TEXT DEFAULT 'pending',  -- pending|scripting|generating|compositing|delivered|failed
    script_json     JSONB,
    sources_json    JSONB,
    seo_json        JSONB,
    output_path     TEXT,
    youtube_id      TEXT,
    duration_secs   INTEGER,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);

-- Scene table
CREATE TABLE scenes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    episode_id      UUID REFERENCES episodes(id),
    scene_number    INTEGER NOT NULL,
    scene_class     TEXT NOT NULL,      -- e.g. SceneDelta
    voiceover_text  TEXT NOT NULL,
    manim_spec      JSONB,              -- equations, colors, layout
    wan_prompt      TEXT,               -- prompt for Wan character clip
    audio_path      TEXT,
    video_path      TEXT,
    duration_secs   FLOAT,
    status          TEXT DEFAULT 'pending'
);

-- Job queue (Redis-backed, mirrored to PG for audit)
CREATE TABLE jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    episode_id      UUID REFERENCES episodes(id),
    job_type        TEXT NOT NULL,      -- wan_generate|manim_render|tts_synthesize|compose|upload
    payload         JSONB,
    status          TEXT DEFAULT 'queued',
    attempts        INTEGER DEFAULT 0,
    error_msg       TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);
```

---

### 7. TECHNOLOGY STACK

```
┌─────────────────────────────────────────────────────────┐
│ LAYER          │ TECHNOLOGY          │ PURPOSE           │
├────────────────┼─────────────────────┼───────────────────┤
│ Orchestration  │ LangGraph (Python)  │ Agentic DAG       │
│ LLM            │ Qwen Cloud API      │ Script + SEO gen  │
│ Video Gen      │ Wan/HappyHorse API  │ Character footage │
│ Math Anim      │ Manim Community     │ Scene rendering   │
│ Voice          │ edge-tts            │ Voice synthesis   │
│ Composition    │ ffmpeg              │ A/V stitching     │
│ Backend        │ FastAPI (Python)    │ REST API layer    │
│ Queue          │ Redis + Celery      │ Async job mgmt    │
│ Database       │ PostgreSQL          │ State persistence │
│ Frontend       │ React (minimal)     │ Demo dashboard    │
│ Thumbnail      │ PIL/Pillow          │ Image generation  │
│ Upload         │ YouTube Data API v3 │ Auto-publishing   │
│ Infra          │ Docker Compose      │ Local + Contabo   │
└─────────────────────────────────────────────────────────┘
```

---

### 8. PEOPLE & ROLES (Solo Execution — G)

| Role | Responsibility | Tools |
|---|---|---|
| **Product Owner** | Define acceptance criteria, review outputs | This document |
| **AI Engineer** | LangGraph agent, Qwen API integration | Python, LangGraph |
| **Backend Engineer** | FastAPI, PostgreSQL, Redis, job queue | Python, Docker |
| **Animation Engineer** | Manim scene classes, rendering pipeline | Python, Manim |
| **DevOps** | Docker Compose, Contabo VPS, CI | Docker, Nginx |
| **Content Director** | Script persona review, quality gate | Manual review step |

---

### 9. GOVERNANCE & RISK

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Wan API quota exhaustion | Medium | High | Cap to 1 Wan clip per episode (intro only); fallback to Manim title card |
| Manim render time overrun | Medium | Medium | Pre-render common elements; parallel scene rendering |
| Qwen script quality below persona standard | Low | High | Self-critique loop: Qwen reviews its own output vs persona checklist |
| ffmpeg sync drift between audio and video | Medium | High | Per-scene sync with `setpts` filter; run automated duration check |
| YouTube API upload failure | Low | Low | Retry 3x; fallback to local file output for manual upload |
| Hackathon deadline miss | Low | Critical | MVP scope: 1 end-to-end demo video by Day 5; refinement Days 6–7 |

---

### 10. METRICS & KPIs

**Hackathon Evaluation Metrics:**

| Metric | Target | Measurement |
|---|---|---|
| End-to-end automation | Topic → video with 0 manual steps | Demo walkthrough |
| Qwen API utilization depth | ≥3 distinct model calls in pipeline | Code audit |
| Video quality | 1080p60, correct LaTeX, synced audio | Judges view |
| Wan integration | ≥1 generated character clip in output | Video review |
| Production readiness | Deployed, accessible URL or runnable Docker | devpost submission |

**Post-Hackathon Production Metrics:**

| Metric | Target |
|---|---|
| Episode generation time (wall-clock) | < 60 minutes topic → upload |
| Script persona adherence score (self-eval) | ≥ 8/10 on Taylor+Axe+Taleb rubric |
| YouTube upload success rate | ≥ 95% |
| Manim render failure rate | < 5% |
| Daily episode cadence | 1 per day, sustained |

---

---

## PART II: PRODUCT BACKLOG

### EPIC STRUCTURE

```
EP-01  Intelligence Layer — Qwen Script Engine
EP-02  Wan Video Generation Layer
EP-03  Manim Automation Engine  
EP-04  Voice Synthesis Pipeline
EP-05  LangGraph Orchestration Agent
EP-06  ffmpeg Composition Engine
EP-07  FastAPI Backend & Job Queue
EP-08  Delivery & YouTube Integration
EP-09  Demo Dashboard (Hackathon Submission)
EP-10  Production Hardening & Deployment
```

---

## EPIC EP-01: INTELLIGENCE LAYER — QWEN SCRIPT ENGINE

**Strategic Goal:** Qwen Cloud generates a full production-ready episode script in the Quantifaya persona, with verified academic sources, Manim scene specs, Wan storyboard prompts, and SEO metadata — from a single topic string input.

**Capability Domain:** Intelligence

---

### FEATURE F-01.1: Topic Analysis & Episode Outline Generator

**Description:** Given a topic string (e.g. "The Heston Model"), Qwen produces a structured episode outline with scene count, scene titles, key equations, and academic sources to pull.

**User Story US-01.1.1:**
> As the AutoDirector pipeline, I need to send a topic to Qwen and receive a structured JSON episode outline, so that downstream agents have a deterministic scaffold to work from.

**Acceptance Criteria:**
- [ ] POST `/api/v1/outline` accepts `{"topic": str, "episode_number": int, "series": str}`
- [ ] Qwen call uses `qwen-max` with a system prompt enforcing Quantifaya persona, Taylor+Axe tone, and output as valid JSON
- [ ] Response JSON contains: `title`, `seo_title`, `scenes[]` (each with `scene_number`, `scene_class_name`, `title`, `duration_target_secs`, `key_equations[]`, `key_sources[]`)
- [ ] Minimum 8 scenes, maximum 12 scenes per outline
- [ ] Scene duration targets sum to 1400–1600 seconds (23–27 min)
- [ ] Response validated against Pydantic `EpisodeOutline` schema before storage
- [ ] Outline written to `episodes` table with `status='outlined'`
- [ ] If Qwen returns invalid JSON, retry up to 3 times with a corrective prompt
- [ ] Unit test: mock Qwen response, assert Pydantic validation passes
- [ ] Integration test: live Qwen call on topic "Yield Curves", assert ≥8 scenes returned

---

### FEATURE F-01.2: Academic Source Extractor

**Description:** For each scene in the outline, Qwen generates 2–4 verified academic citations in APA format, tagged to the specific scene they support. Sources must be real, citable works — not hallucinated.

**User Story US-01.2.1:**
> As the AutoDirector, I need each scene to have real academic citations, so that the video maintains Quantifaya's credibility standard and the pinned YouTube comment can list them accurately.

**Acceptance Criteria:**
- [ ] Source extractor runs per scene, not per episode (allows parallelism)
- [ ] Qwen prompt instructs: "Return only real, verifiable academic works. If uncertain, omit rather than invent."
- [ ] Each source has fields: `ref_number`, `authors`, `year`, `title`, `journal_or_publisher`, `doi_or_url`, `scene_usage_note`
- [ ] Sources stored in `scenes.sources_json` and aggregated to `episodes.sources_json`
- [ ] Post-generation: a Qwen self-review call checks each source for plausibility (author + year + title consistency)
- [ ] Any source failing self-review is flagged with `confidence: "low"` — human gate can inspect
- [ ] Sources formatted for on-screen citation tags: `[Author (Year)]` format matching episodes 1–4 style
- [ ] Test: topic "Black-Scholes", assert Black & Scholes (1973) appears in output with correct journal

---

### FEATURE F-01.3: Full Script Generator (Persona Engine)

**Description:** Qwen writes the complete voice-over script for every scene, in the Taylor+Axe+Taleb persona, with Taleb quotes integrated where sourced, sarcastic asides, and zero tolerance for hand-waving.

**User Story US-01.3.1:**
> As the content creator (G), I need the generated script to sound like it was written by me — Taylor-meets-Axe-Capital energy, Taleb intellectual ruthlessness — so I don't have to rewrite it before production.

**Acceptance Criteria:**
- [ ] Script generator receives: outline JSON + sources JSON + persona system prompt
- [ ] Persona system prompt encodes: Taylor+Axe swagger, Taleb intellectual aggression, no hand-waving rule, "we show" derivation standard, sarcastic asides in gold italic (stage direction), pauses marked as `[PAUSE]`
- [ ] Each scene's script contains: opening hook, derivation/explanation body, [PAUSE] markers, any Taleb quote if source available, closing transition
- [ ] Script word count per scene targets 300–500 words (≈ 2–3 min of speech at 160 WPM)
- [ ] Equations in script written as LaTeX: `$\Delta = N(d_1)$` format for TTS substitution
- [ ] Qwen self-review: second call asks "Does this script match the persona checklist? Score 1–10 per criterion." If any criterion < 7, regenerate that scene.
- [ ] Persona checklist criteria: (1) No hand-waving, (2) Sarcasm present, (3) Equation derivation shown, (4) Real-world consequence named, (5) Taleb/financial crisis reference where relevant
- [ ] Script stored in `scenes.voiceover_text` and full script in `episodes.script_json`
- [ ] Integration test: generate script for "The Greeks", assert "continuous-time hedging" critique appears (Taleb Ch.7 reference)

---

### FEATURE F-01.4: Manim Scene Specification Generator

**Description:** Qwen translates each script scene into a structured Manim scene specification — animation sequences, equation lists, color assignments, visual cues — that the Manim engine can execute without further LLM calls.

**User Story US-01.4.1:**
> As the Manim render engine, I need a structured scene spec JSON so I can generate the Python scene class without parsing natural language.

**Acceptance Criteria:**
- [ ] Scene spec JSON contains: `scene_class_name`, `equations[]` (each with `latex`, `color`, `position`, `animation_type`), `text_blocks[]`, `axes_config` (if chart needed), `color_assignments{}`, `animation_sequence[]` (ordered list of steps with `type`, `target`, `duration`)
- [ ] Color assignments use brand palette constants: `GOLD`, `RED`, `GREEN`, `BLUE_NORM`, `ORANGE`, `PURPLE`, `TEAL`
- [ ] Equation latex strings validated: attempt `MathTex(latex)` parse check before storage (subprocess call)
- [ ] Each step in `animation_sequence` has: `step_number`, `type` (one of: `Write`, `FadeIn`, `Create`, `Transform`, `FadeOut`, `SurroundingRectangle`, `wait`), `target_id`, `duration_secs`, `notes`
- [ ] Scene spec validated against `ManımSceneSpec` Pydantic schema
- [ ] Stored in `scenes.manim_spec`
- [ ] Test: spec for "Delta" scene must contain `N(d_1)` equation, S-curve axes config, and ≥3 animation steps

---

### FEATURE F-01.5: Wan Storyboard Prompt Generator

**Description:** Qwen generates a text-to-video prompt for Wan/HappyHorse for the episode's character intro clip — a 5–15 second cinematic shot of the "quant analyst" host character.

**User Story US-01.5.1:**
> As the video compositor, I need a high-quality Wan prompt that generates a cinematic, on-brand character clip for the episode intro, so the video is Track 2 compliant.

**Acceptance Criteria:**
- [ ] One Wan prompt generated per episode (not per scene — cost control)
- [ ] Prompt structure: `[CHARACTER DESCRIPTION], [SETTING], [ACTION], [CAMERA], [LIGHTING], [STYLE], [DURATION: Xs]`
- [ ] Character: "a sharp, confident financial engineer in a modern trading floor setting, early 30s, intense expression, professional but edgy"
- [ ] Topic-specific setting: e.g. "surrounded by floating mathematical equations and stock charts" for quant topics
- [ ] Prompt length: 150–200 words (Wan optimal range)
- [ ] Negative prompt generated separately: "blurry, watermark, text artifacts, unrealistic proportions"
- [ ] Prompt stored in `episodes.wan_prompt`
- [ ] Test: assert prompt contains all 7 structural elements

---

### FEATURE F-01.6: SEO Metadata Generator

**Description:** Qwen generates the complete YouTube metadata package — SEO-optimised title, description, tags, chapter timestamps, pinned comment text — ready for upload.

**User Story US-01.6.1:**
> As the delivery pipeline, I need YouTube-ready metadata generated automatically so the upload step requires zero manual input.

**Acceptance Criteria:**
- [ ] Uses `qwen-turbo` (cost efficiency — metadata is low-stakes)
- [ ] Outputs: `youtube_title` (≤100 chars, keyword-front-loaded), `youtube_description` (≥300 chars, first 200 chars are hook), `tags[]` (25–30 tags, mix of broad and specific), `chapters[]` (timestamp + title, matching scene structure), `pinned_comment` (references list + challenge question)
- [ ] Title must include: topic keyword + "Explained" or "Derived" + "| Quantifaya Ep.N"
- [ ] Description must include: academic sources summary, book recommendations, challenge question
- [ ] Chapters auto-timestamped from `scenes.duration_secs` cumulative sum
- [ ] Stored in `episodes.seo_json`
- [ ] Test: title for "Heston Model" episode must contain "Heston" and "Quantifaya"

---

## EPIC EP-02: WAN VIDEO GENERATION LAYER

**Strategic Goal:** Integrate Wan/HappyHorse API to generate a cinematic character intro clip per episode — making the submission Track 2 compliant while keeping cost and complexity bounded.

**Capability Domain:** Generation

---

### FEATURE F-02.1: Wan API Client

**Description:** A Python client wrapping the Wan/HappyHorse video generation API with retry logic, polling, and local file download.

**User Story US-02.1.1:**
> As the orchestration agent, I need to submit a Wan generation job and receive a local MP4 file path when complete, so the compositor can use the clip without knowing Wan API internals.

**Acceptance Criteria:**
- [ ] `WanClient` class with methods: `submit_job(prompt, negative_prompt, duration_secs, resolution) -> job_id`, `poll_status(job_id) -> status`, `download_clip(job_id, output_path) -> Path`
- [ ] Poll interval: 10 seconds, max 20 polls (200 second timeout)
- [ ] On timeout: raise `WanTimeoutError`; orchestrator uses fallback (Manim title card)
- [ ] On success: download MP4 to `./output/wan/{episode_id}_intro.mp4`
- [ ] Resolution target: 1920×1080 or nearest supported
- [ ] Duration target: 8–12 seconds
- [ ] API key loaded from environment variable `WAN_API_KEY`
- [ ] All API calls logged with timestamp, job_id, prompt hash, status
- [ ] Unit test: mock Wan API, assert job submission and polling state machine work correctly
- [ ] Integration test (if Wan quota available): submit 5-second job, assert file downloaded and is valid MP4

---

### FEATURE F-02.2: Wan Fallback — Manim Cinematic Title Card

**Description:** If Wan is unavailable, rate-limited, or produces unusable output, a Manim-rendered cinematic title card serves as the intro clip.

**User Story US-02.2.1:**
> As the system operator, I need a graceful fallback when Wan is unavailable, so episode generation does not block on external API availability.

**Acceptance Criteria:**
- [ ] Fallback triggers on: `WanTimeoutError`, `WanAPIError`, or quality check failure
- [ ] Manim title card renders: episode title in gold, topic visualisation (animated equation from scene 1), Quantifaya logo, 8 seconds duration
- [ ] Fallback flag recorded in `episodes` table: `wan_fallback: true`
- [ ] Fallback output path follows same convention as Wan output: `./output/wan/{episode_id}_intro.mp4`
- [ ] Total fallback render time < 90 seconds
- [ ] Test: assert fallback produces valid 1920×1080 MP4 of ≥7 seconds

---

## EPIC EP-03: MANIM AUTOMATION ENGINE

**Strategic Goal:** Auto-generate and execute Manim Python scene classes from the structured scene specs produced by EP-01, without human code authorship per episode.

**Capability Domain:** Generation

---

### FEATURE F-03.1: Manim Code Generator from Scene Spec

**Description:** A code generation service that translates `ManımSceneSpec` JSON into a valid, executable Manim Python scene class using a template engine + Qwen for complex animation logic.

**User Story US-03.1.1:**
> As the Manim render engine, I need a Python file containing all scene classes for an episode, generated from scene specs, so I can render the episode without a human writing code.

**Acceptance Criteria:**
- [ ] Template engine: Jinja2 templates for common animation patterns (`FadeIn`, `Create`, `MathTex`, `Axes`, `FunctionGraph`)
- [ ] Template covers: ≥90% of standard scene types (equation reveal, axis + curve, comparison table, two-column layout, quote box)
- [ ] For non-template scenes (complex interactions): Qwen `qwen-max` generates the scene class Python code from spec JSON
- [ ] Generated code injected into `quantifaya_ep{N}.py` with: brand color constants, helper functions (`cite()`, `bs_delta()`, `bs_gamma()`, etc.), `FullEpisode` compositor class
- [ ] Before saving, generated code passed through `py_compile.compile()` — syntax error triggers Qwen retry
- [ ] Maximum 3 code generation retries per scene; on failure, scene replaced with fallback text card
- [ ] Generated file saved to `./output/scripts/quantifaya_ep{N}.py`
- [ ] Test: generate code for "Delta S-curve scene", execute `manim -ql` on it, assert MP4 produced

---

### FEATURE F-03.2: Manim Render Orchestrator

**Description:** Manages parallel rendering of all scene classes in an episode, tracking per-scene completion and assembling the ordered list of scene MP4 paths.

**User Story US-03.2.1:**
> As the ffmpeg compositor, I need an ordered list of scene MP4 file paths with durations, so I can concatenate them into the full episode without guessing file locations.

**Acceptance Criteria:**
- [ ] Renders each `Scene` class independently: `manim -pqh {file}.py {SceneClass} --fps 60`
- [ ] Maximum 4 parallel renders (CPU-bound; tunable via `MANIM_WORKERS` env var)
- [ ] Per-scene render timeout: 300 seconds; on timeout, use text card fallback
- [ ] On completion: extract actual duration using `ffprobe`
- [ ] Update `scenes.video_path` and `scenes.duration_secs` in PostgreSQL
- [ ] Produce ordered manifest: `[{"scene_number": 1, "path": "...", "duration": 92.4}, ...]`
- [ ] Test: render a known 3-scene episode, assert manifest contains 3 entries with correct paths

---

### FEATURE F-03.3: Equation Validation Service

**Description:** Pre-render validation that all LaTeX equations in a scene spec are parseable by Manim's `MathTex`, preventing render failures due to malformed LaTeX.

**User Story US-03.3.1:**
> As the render engine, I need to know before starting a render that all LaTeX in the scene spec is valid, so I don't waste 5 minutes of GPU time on a doomed render.

**Acceptance Criteria:**
- [ ] For each equation in `scene.manim_spec.equations[]`, spawn a minimal Manim headless check: `MathTex(latex_str)` in isolation
- [ ] Invalid LaTeX: flag equation, send to Qwen for correction, retry validation
- [ ] Maximum 2 correction rounds; if still invalid, replace with plain `Text()` equivalent
- [ ] Validation runs before render submission (blocking, fast — <30 seconds per scene)
- [ ] Validation results logged with pass/fail/corrected status
- [ ] Test: inject known-bad LaTeX `\frac{1}{0}{\sin}`, assert service catches and corrects

---

## EPIC EP-04: VOICE SYNTHESIS PIPELINE

**Strategic Goal:** Synthesize high-quality voice-over audio for every scene, synchronized to the Manim render duration, using edge-tts with a consistent voice persona.

**Capability Domain:** Generation

---

### FEATURE F-04.1: Scene Voice-Over Synthesizer

**Description:** Convert each scene's voice-over text to MP3/WAV audio using edge-tts, with consistent voice settings and pre-processing for equation pronunciation.

**User Story US-04.1.1:**
> As the compositor, I need a WAV file per scene with the correct spoken voice-over, so I can sync it to the Manim video frame-by-frame.

**Acceptance Criteria:**
- [ ] Voice: `en-US-GuyNeural` (authoritative male, matches Quantifaya persona) — configurable
- [ ] Speech rate: `-10%` (slightly slower than default for mathematical content)
- [ ] Before TTS: pre-processor replaces LaTeX with spoken equivalents: `$N(d_1)$` → `N of d one`, `$\frac{\partial C}{\partial S}$` → `partial C over partial S`
- [ ] Pre-processor uses a lookup table for common quant finance terms + Qwen fallback for unknown expressions
- [ ] Output: `./output/audio/{episode_id}/scene_{N}.wav`
- [ ] Duration of audio logged: `scenes.audio_duration_secs`
- [ ] Test: synthesize "Delta equals N of d one" scene text, assert WAV file > 0 bytes and duration > 1 second

---

### FEATURE F-04.2: Audio-Video Duration Alignment

**Description:** Ensure each scene's audio duration matches the Manim render duration, either by adjusting TTS speed or by inserting silence, so compositor sync is trivial.

**User Story US-04.2.1:**
> As the compositor, I need each scene's audio and video to be within 2 seconds of each other in duration, so ffmpeg sync does not produce audible gaps or cut-off speech.

**Acceptance Criteria:**
- [ ] Post-synthesis: compare `audio_duration` vs `video_duration` per scene
- [ ] If audio < video by > 2s: append silence padding to audio (ffmpeg `apad` filter)
- [ ] If audio > video by > 5s: regenerate Manim scene with extended `self.wait()` calls to match (add wait time proportionally distributed)
- [ ] If audio > video by 2–5s: adjust TTS rate: regenerate at `-15%` or `-20%` rate
- [ ] Alignment tolerance: ±2 seconds (acceptable for educational content)
- [ ] Alignment result logged per scene
- [ ] Test: inject mismatched pair (audio=120s, video=100s), assert padded output = 120s

---

## EPIC EP-05: LANGGRAPH ORCHESTRATION AGENT

**Strategic Goal:** A LangGraph directed acyclic graph that coordinates the full pipeline from topic to rendered video, with state management, parallel execution, error recovery, and a human-in-the-loop review gate.

**Capability Domain:** Orchestration

---

### FEATURE F-05.1: Episode Generation Graph Definition

**Description:** Define the LangGraph state graph with all nodes, edges, parallel branches, and conditional routing for the complete episode generation pipeline.

**User Story US-05.1.1:**
> As the system, I need a LangGraph graph that routes from topic input through intelligence, generation, composition, and delivery phases, with correct dependency management between nodes.

**Acceptance Criteria:**
- [ ] Graph state: `EpisodeState` TypedDict with fields: `episode_id`, `topic`, `outline`, `sources`, `script`, `manim_specs`, `wan_prompt`, `seo_metadata`, `scene_paths`, `wan_path`, `final_path`, `status`, `errors[]`
- [ ] Node definitions:
  - `analyze_topic` → calls F-01.1
  - `extract_sources` → calls F-01.2 (parallel per scene)
  - `generate_script` → calls F-01.3
  - `generate_manim_specs` → calls F-01.4 (parallel per scene)
  - `generate_wan_prompt` → calls F-01.5
  - `generate_seo` → calls F-01.6
  - `human_review_gate` → pause node (interrupt_before)
  - `synthesize_audio` → calls EP-04 (parallel per scene)
  - `generate_wan_clip` → calls EP-02
  - `render_manim_scenes` → calls EP-03 (parallel per scene)
  - `align_av` → calls F-04.2
  - `compose_episode` → calls EP-06
  - `upload_youtube` → calls EP-08
  - `mark_complete` → update DB
- [ ] Parallel edges: `extract_sources`, `generate_manim_specs` run after `analyze_topic` in parallel
- [ ] Parallel edges: `synthesize_audio`, `render_manim_scenes`, `generate_wan_clip` run after `human_review_gate` in parallel
- [ ] Error edges: any node failure routes to `handle_error` node which logs, retries (max 3), or routes to fallback
- [ ] State persisted to PostgreSQL at each node completion (for resumability)
- [ ] Test: compile graph, assert all nodes reachable, no cycles

---

### FEATURE F-05.2: Human Review Gate Implementation

**Description:** A pause point in the graph where the generated script and scene specs are surfaced for human review and optional editing before generation begins.

**User Story US-05.2.1:**
> As the content creator (G), I need to review and optionally edit the script before audio and video generation starts, so I can correct any persona drift or factual errors without regenerating everything.

**Acceptance Criteria:**
- [ ] Gate implemented as LangGraph `interrupt_before` on `synthesize_audio` node
- [ ] On interrupt: episode state serialized to JSON, stored in Redis with TTL 24 hours
- [ ] Notification: log message + (optional) email/webhook trigger
- [ ] Resume endpoint: `POST /api/v1/episodes/{id}/resume` with optional `{"script_edits": {...}}`
- [ ] If `script_edits` provided: apply edits to state before resuming
- [ ] If no edits needed: `POST /api/v1/episodes/{id}/resume` with empty body resumes immediately
- [ ] Gate can be disabled: `AUTO_APPROVE=true` env var bypasses gate for full automation (hackathon demo mode)
- [ ] Test: start episode, assert state paused at gate; call resume, assert pipeline continues

---

### FEATURE F-05.3: Error Recovery & Retry Logic

**Description:** Comprehensive error handling with per-node retry policies, fallback strategies, and partial resumption capability.

**User Story US-05.3.1:**
> As the pipeline operator, I need failed episodes to recover automatically where possible, and to resume from the last successful checkpoint when manual intervention is required, so generation time is not wasted.

**Acceptance Criteria:**
- [ ] Each node has retry policy: `max_retries: 3, backoff: exponential (2s, 4s, 8s)`
- [ ] Retriable errors: API timeout, rate limit (429), transient network error
- [ ] Non-retriable errors: invalid API key, Pydantic validation failure (requires human)
- [ ] On non-retriable: episode status set to `failed`, error logged to `jobs` table, alert raised
- [ ] Partial resumption: graph can restart from any completed node using persisted state
- [ ] Wan fallback (F-02.2) auto-triggered after Wan node exhausts retries
- [ ] Manim fallback (text card) auto-triggered after render node exhausts retries
- [ ] Test: mock API to fail twice then succeed, assert episode completes on 3rd attempt

---

## EPIC EP-06: FFMPEG COMPOSITION ENGINE

**Strategic Goal:** Compose the Wan intro clip, all Manim scene renders, and audio tracks into a single broadcast-quality MP4 with correct timing, transitions, and chapter markers.

**Capability Domain:** Orchestration

---

### FEATURE F-06.1: Scene-Level Audio-Video Sync

**Description:** For each scene, merge the Manim video with its corresponding audio track into a synced scene clip.

**User Story US-06.1.1:**
> As the episode compositor, I need each scene clip to have its audio and video perfectly synced from frame 0, so the final episode has no drift.

**Acceptance Criteria:**
- [ ] ffmpeg command per scene: `ffmpeg -i {video} -i {audio} -c:v copy -c:a aac -shortest {output}`
- [ ] Output: `./output/scenes/{episode_id}/scene_{N}_synced.mp4`
- [ ] Post-sync: verify output duration within ±0.5s of video duration using ffprobe
- [ ] On verification failure: retry with `async` audio mode
- [ ] All scene syncs run in parallel (ThreadPoolExecutor, max 4 workers)
- [ ] Test: assert synced output contains both video and audio streams

---

### FEATURE F-06.2: Episode Concatenation

**Description:** Concatenate the Wan intro clip followed by all synced scene clips into the complete episode file.

**User Story US-06.2.1:**
> As the delivery pipeline, I need a single 1080p60 MP4 of the complete episode, starting with the Wan intro and followed by all Manim scenes in order.

**Acceptance Criteria:**
- [ ] Build ffmpeg concat manifest: `file 'wan_intro.mp4'\nfile 'scene_1_synced.mp4'\n...`
- [ ] ffmpeg concat command: `ffmpeg -f concat -safe 0 -i manifest.txt -c copy {output}`
- [ ] Brand intro card (5s static Manim render of Quantifaya logo) prepended before Wan clip
- [ ] Brand outro card (5s) appended after final scene
- [ ] Output: `./output/episodes/{episode_id}/quantifaya_ep{N}_final.mp4`
- [ ] Output validated: resolution 1920×1080, fps 60, duration matches sum of component durations ±5s
- [ ] File size logged (expected: 2–6 GB for 25-min 1080p60)
- [ ] Test: concat 3 dummy clips, assert output contains all 3 in order via ffprobe stream inspection

---

### FEATURE F-06.3: Subtitle & Chapter Track Generation

**Description:** Embed SRT subtitles (from voice-over text + TTS timing) and chapter markers into the final MP4.

**User Story US-06.3.1:**
> As the YouTube uploader, I need the video to have embedded subtitles and chapter markers so YouTube can auto-detect them, improving accessibility and SEO.

**Acceptance Criteria:**
- [ ] SRT generation: use TTS word-timing data (from edge-tts `--words-in-cues` mode) to produce scene-level SRT file
- [ ] Chapter markers: derived from cumulative scene timestamps, formatted as YouTube chapter string in description
- [ ] Subtitles embedded in MP4: `ffmpeg -i {video} -i {srt} -c copy -c:s mov_text {output}`
- [ ] Chapter string auto-prepended to YouTube description field
- [ ] Test: assert SRT file has ≥10 cues for a 2-min scene

---

## EPIC EP-07: FASTAPI BACKEND & JOB QUEUE

**Strategic Goal:** A production-grade REST API that exposes the AutoDirector pipeline, manages async job execution via Celery + Redis, and persists all state to PostgreSQL.

**Capability Domain:** Orchestration

---

### FEATURE F-07.1: Episode Management API

**Description:** REST endpoints for creating, monitoring, and managing episode generation jobs.

**User Story US-07.1.1:**
> As the demo operator, I need a REST API I can call to trigger episode generation and check status, so I can demonstrate the pipeline live to hackathon judges.

**Acceptance Criteria:**
- [ ] `POST /api/v1/episodes` — create episode: `{"topic": str, "episode_number": int}`; returns `episode_id`
- [ ] `GET /api/v1/episodes/{id}` — get episode status and metadata
- [ ] `GET /api/v1/episodes/{id}/script` — get generated script JSON
- [ ] `POST /api/v1/episodes/{id}/resume` — resume after human gate
- [ ] `GET /api/v1/episodes/{id}/progress` — SSE stream of progress events (for dashboard)
- [ ] `GET /api/v1/episodes` — list all episodes with status
- [ ] `DELETE /api/v1/episodes/{id}` — cancel and clean up
- [ ] All endpoints return JSON with: `status`, `data`, `errors[]`, `timestamp`
- [ ] Authentication: API key header `X-API-Key` (single key for MVP)
- [ ] Test: full CRUD cycle via pytest + httpx

---

### FEATURE F-07.2: Celery Job Queue Integration

**Description:** Async job execution for all compute-heavy tasks (Manim renders, Wan calls, TTS synthesis) via Celery workers backed by Redis.

**User Story US-07.2.1:**
> As the system architect, I need long-running tasks to execute asynchronously so the API remains responsive and multiple episodes can generate concurrently.

**Acceptance Criteria:**
- [ ] Celery workers: 4 workers, each handling one task at a time
- [ ] Task types: `render_scene`, `synthesize_audio`, `generate_wan`, `compose_episode`, `upload_youtube`
- [ ] Task priority queue: `wan_generate` and `upload` at high priority; `render_scene` at normal
- [ ] Task result backend: Redis
- [ ] Task state mirrored to PostgreSQL `jobs` table on completion/failure
- [ ] Dead letter queue: failed tasks after max retries moved to `jobs` table with `status='dead'`
- [ ] Flower monitoring: `http://localhost:5555` for Celery task inspection
- [ ] Test: submit 3 render tasks, assert all 3 complete concurrently within timeout

---

## EPIC EP-08: DELIVERY & YOUTUBE INTEGRATION

**Strategic Goal:** Automatically upload the completed episode to YouTube with all metadata, set as unlisted for review, and notify the creator.

**Capability Domain:** Delivery

---

### FEATURE F-08.1: YouTube Upload Service

**Description:** Upload the final MP4 and all metadata to YouTube using the Data API v3.

**User Story US-08.1.1:**
> As the content creator, I need the completed video to be automatically uploaded to YouTube with the correct title, description, tags, and thumbnail, so the only remaining step is changing from unlisted to public.

**Acceptance Criteria:**
- [ ] Uses YouTube Data API v3 with OAuth 2.0 (service account or user OAuth)
- [ ] Upload: `videos.insert` with `snippet.title`, `snippet.description`, `snippet.tags`, `status.privacyStatus='unlisted'`
- [ ] Thumbnail: `thumbnails.set` with PIL-generated 1280×720 JPEG
- [ ] Playlist: auto-add to "Quantifaya" playlist if exists
- [ ] On success: store `youtube_id` in `episodes` table, log URL
- [ ] On failure: retry 3×; on persistent failure, save to `./output/upload_failed/` and alert
- [ ] Test: mock YouTube API, assert upload called with correct metadata fields

---

### FEATURE F-08.2: Thumbnail Generator

**Description:** Programmatically generate a YouTube thumbnail using PIL that matches the Quantifaya brand and episode topic.

**User Story US-08.2.1:**
> As the channel, I need a high-CTR thumbnail that's brand-consistent, shows the episode topic, and is generated automatically without Canva.

**Acceptance Criteria:**
- [ ] Size: 1280×720 JPEG, sRGB
- [ ] Layout: dark background (#0D1117), topic keyword in gold large font, episode-specific equation in white medium font, Quantifaya logo bottom-right, decorative math symbols scattered
- [ ] Font: download and use "Fira Code" or "JetBrains Mono" for equations
- [ ] Topic keyword extracted from `seo_json.youtube_title`
- [ ] Key equation pulled from scene 1 of `episodes.manim_spec`
- [ ] Output: `./output/thumbnails/{episode_id}.jpg`
- [ ] Test: generate thumbnail for topic "Heston Model", assert file size > 50KB and dimensions = 1280×720

---

## EPIC EP-09: DEMO DASHBOARD (HACKATHON SUBMISSION)

**Strategic Goal:** A minimal React dashboard that demonstrates the full pipeline to hackathon judges — live progress, script preview, video preview, and architecture diagram.

**Capability Domain:** Delivery

---

### FEATURE F-09.1: Live Pipeline Dashboard

**Description:** A single-page React app showing the current episode's generation progress, with real-time updates via SSE.

**User Story US-09.1.1:**
> As a hackathon judge, I need to see the pipeline running in real-time, with each stage's status visible, so I can evaluate the depth of the automation.

**Acceptance Criteria:**
- [ ] Input: text box for "Topic" + "Episode Number" + "Generate" button
- [ ] Pipeline stages displayed as a vertical flow: Intelligence → Generation → Composition → Delivery
- [ ] Each stage: status indicator (⏳ pending / 🔄 running / ✅ done / ❌ failed), elapsed time
- [ ] Live script preview: as scenes are generated, script text streams in
- [ ] Wan clip preview: thumbnail of generated clip when available
- [ ] Final video player: embedded video player when composition complete
- [ ] Architecture diagram tab: static SVG of the full system architecture
- [ ] Dark theme, Quantifaya brand colours, minimal design
- [ ] SSE endpoint: `GET /api/v1/episodes/{id}/progress` (text/event-stream)
- [ ] Test: mock SSE stream, assert each stage update renders in UI

---

## EPIC EP-10: PRODUCTION HARDENING & DEPLOYMENT

**Strategic Goal:** Docker Compose deployment to Contabo VPS, with environment configuration, secrets management, and operational readiness for daily episode production.

**Capability Domain:** Delivery

---

### FEATURE F-10.1: Docker Compose Stack

**Description:** Complete Docker Compose configuration for all services.

**User Story US-10.1.1:**
> As the DevOps engineer, I need a single `docker-compose up` command to start the complete AutoDirector stack, so deployment to any environment is reproducible.

**Acceptance Criteria:**
- [ ] Services: `api` (FastAPI), `worker` (Celery ×4), `redis`, `postgres`, `flower`, `frontend` (React/nginx)
- [ ] Volume mounts: `./output` for rendered files, `./secrets` for API keys
- [ ] Health checks: all services have `healthcheck` configured
- [ ] Environment file: `.env.example` with all required vars documented
- [ ] Required env vars: `QWEN_API_KEY`, `WAN_API_KEY`, `YOUTUBE_CLIENT_SECRET`, `POSTGRES_PASSWORD`, `REDIS_URL`, `AUTO_APPROVE`
- [ ] Resource limits: `worker` containers limited to 4 CPU, 8GB RAM each (Manim is hungry)
- [ ] Test: `docker-compose up --build`, assert all services healthy within 90 seconds

---

### FEATURE F-10.2: Nginx Reverse Proxy & HTTPS

**Description:** Nginx configuration for the Contabo VPS deployment, with HTTPS via Let's Encrypt.

**Acceptance Criteria:**
- [ ] Nginx config: proxy `/api` to FastAPI on port 8000, `/` to React on port 3000, `/flower` to Flower on port 5555
- [ ] HTTPS: Let's Encrypt cert via Certbot (or use existing crm.favitech.co.ke cert pattern)
- [ ] Rate limiting: `/api/v1/episodes` (POST) limited to 10 req/hour per IP
- [ ] Static file serving: `/output/episodes/` served directly by Nginx (bypass API for large MP4 files)
- [ ] Test: `curl https://{domain}/api/v1/health` returns 200

---

---

## PART III: SPRINT PLAN

### HACKATHON SPRINT (7 Days — to July 9, 2026)

```
DAY 1 (July 3)  — Foundation
  ✦ EP-07: FastAPI skeleton + PostgreSQL schema + Redis setup
  ✦ EP-01: F-01.1 (Topic Analysis) + F-01.3 (Script Generator) working end-to-end
  ✦ Deliverable: `POST /api/v1/episodes` → generates script for a topic

DAY 2 (July 4)  — Intelligence Complete
  ✦ EP-01: F-01.2 (Sources) + F-01.4 (Manim Specs) + F-01.5 (Wan Prompt) + F-01.6 (SEO)
  ✦ EP-05: F-05.1 (LangGraph graph definition) — nodes wired, not all implemented
  ✦ Deliverable: Full intelligence phase produces all JSON artifacts for an episode

DAY 3 (July 5)  — Generation Layer
  ✦ EP-03: F-03.1 (Manim Code Generator) + F-03.2 (Render Orchestrator)
  ✦ EP-04: F-04.1 (TTS Synthesizer) + F-04.2 (Duration Alignment)
  ✦ EP-02: F-02.1 (Wan API Client) — even if Wan account pending, client coded
  ✦ Deliverable: Scene MP4s + WAV files generated from spec JSON

DAY 4 (July 6)  — Composition & Delivery
  ✦ EP-06: F-06.1 (Scene sync) + F-06.2 (Episode concat) + F-06.3 (Subtitles)
  ✦ EP-08: F-08.1 (YouTube upload) + F-08.2 (Thumbnail)
  ✦ Deliverable: First end-to-end run — topic → uploaded YouTube video (unlisted)

DAY 5 (July 7)  — Orchestration & Human Gate
  ✦ EP-05: F-05.2 (Human gate) + F-05.3 (Error recovery)
  ✦ EP-07: F-07.2 (Celery workers) — async job queue live
  ✦ Deliverable: Pipeline runs fully async, gate tested, retries tested

DAY 6 (July 8)  — Demo Dashboard + Hardening
  ✦ EP-09: F-09.1 (React dashboard) — live progress display
  ✦ EP-10: F-10.1 (Docker Compose) + F-10.2 (Nginx)
  ✦ Run full pipeline on "Heston Model" topic — generate real episode
  ✦ Deliverable: Deployed, accessible demo URL

DAY 7 (July 9)  — Submission Day
  ✦ Devpost writeup: architecture diagram, demo video, GitHub link
  ✦ Record 3-minute demo walkthrough video
  ✦ Submit by 11:59 PM deadline
```

### MINIMUM VIABLE DEMO (if time-constrained — Day 4 deliverable)

If the full pipeline is not ready by Day 6, the MVP submission demonstrates:
1. Qwen generates a full script for "The Greeks" in Quantifaya persona (live)
2. Manim renders 3 scenes from auto-generated code (live or pre-recorded)
3. Wan intro clip plays (pre-generated or from API call)
4. ffmpeg stitches them into a 5-minute preview video
5. Dashboard shows pipeline stages with green checkmarks

This is Track 2 compliant (Wan + LLM + programmatic animation) and defensible on all judging criteria.

---

## PART IV: ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    QUANTIFAYA AUTODIRECTOR                              │
│                    System Architecture v1.0                             │
└─────────────────────────────────────────────────────────────────────────┘

  INPUT: "Topic String"
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│  FastAPI Backend  (port 8000)                           │
│  POST /api/v1/episodes  →  Create episode + queue job  │
└──────────────────────────┬──────────────────────────────┘
                           │ enqueue
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Redis Job Queue + Celery Workers (×4)                  │
└──────────────────────────┬──────────────────────────────┘
                           │ execute
                           ▼
┌─────────────────────────────────────────────────────────┐
│  LangGraph Orchestration Agent                          │
│                                                          │
│  ┌──────────┐    ┌─────────────┐    ┌────────────────┐ │
│  │ Phase 1  │    │  Phase 2    │    │   Phase 3      │ │
│  │Qwen Cloud│───▶│ Parallel    │───▶│ Composition    │ │
│  │Intelligence│  │ Generation  │    │ (ffmpeg)       │ │
│  └──────────┘    └─────────────┘    └────────────────┘ │
│       │               │                    │            │
│  qwen-max         [A] Wan API          concat MP4s      │
│  qwen-turbo       [B] Manim render     sync A/V         │
│  qwen-vl          [C] edge-tts         add subtitles    │
│                   (parallel)           brand cards      │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼──────────────────┐
          ▼                ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│  PostgreSQL   │  │     Redis    │  │  File System     │
│  episodes     │  │  job state   │  │  ./output/       │
│  scenes       │  │  SSE events  │  │    wan/          │
│  jobs         │  │              │  │    scenes/       │
└──────────────┘  └──────────────┘  │    audio/        │
                                     │    episodes/     │
                                     │    thumbnails/   │
                                     └──────────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ YouTube Data API │
                  │ Auto-upload      │
                  │ Metadata set     │
                  │ Unlisted publish │
                  └──────────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  React Dashboard │
                  │  (port 3000)     │
                  │  Live SSE feed   │
                  │  Video preview   │
                  └──────────────────┘
```

---

## PART V: FILE STRUCTURE

```
quantifaya-autodirector/
├── README.md
├── docker-compose.yml
├── .env.example
├── nginx/
│   └── nginx.conf
│
├── backend/
│   ├── main.py                    # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── episodes.py
│   │   │   ├── health.py
│   │   │   └── stream.py          # SSE endpoint
│   │   └── middleware.py
│   │
│   ├── core/
│   │   ├── config.py              # env var loading
│   │   ├── database.py            # SQLAlchemy setup
│   │   └── redis_client.py
│   │
│   ├── models/
│   │   ├── episode.py             # SQLAlchemy models
│   │   ├── scene.py
│   │   └── job.py
│   │
│   ├── schemas/
│   │   ├── episode_outline.py     # Pydantic schemas
│   │   ├── scene_spec.py
│   │   ├── manim_scene_spec.py
│   │   └── seo_metadata.py
│   │
│   ├── services/
│   │   ├── intelligence/
│   │   │   ├── qwen_client.py     # Qwen API wrapper
│   │   │   ├── outline_generator.py
│   │   │   ├── source_extractor.py
│   │   │   ├── script_generator.py
│   │   │   ├── manim_spec_generator.py
│   │   │   ├── wan_prompt_generator.py
│   │   │   └── seo_generator.py
│   │   │
│   │   ├── generation/
│   │   │   ├── wan_client.py      # Wan/HappyHorse API
│   │   │   ├── manim_codegen.py   # Jinja2 + Qwen code gen
│   │   │   ├── manim_renderer.py  # subprocess orchestration
│   │   │   ├── equation_validator.py
│   │   │   ├── tts_synthesizer.py # edge-tts wrapper
│   │   │   └── av_aligner.py
│   │   │
│   │   ├── composition/
│   │   │   ├── scene_syncer.py    # per-scene A/V merge
│   │   │   ├── episode_compositor.py  # concat
│   │   │   └── subtitle_generator.py
│   │   │
│   │   └── delivery/
│   │       ├── youtube_uploader.py
│   │       └── thumbnail_generator.py
│   │
│   ├── orchestration/
│   │   ├── graph.py               # LangGraph definition
│   │   ├── nodes.py               # Node implementations
│   │   ├── state.py               # EpisodeState TypedDict
│   │   └── error_handlers.py
│   │
│   └── workers/
│       ├── celery_app.py
│       └── tasks.py
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── components/
│       │   ├── PipelineFlow.jsx   # visual DAG of stages
│       │   ├── ScriptPreview.jsx
│       │   ├── VideoPlayer.jsx
│       │   └── ArchDiagram.jsx
│       └── hooks/
│           └── useSSE.js
│
├── manim_templates/
│   ├── base_template.py.j2        # Jinja2 base Manim file
│   ├── equation_reveal.py.j2
│   ├── axes_curve.py.j2
│   ├── comparison_table.py.j2
│   ├── two_column.py.j2
│   └── quote_box.py.j2
│
├── brand/
│   ├── intro_card.py              # Static Manim brand intro
│   ├── outro_card.py
│   └── assets/
│       └── quantifaya_logo.svg
│
├── output/                        # gitignored
│   ├── wan/
│   ├── scenes/
│   ├── audio/
│   ├── episodes/
│   └── thumbnails/
│
└── tests/
    ├── unit/
    │   ├── test_outline_generator.py
    │   ├── test_script_generator.py
    │   ├── test_manim_codegen.py
    │   ├── test_wan_client.py
    │   └── test_compositor.py
    └── integration/
        ├── test_pipeline_e2e.py
        └── test_youtube_upload.py
```

---

## PART VI: DEVPOST SUBMISSION TEMPLATE

```markdown
## Project Name
Quantifaya AutoDirector — Autonomous AI Showrunner for Quantitative Finance

## What It Does
AutoDirector takes a financial engineering topic as input and autonomously 
produces a fully-synced, publication-ready YouTube video as output — with 
zero human intervention between intent and render.

It orchestrates four AI systems simultaneously:
- **Qwen Cloud** writes the script in the Quantifaya persona (Taylor+Axe+Taleb)
- **Wan/HappyHorse** generates cinematic character footage for the episode intro
- **Manim** renders verified mathematical animations for every equation
- **edge-tts** synthesizes the voice-over, synced to each scene

A LangGraph agent coordinates the pipeline. ffmpeg composes the final video.
YouTube Data API publishes it.

## Qwen Cloud Integration
- `qwen-max`: Full 25-minute script generation with persona enforcement
- `qwen-turbo`: SEO metadata, chapter generation, source validation
- `qwen-vl`: Storyboard analysis and thumbnail quality review
- Wan/HappyHorse: Character intro footage generation

## Technical Architecture
[Link to arch diagram]

## Demo
[Link to demo video]
[Link to generated episode example on YouTube]

## GitHub
[Link to repo]

## What Makes This Different
Most Track 2 submissions chain Wan calls to generate drama footage.
AutoDirector does that — and then adds a layer of mathematical precision 
no diffusion model can match. The result is genuinely educational content 
with cinematic production values, accurate derivations, and real academic 
citations. Built for a real YouTube channel with a real daily production 
requirement.
```

---

## PART VII: ACCEPTANCE TEST SUITE (End-to-End)

**Test: Full Pipeline on "Heston Stochastic Volatility" topic**

```
Step 1: POST /api/v1/episodes {"topic": "Heston Stochastic Volatility Model", "episode_number": 5}
Assert: 201 response, episode_id returned

Step 2: GET /api/v1/episodes/{id} 
Assert: status = "outlining"

Step 3: Wait for status = "awaiting_review" (≤5 min)
Assert: script_json contains ≥8 scenes
Assert: sources_json contains Heston (1993) reference
Assert: wan_prompt generated

Step 4: POST /api/v1/episodes/{id}/resume
Assert: status transitions to "generating"

Step 5: Wait for status = "compositing" (≤30 min)
Assert: ./output/wan/{id}_intro.mp4 exists
Assert: ./output/scenes/{id}/scene_*_synced.mp4 count ≥8

Step 6: Wait for status = "delivered" (≤10 min)
Assert: ./output/episodes/{id}/quantifaya_ep5_final.mp4 exists
Assert: Duration 1350–1650 seconds
Assert: Resolution 1920×1080
Assert: youtube_id populated in DB

Step 7: Check YouTube (manual)
Assert: Video accessible at https://youtube.com/watch?v={youtube_id}
Assert: Title contains "Heston"
Assert: Description contains academic references
Assert: Thumbnail uploaded
```

**Pass criteria:** All 7 steps pass. Total wall-clock time ≤ 60 minutes.
```
