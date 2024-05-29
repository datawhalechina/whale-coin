from fastapi import APIRouter, Form, Depends, HTTPException, status, Request
from datetime import datetime, timedelta
from app.dependencies import check_jwt_token, get_db
from app.config import settings
from jose import jwt
from typing import Optional
from app.core.schemas.users import UserBase
from sqlalchemy.orm import Session
from app.core.models.coin import Base
from app.core.models.users import Users
from app.database import engine
import json

Base.metadata.create_all(bind=engine)

coin = APIRouter(
    prefix="/api/coin",
    tags=["coin"],
    responses={404: {"description": "Not found"}},
)

@coin.get("/hello/{name}")
async def hello(name: str):
    return {"code": 200, "message":"hello "+name}
