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

    UPDATAREPO_STARTTIMEHOUR: int
    UPDATAREPO_STARTTIMEMINUTE: int
    UPDATAREPO_STARTTIMESECOND: int

    # 确定使用哪个 .env 文件，若 .env.production 存在则优先使用
    if os.path.exists(".env.production"):
        env_file: ClassVar[str] = ".env.production"
    else:
        env_file: ClassVar[str] = ".env"

    model_config = SettingsConfigDict(
        env_file=env_file, _env_file_encoding="utf-8", extra="allow"
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
