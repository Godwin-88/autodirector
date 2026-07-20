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

    # Memgraph
    memgraph_uri: str = "bolt://memgraph:7687"
    memgraph_user: str = ""
    memgraph_password: str = ""
    memgraph_enabled: bool = False

    # Source Ingestion
    max_pdf_size_mb: int = 50
    playwright_enabled: bool = True
    embedding_batch_size: int = 32

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