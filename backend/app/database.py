from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy.orm import scoped_session

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 启用预检查
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20
)

# SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

