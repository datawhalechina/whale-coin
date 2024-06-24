from fastapi import APIRouter, Form, Depends, HTTPException, status, Request
from datetime import datetime, timedelta
from app.dependencies import check_jwt_token, get_db
from app.config import settings
from jose import jwt
from typing import Optional
from app.core.schemas.users import UserBase
from sqlalchemy.orm import Session
from app.core.models.coin import Base, Apply, Consume, Bill
from app.core.models.users import Users
from app.core.models.item import Item,Order
from app.database import engine
import json

Base.metadata.create_all(bind=engine)

item = APIRouter(
    prefix="/api/item",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)

@coin.get("/fetch_apply")
async def fetch_apply(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    apply_items = db.query(Apply).filter_by(user_id=user.id, apply_status=None).all()
    all_apply = [{"id":row.id, "repo":row.repo, "role":row.role, "content":row.content, "record_time":row.record_time} for row in apply_items]
    return all_apply

@item.get("/fetch_item")
async def fetch_item(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    return db.query(Item).all()

@item.post("/add_item")
async def add_item(item: Item,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    new_item = item
    new_item.create_time=datetime.now()
    new_item.create_user=user.id
    try:
        db.add(new_item)
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        return {"code":500,"message":e}
@item.get("/get_order")
async def get_order(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    return db.query(Order).all()
@item.post("/add_order")
async def add_order(order:Order,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    new_order = order
    new_order.create_time=datetime.now()
    new_order.create_user=user.id
    try:
        db.add(new_order)
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        return {"code":500,"message":e}    
@item.post("/auduit_order")
async def audit_order(orderid:int,status:int,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    order=db.query(Order).filter_by(id=orderid)
    try:
        order.status=status
        order.audit_id=user.id
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        return {"code":500,"message":e}
@item.get("/get_audit_order")
async def get_audit_order(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):   
    order=db.query(Order).filter_by(status=1).all()