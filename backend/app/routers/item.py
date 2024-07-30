from fastapi import APIRouter, Form, Depends, HTTPException, status, Request,UploadFile,File
from datetime import datetime, timedelta
from app.dependencies import check_jwt_token, get_db
from app.config import settings
from jose import jwt
from typing import Optional
from app.core.schemas.users import UserBase
from sqlalchemy.orm import Session
from app.core.models.coin import Base
from app.core.models.item import Item,Order
from app.database import engine
import json

Base.metadata.create_all(bind=engine)

item = APIRouter(
    prefix="/api/item",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)

@item.get("/get_item")
async def fetch_item(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    return db.query(Item).all()

item.post("/get_item_detal")
async def get_item_detal(itemid:int,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    return db.query(Item).filter_by(id=itemid).first()

@item.post("/add_item")
async def add_item(request: Request,user: UserBase = Depends(check_jwt_token),db: Session = Depends(get_db)):
    uploaded_files_info = []
    form: UploadFile = await request.form()
    name=form.get("name")
    describe=form.get("describe")
    stock=form.get("stock")
    prince=form.get("prince")
    files=form.get("files")
    new_item = Item(
        name=name,
        describe=describe,
        stock=stock,
        prince=prince,
    )
    new_item.create_time=datetime.now()
    new_item.create_user=user.id
    for file,index in files:
        # 保存文件到本地目录
        new_file_name=new_item.name+index+'.'+file.filename.split('.')[-1]
        file_path = f"../static/img/{new_file_name}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        # 记录已上传文件的基本信息
        uploaded_files_info.append(new_file_name)
        new_item.img_path=uploaded_files_info
    try:
        
        db.add(new_item)
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        return {"code":500,"message":e}
@item.post("/delete_item") 
async def delete_item(itemid:int,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    item=db.query(Item).filter_by(id=itemid).first()
    imgs=item.img_path.split(',')
    for img in imgs:
        img_path=f"../static/img/{img}"
        if os.path.exists(img_path):
            os.remove(img_path)
    try:
        db.delete(item)
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        return{"code":500,"message":e}   

@item.get("/get_order")
async def get_order(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    return db.query(Order).all()
@item.post("/add_order")
async def add_order(itemid:int=Form(...),quantity:int=Form(...),order_type:str=Form(...),status:str=Form(...),toal_price:float=Form(...),address:str=Form(...),phone:str=Form(...),user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    new_order = Order(
        item_id=itemid,
        quantity=quantity,
        order_type=order_type,
        status=status,
        toal_price=toal_price,
        address=address,
        phone=phone,
        create_time=datetime.now(),
        user_id=user.id,
    )
    try:
        db.add(new_order)
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        return {"code":500,"message":e}    
@item.post("/auduit_order")
async def audit_order(orderid:int=Form(),status:str=Form(),user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    order=db.query(Order).filter_by(id=orderid)
    try:
        order.status=status
        order.audit_id=user.id
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        return {"code":500,"message":e}
@item.post("/get_audit_order")
async def get_audit_order(statusId:str,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):   
    order=db.query(Order).filter_by(status=statusId).all()

@item.post("/get_order_detal")
async def get_order_detal(orderid:int,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    order=db.query(Order).filter_by(id=orderid).first()

@item.get("/get_user_order")
async def get_user_order(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    order=db.query(Order).filter_by(user_id=user.id).all()

@item.post('/delete_order')
async def delete_order(orderid:int,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    order=db.query(Order).filter_by(id=orderid).first()
    try:
        db.delete(order)
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        return {"code":500,"message":e}
