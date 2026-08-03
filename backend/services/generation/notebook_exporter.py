"""Notebook exporter — Pattern B: manual Colab fallback.

When the automated Colab queue worker (Pattern A) is not running, AutoDirector
can emit a complete, self-contained ``.ipynb`` notebook capturing everything
needed to generate the video clip manually in Colab (free T4 GPU):

  - installs difffusers/torch/accelerate/redis/boto3
  - prompts for the Hugging Face token at runtime (or reads HUGGINGFACE_TOKEN)
  - loads THUDM/CogVideoX-2b in float16 with CPU offload
  - generates the clip from the episode's saved prompt
  - uploads the mp4 to Backblaze B2 and writes the result back to Redis

The notebook JSON is built directly here (no nbformat dependency), and is
validated against the nbformat spec in the unit tests.
"""
import json
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import get_settings
from core.logging import get_logger

logger = get_logger("notebook_exporter")


def _cell(cell_type: str, source: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
    """Build a single notebook cell dict."""
    return {
        "cell_type": cell_type,
        "metadata": metadata or {},
        "source": source,
        "execution_count": None,
        "outputs": [],
    } if cell_type == "code" else {
        "cell_type": "markdown",
        "metadata": metadata or {},
        "source": source,
    }


def build_notebook(
    prompt: str,
    negative_prompt: str,
    duration_secs: int,
    episode_id: str,
    *,
    output_key: str = "",
) -> Dict[str, Any]:
    """Build a Colab notebook dict for a single episode's video clip.

    Args:
        prompt: The text prompt for the clip.
        negative_prompt: Things to avoid.
        duration_secs: Target clip duration.
        episode_id: The episode this clip belongs to.
        output_key: Optional B2 object key (defaults to ``episodes/{episode_id}/intro.mp4``).

    Returns:
        A notebook dict conforming to nbformat v4.
    """
    key = output_key or f"episodes/{episode_id}/intro.mp4"

    cells = [
        _cell("markdown", (
            "# Quantifaya AutoDirector — CogVideoX Colab Generation\n\n"
            f"This notebook generates the intro clip for **episode `{episode_id}`** "
            "using CogVideoX-2b on the free Colab T4 GPU and uploads it to Backblaze B2.\n\n"
            "## Before running\n"
            "1. **Runtime → Change runtime type → T4 GPU** (free).\n"
            "2. Run the 'Auth' cell in step 3 — it will ask for your Hugging Face token "
            "(required, the model is gated).\n"
            "3. Set the B2 + Redis secrets in the 'Credentials' cell (or paste them there)."
        )),
        _cell("code", (
            "# 1. Install dependencies\n"
            "!pip install -q torch diffusers transformers accelerate sentencepiece \\\n"
            "             protobuf redis boto3 imageio[ffmpeg]"
        )),
        _cell("code", (
            "# 2. Imports\n"
            "import json, os, io, uuid, getpass\n"
            "import torch\n"
            "from diffusers import CogVideoXPipeline\n"
            "from diffusers.utils import export_to_video\n"
            "from PIL import Image"
        )),
        _cell("code", (
            "# 3. Hugging Face auth (model is gated — token required)\n"
            "hf_token = os.environ.get('HUGGINGFACE_TOKEN') or getpass.getpass('Hugging Face token: ')\n"
            "if not hf_token:\n"
            "    raise ValueError('A Hugging Face token is required to download CogVideoX-2b.')\n"
            "print('HF token set:', bool(hf_token))"
        )),
        _cell("code", (
            "# 4. Credentials (paste your values or set env vars)\n"
            "B2_KEY_ID        = os.environ.get('B2_KEY_ID', '')\n"
            "B2_APPLICATION_KEY = os.environ.get('B2_APPLICATION_KEY', '')\n"
            "B2_BUCKET        = os.environ.get('B2_BUCKET_NAME', 'quantifaya')\n"
            "B2_ENDPOINT      = os.environ.get('B2_ENDPOINT_URL', 'https://s3.us-east-005.backblazeb2.com')\n"
            "REDIS_URL        = os.environ.get('REDIS_URL', '')\n"
            "if not (B2_KEY_ID and B2_APPLICATION_KEY):\n"
            "    print('WARNING: B2 credentials missing — set them below or as env vars before proceeding.')\n"
            "if not REDIS_URL:\n"
            "    print('WARNING: REDIS_URL missing — set it to push the result back (Upstash).')"
        )),
        _cell("code", (
            "# 5. Load the model (T4-friendly)\n"
            "MODEL_ID = 'THUDM/CogVideoX-2b'\n"
            "print('Loading', MODEL_ID, '...')\n"
            "pipe = CogVideoXPipeline.from_pretrained(\n"
            "    MODEL_ID, torch_dtype=torch.float16, token=hf_token\n"
            ")\n"
            "pipe.enable_model_cpu_offload()\n"
            "print('Model loaded.')"
        )),
        _cell("code", (
            "# 6. Prompt (from the episode)\n"
            f"PROMPT = {json.dumps(prompt)}\n"
            f"NEGATIVE_PROMPT = {json.dumps(negative_prompt)}\n"
            f"EPISODE_ID = {json.dumps(episode_id)}\n"
            f"DURATION_SECS = {int(duration_secs)}\n"
            f"OUTPUT_KEY = {json.dumps(key)}\n"
            f"RESULT_KEY = 'colab:results:{str(uuid.uuid4())[:8]}'\n"
            f"print('Episode:', EPISODE_ID)\n"
            f"print('Output key:', OUTPUT_KEY)"
        )),
        _cell("code", (
            "# 7. Generate the clip\n"
            "num_frames = max(16, min(49, int(DURATION_SECS * 8)))\n"
            "frames = pipe(\n"
            "    prompt=PROMPT,\n"
            "    negative_prompt=NEGATIVE_PROMPT,\n"
            "    num_frames=num_frames,\n"
            "    num_inference_steps=50,\n"
            "    guidance_scale=6.0,\n"
            ").frames[0]\n"
            "local_path = f'/content/{EPISODE_ID}_intro.mp4'\n"
            "export_to_video(frames, local_path, fps=8)\n"
            "print('Generated', local_path)"
        )),
        _cell("code", (
            "# 8. Upload to Backblaze B2 and push the result to Redis\n"
            "import boto3, redis, json, os\n"
            "\n"
            "s3 = boto3.client(\n"
            "    's3',\n"
            "    endpoint_url=B2_ENDPOINT,\n"
            "    aws_access_key_id=B2_KEY_ID,\n"
            "    aws_secret_access_key=B2_APPLICATION_KEY,\n"
            "    region_name='us-east-005',\n"
            ")\n"
            "s3.upload_file(local_path, B2_BUCKET, OUTPUT_KEY, ExtraArgs={'ContentType': 'video/mp4'})\n"
            "# Public URL\n"
            "public_base = os.environ.get('B2_PUBLIC_URL_BASE', f'https://f005.backblazeb2.com/file/{B2_BUCKET}')\n"
            "public_url = f'{public_base}/{OUTPUT_KEY}'\n"
            "print('Uploaded:', public_url)\n"
            "\n"
            "if REDIS_URL:\n"
            "    r = redis.from_url(REDIS_URL, decode_responses=True)\n"
            "    r.lpush(RESULT_KEY, json.dumps({'status': 'success', 'url': public_url}))\n"
            "    print('Result pushed to Redis:', RESULT_KEY)\n"
            "else:\n"
            "    print('No REDIS_URL — result not pushed; your API will time out and fall back to Manim.')"
        )),
        _cell("markdown", (
            "## Done\n"
            "The clip is now on Backblaze B2. The AutoDirector API (if polling with the `colab` "
            "provider) will pick it up. If you ran this manually without Redis, the API already "
            "fell back to the Manim title card for this episode."
        )),
    ]

    return {
        "cells": cells,
        "metadata": {
            "colab": {
                "provenance": [],
                "toc_visible": True,
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


class NotebookExporter:
    """Exports a runnable Colab notebook for the manual generation path."""

    def __init__(self):
        self.settings = get_settings()

    def export(
        self,
        episode_id: str,
        prompt: str,
        negative_prompt: str = "",
        duration_secs: int = 8,
        output_key: str = "",
        output_dir: str = "",
    ) -> Path:
        """Write a .ipynb for the given episode to disk and return its path."""
        notebook = build_notebook(
            prompt,
            negative_prompt,
            duration_secs,
            episode_id,
            output_key=output_key,
        )

        out_dir = Path(output_dir or f"./output/colab")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"export_{episode_id}.ipynb"

        out_path.write_text(json.dumps(notebook, indent=2))
        logger.info(
            "notebook_exported",
            path=str(out_path),
            episode_id=episode_id,
        )
        return out_path