from fastapi import APIRouter, Form, Depends, HTTPException, status, Request,UploadFile,File
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

@item.get("/fetch_item")
async def fetch_item(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    return db.query(Item).all()

@item.post("/add_item")
async def add_item(item: Item=Form(),files: list[UploadFile]=File(...),user: UserBase = Depends(check_jwt_token),db: Session = Depends(get_db)):
    uploaded_files_info = []
    for file,index in files:
        # 保存文件到本地目录
        new_file_name=index+file.filename.split('.')[-1]
        file_path = f"../static/img/{new_file_name}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        # 记录已上传文件的基本信息
        uploaded_files_info.append({"filename": file.new_file_name, "size": len(content)})
    new_item = item
    new_item.create_time=datetime.now()
    new_item.create_user=user.id
    new_item.img_path=json.dumps(uploaded_files_info)
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
async def add_order(order:Order=Form(...),user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
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
async def audit_order(orderid:int=Form(),status:int=Form(),user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
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