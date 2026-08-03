from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    qwen_api_key: str = ""
    qwen_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    wan_api_key: str = ""
    wan_api_base_url: str = "https://dashscope.aliyuncs.com/api/v1"
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "autodirector"
    postgres_user: str = "autodirector"
    postgres_password: str = "changeme"
    redis_url: str = "redis://redis:6379/0"
    youtube_client_secrets_file: str = "./secrets/youtube_client_secrets.json"
    youtube_channel_id: str = ""
    auto_approve: bool = False
    manim_workers: int = 4
    manim_quality: str = "h"
    log_level: str = "INFO"

    # Memgraph
    memgraph_uri: str = "bolt://memgraph:7687"
    memgraph_user: str = ""
    memgraph_password: str = ""
    memgraph_enabled: bool = False
    memgraph_concept_index: str = "conceptIndex"
    memgraph_max_subgraph_depth: int = 3
    memgraph_retrieval_limit: int = 10

    # Source Ingestion
    max_pdf_size_mb: int = 50
    playwright_enabled: bool = True
    embedding_batch_size: int = 32

    # Backblaze B2
    b2_key_id: str = ""
    b2_application_key: str = ""
    b2_bucket_name: str = "quantifaya"
    b2_endpoint_url: str = "https://s3.us-east-005.backblazeb2.com"
    b2_public_url_base: str = "https://f005.backblazeb2.com/file/quantifaya"

    # Video Generation Providers (free-tier)
    # Primary provider: cogvideox (self-hosted, free) | wan (legacy)
    video_gen_provider: str = "cogvideox"
    # Fallback provider used if the primary fails (must be free-tier too)
    video_gen_fallback_provider: str = "wan"
    # CogVideoX (self-hosted via diffusers)
    cogvideox_model: str = "THUDM/CogVideoX-5b"
    cogvideox_device: str = "cuda"          # cuda | cpu
    cogvideox_dtype: str = "float16"        # float16 | float32
    # B-roll strategy: off | cold_open_only | scene_transitions | full
    broll_strategy: str = "cold_open_only"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

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