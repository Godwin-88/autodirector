# QUANTIFAYA AUTODIRECTOR — CODING AGENT KICKSTART PROMPT
# Copy this entire prompt into Claude Code, Cursor, or your agentic coding tool of choice.
# Paste it as the first message after `git init` on a fresh repo.

---

## PROMPT

You are a senior full-stack AI engineer. You are building **Quantifaya AutoDirector** — a production-grade autonomous video generation pipeline that takes a topic string as input and outputs a fully rendered, uploaded YouTube video with zero human steps between them.

This is a **Qwen Cloud Hackathon Track 2 submission** due July 9, 2026. The pipeline must be demonstrably end-to-end by Day 4 (July 6). Treat every architectural decision as production-first, not demo-first.

---

### WHAT YOU ARE BUILDING

A FastAPI + LangGraph + Celery system with four capability domains:

1. **Intelligence** — Qwen Cloud API writes episode scripts in a defined persona, extracts academic sources, generates Manim scene specs as JSON, creates Wan video prompts, and writes SEO metadata
2. **Generation** — Wan/HappyHorse API generates character intro footage; Manim renders mathematical animation scenes from auto-generated Python; edge-tts synthesises voice-over audio per scene
3. **Orchestration** — LangGraph directed graph coordinates the full pipeline with parallel execution, a human-in-the-loop review gate, and retry/fallback logic; Celery + Redis handles async job execution
4. **Delivery** — ffmpeg composes Wan intro + Manim scenes + audio into a single 1080p60 MP4; YouTube Data API v3 uploads with full metadata; PIL generates thumbnails

---

### YOUR FIRST TASK — DO THIS NOW, IN THIS ORDER

**Do not ask for clarification. Execute sequentially. Commit after each phase completes.**

---

#### PHASE 0: REPO SCAFFOLD (commit: `chore: initial scaffold`)

Create the following directory structure exactly. Every `__init__.py` must be empty but present.

```
quantifaya-autodirector/
├── backend/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   ├── intelligence/
│   │   ├── generation/
│   │   ├── composition/
│   │   └── delivery/
│   ├── orchestration/
│   └── workers/
├── frontend/
│   └── src/
│       └── components/
├── manim_templates/
├── brand/
│   └── assets/
├── output/
│   ├── wan/
│   ├── scenes/
│   ├── audio/
│   ├── episodes/
│   └── thumbnails/
├── tests/
│   ├── unit/
│   └── integration/
└── nginx/
```

Create these root files with the content specified below:

**`.gitignore`** — include: `output/`, `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `*.mp4`, `*.wav`, `*.mp3`, `node_modules/`

**`.env.example`**:
```
# Qwen Cloud
QWEN_API_KEY=your_qwen_api_key
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# Wan / HappyHorse Video Generation
WAN_API_KEY=your_wan_api_key
WAN_API_BASE_URL=https://dashscope.aliyuncs.com/api/v1

# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=autodirector
POSTGRES_USER=autodirector
POSTGRES_PASSWORD=changeme

# Redis
REDIS_URL=redis://redis:6379/0

# YouTube
YOUTUBE_CLIENT_SECRETS_FILE=./secrets/youtube_client_secrets.json
YOUTUBE_CHANNEL_ID=your_channel_id

# Pipeline config
AUTO_APPROVE=false
MANIM_WORKERS=4
MANIM_QUALITY=h
LOG_LEVEL=INFO
```

**`docker-compose.yml`**:
```yaml
version: "3.9"
services:
  api:
    build: ./backend
    ports: ["8000:8000"]
    env_file: .env
    volumes:
      - ./output:/app/output
      - ./secrets:/app/secrets
      - ./manim_templates:/app/manim_templates
    depends_on: [postgres, redis]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  worker:
    build: ./backend
    command: celery -A workers.celery_app worker --loglevel=info --concurrency=4
    env_file: .env
    volumes:
      - ./output:/app/output
      - ./manim_templates:/app/manim_templates
    depends_on: [postgres, redis]
    deploy:
      resources:
        limits:
          cpus: "4"
          memory: 8G

  flower:
    build: ./backend
    command: celery -A workers.celery_app flower --port=5555
    ports: ["5555:5555"]
    env_file: .env
    depends_on: [redis]

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: autodirector
      POSTGRES_USER: autodirector
      POSTGRES_PASSWORD: changeme
    volumes: [postgres_data:/var/lib/postgresql/data]
    ports: ["5433:5432"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U autodirector"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports: ["6380:6379"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s

volumes:
  postgres_data:
```

**`backend/requirements.txt`**:
```
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
alembic==1.13.1
asyncpg==0.29.0
psycopg2-binary==2.9.9
pydantic==2.7.1
pydantic-settings==2.2.1
celery==5.4.0
redis==5.0.4
flower==2.0.1
httpx==0.27.0
openai==1.30.0
langgraph==0.1.5
langchain-core==0.2.7
edge-tts==6.1.10
manim==0.18.1
Pillow==10.3.0
jinja2==3.1.4
google-api-python-client==2.131.0
google-auth-oauthlib==1.2.0
python-multipart==0.0.9
sse-starlette==2.1.0
tenacity==8.3.0
structlog==24.1.0
pytest==8.2.2
pytest-asyncio==0.23.7
httpx==0.27.0
```

**`backend/Dockerfile`**:
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    python3-dev \
    gcc \
    texlive-latex-extra \
    texlive-fonts-extra \
    dvipng \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

#### PHASE 1: CORE INFRASTRUCTURE (commit: `feat: core config, db, redis`)

**`backend/core/config.py`**:
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    qwen_api_key: str
    qwen_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    wan_api_key: str = ""
    wan_api_base_url: str = "https://dashscope.aliyuncs.com/api/v1"
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "autodirector"
    postgres_user: str = "autodirector"
    postgres_password: str
    redis_url: str = "redis://redis:6379/0"
    youtube_client_secrets_file: str = "./secrets/youtube_client_secrets.json"
    youtube_channel_id: str = ""
    auto_approve: bool = False
    manim_workers: int = 4
    manim_quality: str = "h"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")

    @property
    def sync_database_url(self) -> str:
        return (f"postgresql://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

**`backend/core/database.py`** — SQLAlchemy async engine, `get_db` dependency, `Base` declarative base. Use `asyncpg` driver. Expose `async_engine`, `AsyncSessionLocal`, `Base`, `get_db`.

**`backend/core/redis_client.py`** — Redis client using `redis.asyncio`. Expose `get_redis()` as async context manager.

**`backend/core/logging.py`** — structlog configuration. JSON output in production, console in development. Expose `get_logger(name: str)`.

---

#### PHASE 2: DATABASE MODELS + MIGRATIONS (commit: `feat: sqlalchemy models and alembic`)

Create SQLAlchemy models in `backend/models/`. Each model in its own file. Use UUID primary keys (`uuid4`), all timestamps as `TIMESTAMPTZ`.

**`backend/models/episode.py`**:
```python
# Fields: id (UUID PK), topic (Text), episode_number (Integer nullable),
# series (Text default "quantifaya"), status (Text default "pending"),
# wan_fallback (Boolean default False),
# script_json (JSONB), sources_json (JSONB), seo_json (JSONB),
# wan_prompt (Text), output_path (Text), youtube_id (Text),
# duration_secs (Integer), created_at (TIMESTAMPTZ now), completed_at (TIMESTAMPTZ)
# status enum values: pending|outlining|scripting|awaiting_review|generating|compositing|delivered|failed
```

**`backend/models/scene.py`**:
```python
# Fields: id (UUID PK), episode_id (UUID FK → episodes.id CASCADE DELETE),
# scene_number (Integer), scene_class (Text), voiceover_text (Text),
# manim_spec (JSONB), wan_prompt (Text nullable),
# audio_path (Text), video_path (Text), synced_path (Text),
# audio_duration_secs (Float), video_duration_secs (Float),
# status (Text default "pending")
```

**`backend/models/job.py`**:
```python
# Fields: id (UUID PK), episode_id (UUID FK → episodes.id),
# job_type (Text), payload (JSONB), status (Text default "queued"),
# attempts (Integer default 0), max_retries (Integer default 3),
# error_msg (Text), celery_task_id (Text),
# created_at (TIMESTAMPTZ now), completed_at (TIMESTAMPTZ)
# job_type enum: wan_generate|manim_render|tts_synthesize|compose|upload
```

**`backend/models/__init__.py`** — import all models so Alembic sees them.

Initialise Alembic: `alembic init alembic` inside `backend/`. Configure `alembic.ini` to use `settings.sync_database_url`. Create initial migration. **Do not auto-migrate on startup — migrations run explicitly.**

---

#### PHASE 3: PYDANTIC SCHEMAS (commit: `feat: pydantic schemas`)

Create all schemas in `backend/schemas/`. These are the contracts between pipeline stages.

**`backend/schemas/episode_outline.py`**:
```python
from pydantic import BaseModel
from typing import List

class SceneOutlineItem(BaseModel):
    scene_number: int
    scene_class_name: str        # e.g. "SceneDelta"
    title: str
    duration_target_secs: int
    key_equations: List[str]     # LaTeX strings
    key_sources: List[str]       # "Author (Year)" format
    voiceover_hint: str          # 1-sentence description of what to say

class EpisodeOutline(BaseModel):
    topic: str
    episode_number: int
    series: str
    seo_title: str
    scenes: List[SceneOutlineItem]

    @property
    def total_duration_target(self) -> int:
        return sum(s.duration_target_secs for s in self.scenes)
```

**`backend/schemas/source.py`**:
```python
class AcademicSource(BaseModel):
    ref_number: int
    authors: str
    year: int
    title: str
    journal_or_publisher: str
    doi_or_url: str = ""
    scene_usage_note: str
    confidence: str = "high"     # high|low — low = flagged for human review

class SourcesPackage(BaseModel):
    episode_topic: str
    sources: List[AcademicSource]
```

**`backend/schemas/manim_spec.py`**:
```python
class EquationSpec(BaseModel):
    id: str                          # e.g. "eq_001"
    latex: str
    color: str = "FG"                # brand color constant name
    position: str = "center"         # center|top|bottom|left|right
    animation_type: str = "Write"    # Write|FadeIn|Transform

class TextBlockSpec(BaseModel):
    id: str
    content: str
    color: str = "FG"
    font_size: int = 24
    weight: str = "normal"           # normal|BOLD
    slant: str = "normal"            # normal|ITALIC

class AxesConfig(BaseModel):
    x_range: List[float]
    y_range: List[float]
    x_label: str
    y_label: str
    x_length: float = 10.0
    y_length: float = 5.0

class AnimationStep(BaseModel):
    step_number: int
    type: str    # Write|FadeIn|Create|Transform|FadeOut|SurroundingRectangle|wait|FadeInFromLeft
    target_id: str
    duration_secs: float = 0.5
    notes: str = ""

class ManımSceneSpec(BaseModel):
    scene_class_name: str
    equations: List[EquationSpec] = []
    text_blocks: List[TextBlockSpec] = []
    axes_config: Optional[AxesConfig] = None
    animation_sequence: List[AnimationStep]
    cite_string: str = ""
    background_color: str = "#0D1117"
```

**`backend/schemas/seo.py`**:
```python
class ChapterMark(BaseModel):
    timestamp: str           # "00:00"
    title: str

class SEOMetadata(BaseModel):
    youtube_title: str       # ≤100 chars
    youtube_description: str # ≥300 chars
    tags: List[str]          # 25-30 tags
    chapters: List[ChapterMark]
    pinned_comment: str
```

**`backend/schemas/episode_state.py`**:
```python
# LangGraph state — TypedDict, not Pydantic
from typing import TypedDict, Optional, List, Dict, Any

class EpisodeState(TypedDict):
    episode_id: str
    topic: str
    episode_number: int
    series: str
    outline: Optional[Dict[str, Any]]
    sources: Optional[Dict[str, Any]]
    script: Optional[Dict[str, Any]]
    manim_specs: Optional[List[Dict[str, Any]]]
    wan_prompt: Optional[str]
    seo_metadata: Optional[Dict[str, Any]]
    scene_video_paths: Optional[List[str]]
    scene_audio_paths: Optional[List[str]]
    scene_synced_paths: Optional[List[str]]
    wan_clip_path: Optional[str]
    final_video_path: Optional[str]
    youtube_id: Optional[str]
    wan_fallback: bool
    errors: List[str]
    current_phase: str
```

---

#### PHASE 4: QWEN CLIENT + INTELLIGENCE SERVICES (commit: `feat: qwen client and intelligence layer`)

**`backend/services/intelligence/qwen_client.py`**:

Wrap the OpenAI-compatible Qwen endpoint. The base URL is `settings.qwen_base_url`. Use `openai.AsyncOpenAI(api_key=settings.qwen_api_key, base_url=settings.qwen_base_url)`.

Implement:
```python
class QwenClient:
    async def complete(self, model: str, messages: List[dict], 
                       temperature: float = 0.7, max_tokens: int = 4096,
                       response_format: Optional[dict] = None) -> str:
        # Returns content string. Retries 3x with exponential backoff on rate limit.
        # Logs every call: model, prompt_tokens, completion_tokens, latency_ms

    async def complete_json(self, model: str, messages: List[dict],
                            temperature: float = 0.3) -> dict:
        # Same as complete() but parses JSON response.
        # Strips ```json fences before parsing.
        # On JSONDecodeError: retry once with corrective message.
```

Model constants at top of file:
```python
QWEN_MAX = "qwen-max"
QWEN_TURBO = "qwen-turbo"  
QWEN_VL = "qwen-vl-max"
```

**`backend/services/intelligence/persona.py`**:

Single source of truth for the Quantifaya persona system prompt. This must be imported by every script generation call — never duplicated inline.

```python
QUANTIFAYA_PERSONA = """
You are the Quantifaya scriptwriter. Your persona is a fusion of:
- Bobby Axelrod (Billions): absolute confidence, zero tolerance for mediocrity, controlled aggression
- Taylor Mason (Billions): precision, data-first thinking, no wasted words, surgical clarity
- Nassim Taleb: intellectual combativeness, deep scepticism of models, obsession with second-order effects

VOICE RULES — NON-NEGOTIABLE:
1. Never use the phrase "it can be shown." Show it. Every time.
2. Every claim about a model has a corresponding critique of that model's assumptions.
3. Sarcasm is permitted. Epistemic cowardice is not.
4. Historical examples of model failure are mandatory for every risk-related topic.
5. Taleb must be quoted by name at least once per episode, with the exact source.
6. Equations are derived, not stated. The derivation IS the video.
7. Every episode ends with a real, verifiable challenge question.
8. Academic citations use format: Author (Year) [RefNumber] inline.
9. PAUSE markers: write [PAUSE] wherever a 2-3 second silence should occur.
10. Stage directions: write in italics using *asterisks* — e.g. *equation glows gold*

OUTPUT FORMAT: Valid JSON only. No markdown fences. No preamble. No postamble.
"""

PERSONA_SELF_REVIEW_CHECKLIST = """
Score the following script on each criterion from 1-10:
1. no_handwaving: Are all claims derived or cited? (10 = fully derived)
2. sarcasm_present: Is there at least one sharp, pointed aside? (10 = perfectly placed)
3. model_critique: Is at least one model assumption explicitly challenged? (10 = surgically critiqued)
4. real_world_consequence: Is there at least one historical market event referenced? (10 = vivid, named)
5. taleb_quote: Is Taleb quoted with exact source? (10 = present, sourced, relevant)
6. equation_derivation: Are equations shown step by step? (10 = every step explicit)
7. challenge_question: Is the final challenge derivable but non-trivial? (10 = perfect difficulty)

If any score < 7, return the scene number and specific fix required.
Return as JSON: {"scores": {...}, "fixes_required": [...]}
"""
```

**`backend/services/intelligence/outline_generator.py`**:

Implement `OutlineGenerator` class with method `async generate(topic: str, episode_number: int, series: str) -> EpisodeOutline`.

System prompt: QUANTIFAYA_PERSONA + outline-specific instructions.

User message:
```
Generate a structured episode outline for a 25-minute Quantifaya episode on: "{topic}"

Return JSON matching this exact schema:
{
  "topic": str,
  "episode_number": int,
  "series": "quantifaya",
  "seo_title": str,  // ≤100 chars, keyword-front-loaded
  "scenes": [
    {
      "scene_number": int,
      "scene_class_name": str,  // PascalCase, e.g. "SceneDelta"
      "title": str,
      "duration_target_secs": int,  // 90-300 per scene
      "key_equations": [str],  // LaTeX strings, no $ wrappers
      "key_sources": [str],  // "Author (Year)" format
      "voiceover_hint": str  // one sentence: what this scene argues
    }
  ]
}

Rules:
- 8-12 scenes
- Scene durations must sum to 1400-1600 seconds
- Scene 1 must be a cold open with a shocking hook (a crisis, a failure, a number)
- Final scene must be outro with challenge question and next episode tease
- scene_class_name must be unique per episode
```

Validate response against `EpisodeOutline` schema. Retry up to 3 times on validation failure, sending the Pydantic error as feedback to Qwen.

**`backend/services/intelligence/source_extractor.py`**:

Implement `SourceExtractor` with `async extract(scene: SceneOutlineItem, episode_topic: str) -> List[AcademicSource]`.

Prompt must include: "Return only real, verifiable academic works. If you are not certain a work exists with this exact author, year, and title, omit it. Do not invent sources."

Post-generation: run a self-review Qwen call that checks each source for internal consistency (author + year + title + journal all plausible together). Flag inconsistencies as `confidence: "low"`.

**`backend/services/intelligence/script_generator.py`**:

Implement `ScriptGenerator` with `async generate(outline: EpisodeOutline, sources: SourcesPackage) -> dict`.

The script dict has keys: `episode_id`, `scenes` (list, one per scene), each scene having: `scene_number`, `scene_class`, `voiceover_text`, `stage_directions` (list of strings).

After generation, run `PERSONA_SELF_REVIEW_CHECKLIST`. If any score < 7, regenerate only the flagged scenes with the fix instructions appended to the prompt.

**`backend/services/intelligence/manim_spec_generator.py`**:

Implement `ManımSpecGenerator` with `async generate(scene_outline: SceneOutlineItem, voiceover: str, sources: List[AcademicSource]) -> ManımSceneSpec`.

The prompt must produce valid `ManımSceneSpec` JSON. After generation, validate all LaTeX strings by attempting `py_compile` on a minimal Manim test file containing `MathTex(r"{latex}")`. Any invalid LaTeX triggers a Qwen correction call with the error message.

**`backend/services/intelligence/wan_prompt_generator.py`**:

One Wan prompt per episode. Structure:

```python
WAN_PROMPT_TEMPLATE = """
A sharp, confident financial engineer in his early 30s sits at a sleek 
modern trading desk. Multiple monitors glow behind him showing real-time 
charts and floating mathematical equations. He looks directly at camera 
with intense, calculated focus — the expression of someone who has seen 
every market crash and learned from all of them. The lighting is dramatic: 
high-contrast, blue-tinted ambient light from the screens. Cinematic.
Photorealistic. Professional. Topic context: {topic}.
Camera: slow dolly in, starting wide, ending medium close-up. 8 seconds.
"""

WAN_NEGATIVE_PROMPT = "blurry, watermark, text artifacts, unrealistic anatomy, cartoon, anime, drawing"
```

**`backend/services/intelligence/seo_generator.py`**:

Use `QWEN_TURBO` (not `qwen-max` — this is low-stakes). Generate `SEOMetadata`. Chapter timestamps computed from cumulative `duration_target_secs` values in the outline. Format: `"MM:SS"`.

---

#### PHASE 5: WAN CLIENT + FALLBACK (commit: `feat: wan video generation client`)

**`backend/services/generation/wan_client.py`**:

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class WanClient:
    def __init__(self):
        self.api_key = settings.wan_api_key
        self.base_url = settings.wan_api_base_url

    async def submit_job(self, prompt: str, negative_prompt: str,
                         duration_secs: int = 8,
                         resolution: str = "1920*1080") -> str:
        # POST to Wan API endpoint
        # Returns job_id string
        # Endpoint: POST {base_url}/services/aigc/video-generation/video-synthesis
        # Headers: Authorization: Bearer {api_key}, X-DashScope-Async: enable
        # Payload: {"model": "wan2.1-t2v-plus", "input": {"text": prompt, 
        #           "negative_prompt": negative_prompt},
        #           "parameters": {"size": resolution, "duration": duration_secs}}

    async def poll_status(self, task_id: str) -> dict:
        # GET {base_url}/tasks/{task_id}
        # Returns {"status": "PENDING"|"RUNNING"|"SUCCEEDED"|"FAILED", "output": {...}}

    async def download_clip(self, task_id: str, output_path: str) -> Path:
        # Poll until SUCCEEDED (max 20 attempts × 10s = 200s timeout)
        # Download video_url from output to output_path
        # Raise WanTimeoutError after 200s
        # Raise WanAPIError on FAILED status

    async def generate(self, prompt: str, negative_prompt: str,
                       output_path: str, duration_secs: int = 8) -> Path:
        # Convenience: submit → poll → download
        # Used by the orchestration node
```

**`backend/services/generation/wan_fallback.py`**:

`WanFallback` class with `async render(topic: str, episode_id: str, output_path: str) -> Path`.

Generates a Manim title card: Quantifaya logo text in purple, episode topic in gold, key equation from the outline animating in. 8 seconds. Saves to `output_path`. Returns path.

Uses `subprocess.run(["manim", "-pq{quality}", fallback_script_path, "WanFallbackCard"])`.

---

#### PHASE 6: MANIM CODE GENERATOR + RENDERER (commit: `feat: manim codegen and renderer`)

**`backend/services/generation/manim_codegen.py`**:

`ManımCodeGenerator` class.

**Method `generate_episode_file(episode_id: str, scenes: List[ManımSceneSpec]) -> Path`**:

1. Load `manim_templates/base_template.py.j2` (you must create this)
2. For each scene spec, attempt template matching:
   - Has only equations + text + no axes → use `equation_reveal.py.j2`
   - Has axes_config → use `axes_curve.py.j2`
   - Has ≥2 columns of content → use `two_column.py.j2`
   - Has quote content → use `quote_box.py.j2`
   - None match → call Qwen to generate the scene class code directly
3. Render Jinja2 template with spec as context
4. Inject brand constants at file top (copy from the constants block below)
5. Append `FullEpisode` class that chains all scene classes
6. Run `py_compile.compile(output_path)` — on SyntaxError, send error + code to Qwen for fix (max 2 rounds)
7. Save to `./output/scripts/quantifaya_ep{N}_{episode_id[:8]}.py`

**Brand constants block** (inject at top of every generated file):
```python
# QUANTIFAYA BRAND — DO NOT MODIFY
BG        = "#0D1117"
FG        = "#E6EDF3"
GOLD      = "#F0B429"
RED       = "#FF4D4F"
GREEN     = "#52C41A"
BLUE_NORM = "#4C9BE8"
ORANGE    = "#FF7A00"
PURPLE    = "#7C3AED"
TEAL      = "#00B8D9"
config.background_color = BG

def cite(refs: str):
    return Text(refs, color=TEAL, font_size=13).to_corner(DR).shift(UP*0.1+LEFT*0.1)
```

**Create these Jinja2 templates** in `manim_templates/`:

`base_template.py.j2`:
```jinja2
from manim import *
import numpy as np
from scipy.stats import norm

{{ brand_constants }}

{% for scene in scenes %}
{{ scene.rendered_code }}

{% endfor %}

class FullEpisode(Scene):
    def construct(self):
        for SceneClass in [{% for scene in scenes %}{{ scene.scene_class_name }}, {% endfor %}]:
            instance = SceneClass()
            instance.camera = self.camera
            instance.renderer = self.renderer
            instance.construct()
            self.wait(0.5)
```

`equation_reveal.py.j2`:
```jinja2
class {{ scene.scene_class_name }}(Scene):
    def construct(self):
        {% if scene.cite_string %}
        src = cite("{{ scene.cite_string }}")
        self.add(src)
        {% endif %}
        {% for eq in scene.equations %}
        {{ eq.id }} = MathTex(r"{{ eq.latex }}", color={{ eq.color }}, font_size=36)
        {% endfor %}
        {% for tb in scene.text_blocks %}
        {{ tb.id }} = Text("{{ tb.content }}", color={{ tb.color }}, font_size={{ tb.font_size }}{% if tb.weight == 'BOLD' %}, weight=BOLD{% endif %}{% if tb.slant == 'ITALIC' %}, slant=ITALIC{% endif %})
        {% endfor %}
        {% for step in scene.animation_sequence %}
        {% if step.type == 'wait' %}
        self.wait({{ step.duration_secs }})
        {% else %}
        self.play({{ step.type }}({{ step.target_id }}), run_time={{ step.duration_secs }})
        {% endif %}
        {% endfor %}
```

Create `axes_curve.py.j2`, `two_column.py.j2`, `quote_box.py.j2` following the same pattern, adapting to their respective content types.

**`backend/services/generation/manim_renderer.py`**:

```python
class ManımRenderer:
    async def render_scene(self, script_path: str, scene_class: str,
                           episode_id: str, scene_number: int) -> Path:
        # subprocess.run with timeout=300
        # Command: manim -pq{settings.manim_quality} {script_path} {scene_class} 
        #          --fps 60 --media_dir ./output/scenes/{episode_id}/
        # On timeout: raise ManımRenderTimeout
        # On non-zero return: raise ManımRenderError(stderr)
        # On success: find output MP4 using glob, extract duration via ffprobe
        # Return Path to MP4

    async def render_all_scenes(self, script_path: str, 
                                 scenes: List[ManımSceneSpec],
                                 episode_id: str) -> List[dict]:
        # ThreadPoolExecutor(max_workers=settings.manim_workers)
        # Render all scenes in parallel
        # Returns list of {"scene_number": int, "path": str, "duration": float}
        # Failed scenes replaced with text card fallback render
```

**`backend/services/generation/equation_validator.py`**:

```python
async def validate_latex(latex: str) -> tuple[bool, str]:
    # Write minimal Python to temp file: 
    # from manim import MathTex; MathTex(r"{latex}")
    # Run py_compile on it (fast, no render)
    # Return (True, "") or (False, error_message)

async def validate_and_fix(latex: str, qwen: QwenClient) -> str:
    # If validate_latex fails, ask Qwen to fix it
    # Max 2 rounds. If still failing, return plain text equivalent.
```

---

#### PHASE 7: TTS + AV ALIGNMENT (commit: `feat: voice synthesis and av alignment`)

**`backend/services/generation/tts_synthesizer.py`**:

```python
import edge_tts
import re

LATEX_TO_SPEECH = {
    r"\Delta": "Delta",
    r"\Gamma": "Gamma",
    r"\sigma": "sigma",
    r"\mu": "mu",
    r"\partial": "partial",
    r"\frac{1}{2}": "one half",
    r"\sqrt{T}": "root T",
    r"\infty": "infinity",
    r"N(d_1)": "N of d one",
    r"N(d_2)": "N of d two",
    r"\mathbb{E}": "the expected value of",
    r"\mathbb{P}": "the probability",
    r"dB": "d B",
    r"dS": "d S",
    r"dt": "d t",
    r"\Rightarrow": "which gives us",
    r"\approx": "approximately equals",
    r"\geq": "greater than or equal to",
    r"\leq": "less than or equal to",
}

class TTSSynthesizer:
    VOICE = "en-US-GuyNeural"
    RATE = "-10%"

    def preprocess(self, text: str) -> str:
        # Strip [PAUSE] markers (silence handled by video padding)
        # Replace *asterisk stage directions* with ""
        # Apply LATEX_TO_SPEECH substitutions
        # Remove inline citation tags [T1], [H2] etc.
        # Return clean speech text

    async def synthesize_scene(self, voiceover_text: str, 
                                output_path: str) -> tuple[Path, float]:
        # preprocess text
        # edge_tts.Communicate(text, voice=VOICE, rate=RATE)
        # Save to output_path (.wav)
        # Measure duration via ffprobe
        # Return (Path, duration_secs)
```

**`backend/services/generation/av_aligner.py`**:

```python
class AVAligner:
    TOLERANCE_SECS = 2.0
    
    async def align(self, video_path: str, audio_path: str,
                    output_path: str) -> tuple[Path, float]:
        # Get video_duration and audio_duration via ffprobe
        # If abs(audio - video) <= TOLERANCE: merge directly
        # If audio < video by > TOLERANCE: pad audio with silence
        #   ffmpeg -i audio -af "apad=pad_dur={gap}" padded_audio
        # If audio > video by > 5s: regenerate TTS at -15% rate
        # If audio > video by 2-5s: pad video with self.wait()
        # Final merge: ffmpeg -i video -i audio -c:v copy -c:a aac -shortest output
        # Return (output_path, final_duration)
```

---

#### PHASE 8: FFMPEG COMPOSITOR (commit: `feat: ffmpeg composition engine`)

**`backend/services/composition/scene_syncer.py`**:

`SceneSyncer` — takes ordered list of `{"video": path, "audio": path}` dicts. Runs `AVAligner` on each pair in parallel (ThreadPoolExecutor, 4 workers). Returns ordered list of synced scene paths.

**`backend/services/composition/episode_compositor.py`**:

```python
class EpisodeCompositor:
    async def compose(self, episode_id: str, wan_clip_path: str,
                      synced_scene_paths: List[str],
                      brand_intro_path: str, brand_outro_path: str,
                      output_path: str) -> Path:
        # 1. Build ffmpeg concat manifest:
        #    brand_intro → wan_clip → scene_1 → scene_2 → ... → brand_outro
        # 2. ffmpeg -f concat -safe 0 -i manifest.txt -c copy output.mp4
        # 3. ffprobe to verify: resolution 1920x1080, fps 60
        # 4. Log file size
        # 5. Return output_path

    async def _get_video_info(self, path: str) -> dict:
        # ffprobe -v quiet -print_format json -show_streams -show_format {path}
        # Returns dict with width, height, fps, duration
```

**`backend/services/composition/subtitle_generator.py`**:

Generate SRT from voiceover text. Use word-count-based timing estimation (160 WPM) since edge-tts word-level timing is not always reliable. Produce scene-level SRT cues (not word-level). Embed in final MP4 using ffmpeg subtitle filter.

---

#### PHASE 9: DELIVERY SERVICES (commit: `feat: youtube upload and thumbnail`)

**`backend/services/delivery/thumbnail_generator.py`**:

```python
from PIL import Image, ImageDraw, ImageFont
import qrcode

class ThumbnailGenerator:
    SIZE = (1280, 720)
    BG_COLOR = (13, 17, 23)       # #0D1117
    GOLD = (240, 180, 41)          # #F0B429
    WHITE = (230, 237, 243)        # #E6EDF3
    PURPLE = (124, 58, 237)        # #7C3AED

    def generate(self, topic_keyword: str, key_equation_latex: str,
                 episode_number: int, output_path: str) -> Path:
        # Create 1280x720 dark background
        # Large topic keyword in GOLD (top area)
        # Smaller "Episode {N}" in WHITE
        # Key equation rendered as text (LaTeX stripped to readable form) in WHITE
        # "QUANTIFAYA" watermark in PURPLE bottom-right
        # Decorative math symbols scattered (∑ ∫ ∂ σ Δ) in semi-transparent GOLD
        # Save as JPEG quality=95
```

Note: For proper LaTeX rendering in thumbnails, use matplotlib's `mathtext` renderer: `from matplotlib import mathtext`. This avoids needing a full TeX installation for thumbnail generation alone.

**`backend/services/delivery/youtube_uploader.py`**:

```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

class YouTubeUploader:
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
              "https://www.googleapis.com/auth/youtube"]

    async def upload(self, video_path: str, thumbnail_path: str,
                     seo_metadata: SEOMetadata, channel_id: str) -> str:
        # Build YouTube service from client secrets
        # videos.insert with resumable upload (MediaFileUpload chunksize=1MB)
        # status.privacyStatus = "unlisted"
        # snippet: title, description (with chapters prepended), tags
        # On success: thumbnails.set, then return video_id
        # Retry 3x on upload failure
        # Store youtube_id in episodes table
```

---

#### PHASE 10: LANGGRAPH ORCHESTRATION (commit: `feat: langgraph episode generation graph`)

**`backend/orchestration/state.py`** — `EpisodeState` TypedDict as specified in schemas.

**`backend/orchestration/nodes.py`** — one async function per node. Each node:
1. Receives `state: EpisodeState`
2. Does its work (calling the relevant service)
3. Updates the state dict
4. Persists key fields to PostgreSQL via `update_episode_status()`
5. Returns the updated state

Node functions:
```python
async def analyze_topic(state: EpisodeState) -> EpisodeState: ...
async def extract_sources(state: EpisodeState) -> EpisodeState: ...
async def generate_script(state: EpisodeState) -> EpisodeState: ...
async def generate_manim_specs(state: EpisodeState) -> EpisodeState: ...
async def generate_wan_prompt(state: EpisodeState) -> EpisodeState: ...
async def generate_seo(state: EpisodeState) -> EpisodeState: ...
async def synthesize_audio(state: EpisodeState) -> EpisodeState: ...
async def generate_wan_clip(state: EpisodeState) -> EpisodeState: ...
async def render_manim_scenes(state: EpisodeState) -> EpisodeState: ...
async def align_av_scenes(state: EpisodeState) -> EpisodeState: ...
async def compose_episode(state: EpisodeState) -> EpisodeState: ...
async def upload_youtube(state: EpisodeState) -> EpisodeState: ...
async def mark_complete(state: EpisodeState) -> EpisodeState: ...
async def handle_error(state: EpisodeState) -> EpisodeState: ...
```

**`backend/orchestration/graph.py`**:

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

def build_episode_graph() -> StateGraph:
    graph = StateGraph(EpisodeState)

    # Add all nodes
    graph.add_node("analyze_topic", analyze_topic)
    graph.add_node("extract_sources", extract_sources)
    # ... add all nodes

    # Entry point
    graph.set_entry_point("analyze_topic")

    # Intelligence phase (sequential)
    graph.add_edge("analyze_topic", "extract_sources")
    graph.add_edge("extract_sources", "generate_script")
    graph.add_edge("generate_script", "generate_manim_specs")
    graph.add_edge("generate_manim_specs", "generate_wan_prompt")
    graph.add_edge("generate_wan_prompt", "generate_seo")

    # Human review gate — interrupt before generation starts
    graph.add_edge("generate_seo", "synthesize_audio")  
    # interrupt_before=["synthesize_audio"] set at compile time

    # Generation phase (these run, then join at compose)
    graph.add_edge("synthesize_audio", "render_manim_scenes")
    graph.add_edge("render_manim_scenes", "generate_wan_clip")
    graph.add_edge("generate_wan_clip", "align_av_scenes")
    graph.add_edge("align_av_scenes", "compose_episode")
    graph.add_edge("compose_episode", "upload_youtube")
    graph.add_edge("upload_youtube", "mark_complete")
    graph.add_edge("mark_complete", END)

    # Error routing
    graph.add_conditional_edges(
        "handle_error",
        lambda s: END if s["errors"] else "analyze_topic"
    )

    checkpointer = SqliteSaver.from_conn_string("./output/graph_checkpoints.db")
    return graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["synthesize_audio"] if not settings.auto_approve else []
    )
```

---

#### PHASE 11: FASTAPI APP + ROUTES (commit: `feat: fastapi app and episode routes`)

**`backend/main.py`**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.database import async_engine
from models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup: verify DB connection, verify Redis connection, log config
    yield
    # On shutdown: close connections

app = FastAPI(title="Quantifaya AutoDirector API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Include routers
from api.routes import episodes, health, stream
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(episodes.router, prefix="/api/v1/episodes", tags=["episodes"])
app.include_router(stream.router, prefix="/api/v1/stream", tags=["stream"])
```

**`backend/api/routes/health.py`**:
- `GET /health` → `{"status": "ok", "version": "1.0.0"}`
- `GET /health/db` → test DB query
- `GET /health/redis` → test Redis ping
- `GET /health/qwen` → test Qwen API with a minimal completion

**`backend/api/routes/episodes.py`**:
- `POST /` → create episode, enqueue Celery task, return `{"episode_id": str, "status": "pending"}`
- `GET /{id}` → return episode + all scenes
- `GET /{id}/script` → return `episodes.script_json`
- `POST /{id}/resume` → resume LangGraph from human gate
- `GET /` → list episodes, paginated
- `DELETE /{id}` → cancel + mark failed

**`backend/api/routes/stream.py`**:
- `GET /{episode_id}/progress` → SSE endpoint using `sse_starlette`
- Reads events from Redis pub/sub channel `episode:{id}:progress`
- Each event: `{"phase": str, "node": str, "progress_pct": int, "message": str}`

**`backend/workers/celery_app.py`**:
```python
from celery import Celery
from core.config import get_settings

settings = get_settings()
celery_app = Celery("autodirector", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_routes = {
    "workers.tasks.run_episode_graph": {"queue": "default"},
    "workers.tasks.upload_youtube": {"queue": "high"},
}
```

**`backend/workers/tasks.py`**:
```python
@celery_app.task(bind=True, max_retries=3)
def run_episode_graph(self, episode_id: str, topic: str, 
                      episode_number: int, series: str):
    # Build graph, create initial state, invoke
    # graph.invoke(initial_state, config={"configurable": {"thread_id": episode_id}})
    # Publish progress events to Redis on each node completion
```

---

#### PHASE 12: TESTS (commit: `feat: test suite`)

Write these tests. All must pass before submission.

**`tests/unit/test_outline_generator.py`**:
- Mock Qwen client. Assert `EpisodeOutline` validates correctly for a known topic.
- Assert scene count 8-12. Assert duration sum 1400-1600.

**`tests/unit/test_script_generator.py`**:
- Mock Qwen. Assert script has correct structure. Assert `[PAUSE]` markers present.

**`tests/unit/test_equation_validator.py`**:
- Known good LaTeX: assert passes. Known bad: `\frac{1}{0}{\sin}`, assert caught.

**`tests/unit/test_wan_client.py`**:
- Mock HTTP. Assert submit → poll → download state machine.
- Assert `WanTimeoutError` raised after 20 failed polls.

**`tests/unit/test_compositor.py`**:
- Mock ffmpeg subprocess. Assert concat manifest built correctly.
- Assert output path returned.

**`tests/integration/test_pipeline_e2e.py`**:
- Requires live Qwen API key and PostgreSQL.
- Topic: "The Normal Distribution Fails in Finance"
- Assert outline generated. Assert sources contain at least one real citation. Assert script > 2000 words. Assert SEO title ≤ 100 chars.
- DO NOT render Manim or call Wan in this test — stop after script phase.

---

#### PHASE 13: BRAND ASSETS (commit: `feat: brand intro and outro manim files`)

**`brand/intro_card.py`**:

Manim file with `BrandIntro(Scene)` class. 5 seconds. Renders: Quantifaya logo text in purple (#7C3AED) pulsing in, tagline "Financial Engineering. Explained Rigorously. Applied Practically." in gold, dark background. Renders to `brand/rendered/intro_5s.mp4` when run with `manim -pqh brand/intro_card.py BrandIntro`.

**`brand/outro_card.py`**:

`BrandOutro(Scene)` class. 5 seconds. Subscribe prompt, channel handle, next episode tease placeholder. Renders to `brand/rendered/outro_5s.mp4`.

Pre-render both during Docker build and cache in `brand/rendered/`. These never change per episode.

---

### EXECUTION ORDER SUMMARY

Execute phases in this exact sequence. Commit after each. Do not proceed to a phase until the previous phase's files exist and are syntactically valid.

```
Phase 0  → Scaffold         → commit
Phase 1  → Core infra       → commit
Phase 2  → DB models        → commit
Phase 3  → Schemas          → commit
Phase 4  → Qwen + Intel     → commit
Phase 5  → Wan client       → commit
Phase 6  → Manim codegen    → commit
Phase 7  → TTS + alignment  → commit
Phase 8  → ffmpeg           → commit
Phase 9  → Delivery         → commit
Phase 10 → LangGraph        → commit
Phase 11 → FastAPI + routes → commit
Phase 12 → Tests            → commit
Phase 13 → Brand assets     → commit
```

After Phase 13: run `docker-compose up --build`. All services must reach healthy state. Then run:

```bash
curl -X POST http://localhost:8000/api/v1/episodes \
  -H "Content-Type: application/json" \
  -d '{"topic": "Why the Normal Distribution Fails in Finance", "episode_number": 1, "series": "quantifaya"}'
```

This must return a 201 with an `episode_id`. The pipeline must progress through at least Phase 1 (Intelligence) without error before you stop.

---

### CONSTRAINTS — READ BEFORE WRITING ANY CODE

1. **No mock data in production paths.** Every service calls its real dependency. Mocks only in test files.
2. **Every service is independently importable.** No circular imports. Services import from `core/` and `schemas/` only — never from each other except through dependency injection.
3. **Every long-running operation is async.** No `time.sleep()` — use `asyncio.sleep()`. No blocking IO in FastAPI request handlers.
4. **ffmpeg is always called via subprocess**, never via a Python wrapper library. This ensures compatibility with system ffmpeg.
5. **Manim is always called via subprocess**, not imported. Manim's global state is not safe to share across scenes in a single process.
6. **All output paths use `pathlib.Path`**, never raw strings.
7. **All Qwen responses are logged** with: timestamp, model, topic, prompt_tokens, completion_tokens, latency_ms. Log to structlog at DEBUG level.
8. **The `output/` directory is the only mutable state on disk.** Everything else is in PostgreSQL or Redis.
9. **Brand color constants are defined once** in `backend/core/brand.py` and imported everywhere — including into generated Manim files. Never define them inline.
10. **The human review gate is always respected** unless `AUTO_APPROVE=true`. This is not negotiable for production use.