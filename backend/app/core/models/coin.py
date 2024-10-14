from sqlalchemy import Column, Integer, Float, VARCHAR, DateTime, Boolean, String, Text
from app.database import Base


class Apply(Base):
    __tablename__ = "apply"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    repo = Column(VARCHAR(200))
    role = Column(VARCHAR(200))
    content = Column(Text)
    url = Column(VARCHAR(255), nullable=True)
    record_time = Column(DateTime)
    apply_time = Column(DateTime)
    apply_status = Column(Boolean)
    supervisor_id = Column(Integer)
    decision = Column(Boolean)
    notes = Column(VARCHAR(500))
    confirm_time = Column(DateTime)
    coin_amount = Column(Float, default=0.0)
    repo_owner_name = Column(VARCHAR(100))
    user_name = Column(VARCHAR(100))
    pid = Column(Integer)
    title = Column(VARCHAR(200))
    state = Column(VARCHAR(20))


class Consume(Base):
    __tablename__ = "consume"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    content = Column(VARCHAR(200))
    apply_time = Column(DateTime)
    supervisor_id = Column(Integer)
    notes = Column(VARCHAR(500))
    confirm_time = Column(DateTime)
    price = Column(Float, default=0.0)


class Bill(Base):
    __tablename__ = "bill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    type = Column(VARCHAR(200))
    content = Column(VARCHAR(200))
    change_amount = Column(Float, default=0.0)
    balance = Column(Float, default=0.0)
    create_time = Column(DateTime)
