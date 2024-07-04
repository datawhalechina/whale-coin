from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    HOST: str
    PORT: int
    SQLALCHEMY_DATABASE_URL: str

    # 动态获取环境变量 ENV_FILE，默认为 .env
    env_file = os.getenv("ENV_FILE", ".env")

    model_config = SettingsConfigDict(env_file=env_file, _env_file_encoding='utf-8', extra='allow')

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
