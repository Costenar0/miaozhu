from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # Database (SQLite, stored in data/)
    DATABASE_URL: str = "sqlite+aiosqlite:///data/miaozhu.db"

    # CORS
    CORS_ORIGINS: str = '["http://localhost:5173"]'

    @property
    def cors_origins_list(self) -> List[str]:
        return json.loads(self.CORS_ORIGINS)

    # Scheduler
    SCHEDULER_POLL_INTERVAL: int = 5       # 轮询间隔（秒）
    SCHEDULER_MAX_CONCURRENT_LLM: int = 5  # 最大并发 LLM 调用数
    SCHEDULER_MAX_CONCURRENT_EXPORT: int = 4  # 最大并发导出数

    # LLM (OpenAI-compatible)
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o"

    # Export data directory
    EXPORT_DATA_DIR: str = "data/exports"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
