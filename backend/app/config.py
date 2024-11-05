from logging.handlers import TimedRotatingFileHandler

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from typing import ClassVar
import logging

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

def setup_logging():
    # 设置日志文件名，包含日期
    log_name = "coin"
    # # 创建logger对象。传入logger名字
    # logger = logging.getLogger(log_name)
    log_path = os.path.join("./data_logs/", log_name)
    # 创建一个 TimedRotatingFileHandler，每天生成一个新日志文件，保留最近7天的日志文件
    handler = TimedRotatingFileHandler(
        log_path,
        when="D",  # "D" 表示每天轮转
        interval=1,  # 每 1 天轮转一次
        backupCount=7,  # 仅保留最近 7 天的日志
        encoding="utf-8"
    )

    # 设置日志格式
    handler.suffix = "%Y-%m-%d.log"
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [Class: %(module)s, Function: %(funcName)s, Line: %(lineno)d]')
    handler.setFormatter(formatter)
    # 配置日志
    logging.basicConfig(level=logging.INFO, handlers=[handler])

    # 设置 watchfiles 的日志级别为 WARNING，以屏蔽 INFO 日志
    logging.getLogger('watchfiles').setLevel(logging.WARNING)
    return logging

@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
logging = setup_logging()