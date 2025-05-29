from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres.fjyxvuluxvzrjgofhsrj:HardPass1@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
