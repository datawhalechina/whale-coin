from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from typing import ClassVar
class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    HOST: str
    PORT: int
    SQLALCHEMY_DATABASE_URL: str

    # 动态获取环境变量 ENV_FILE，默认为 .env
    # 标记 env_file 为 ClassVar，指定为类属性
    env_file: ClassVar[str] = os.getenv("ENV_FILE", ".env")

    model_config = SettingsConfigDict(env_file=env_file, _env_file_encoding='utf-8', extra='allow')

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
