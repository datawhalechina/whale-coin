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
    # 查询数据库中所有的Item记录
    return db.query(Item).all()

item.post("/get_item_detal")
async def get_item_detal(itemid:int,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    # 查询数据库中的Item表，按照id进行过滤
    # 返回查询结果中的第一条记录
    return db.query(Item).filter_by(id=itemid).first()

@item.post("/add_item")
async def add_item(request: Request,user: UserBase = Depends(check_jwt_token),db: Session = Depends(get_db)):
    # 存储已上传文件的信息
    uploaded_files_info = []

    # 获取表单数据
    form: UploadFile = await request.form()
    name=form.get("name")
    describe=form.get("describe")
    stock=form.get("stock")
    prince=form.get("prince")
    files=form.get("files")

    # 创建一个新的商品对象
    new_item = Item(
        name=name,
        describe=describe,
        stock=stock,
        prince=prince,
    )
    # 设置创建时间和创建用户
    new_item.create_time=datetime.now()
    new_item.create_user=user.id

    # 遍历上传的文件
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
        # 将新商品对象添加到数据库中
        db.add(new_item)
        # 提交事务
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        # 发生异常时返回错误信息
        return {"code":500,"message":e}
@item.post("/delete_item") 
async def delete_item(itemid:int,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    # 查询数据库中对应id的item
    item=db.query(Item).filter_by(id=itemid).first()

    # 将item的img_path按逗号分割成列表
    imgs=item.img_path.split(',')

    # 遍历imgs列表中的每个img
    for img in imgs:
        # 拼接图片路径
        img_path=f"../static/img/{img}"

        # 判断图片路径是否存在
        if os.path.exists(img_path):
            # 删除图片文件
            os.remove(img_path)

    try:
        # 从数据库中删除item
        db.delete(item)
        # 提交数据库事务
        db.commit()
        # 返回成功响应
        return {"code": 200, "message":"OK"}
    except Exception as e:
        # 返回错误响应
        return{"code":500,"message":e}   

@item.get("/get_order")
async def get_order(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    # 查询数据库中所有的订单记录
    return db.query(Order).all()
@item.post("/add_order")
async def add_order(itemid:int=Form(...),quantity:int=Form(...),order_type:str=Form(...),status:str=Form(...),toal_price:float=Form(...),address:str=Form(...),phone:str=Form(...),user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    # 创建一个新的订单对象
    new_order = Order(
        # 设置订单的商品ID
        item_id=itemid,
        # 设置订单的数量
        quantity=quantity,
        # 设置订单的类型
        order_type=order_type,
        # 设置订单的状态
        status=status,
        # 设置订单的总价
        toal_price=toal_price,
        # 设置订单的收货地址
        address=address,
        # 设置订单的联系电话
        phone=phone,
        # 设置订单的创建时间
        create_time=datetime.now(),
        # 设置订单所属用户的ID
        user_id=user.id,
    )
    try:
        # 将新订单添加到数据库会话中
        db.add(new_order)
        # 提交数据库会话，保存订单到数据库
        db.commit()
        # 返回成功响应
        return {"code": 200, "message":"OK"}
    except Exception as e:
        # 捕获异常，返回错误响应
        return {"code":500,"message":e}    
@item.post("/auduit_order")
async def audit_order(orderid:int=Form(),status:str=Form(),user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    # 根据订单id查询订单
    order=db.query(Order).filter_by(id=orderid)
    try:
        # 更新订单状态
        order.status=status
        # 更新审核人id
        order.audit_id=user.id
        # 提交数据库更改
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        # 返回错误信息
        return {"code":500,"message":e}
@item.post("/get_audit_order")
async def get_audit_order(statusId:str,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    # 从数据库中查询订单记录，筛选条件为订单状态等于给定的statusId
    order=db.query(Order).filter_by(status=statusId).all()

@item.post("/get_order_detal")
async def get_order_detal(orderid:int, user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    # 从数据库中查询指定订单id的订单
    order = db.query(Order).filter_by(id=orderid).first()

@item.get("/get_user_order")
async def get_user_order(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    # 根据用户ID查询订单，并返回所有订单对象列表
    order = db.query(Order).filter_by(user_id=user.id).all()

@item.post('/delete_order')
async def delete_order(orderid:int,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    # 查询订单
    order=db.query(Order).filter_by(id=orderid).first()
    try:
        # 删除订单
        db.delete(order)
        # 提交数据库更改
        db.commit()
        # 返回成功消息
        return {"code": 200, "message":"OK"}
    except Exception as e:
        # 返回异常信息
        return {"code":500,"message":e}
