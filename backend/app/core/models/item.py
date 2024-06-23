from sqlalchemy import Column, Integer, Float, VARCHAR, DateTime, Boolean
from app.database import Base

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(VARCHAR(50))
    describe = Column(VARCHAR(1500))
    stock=Column(Integer)
    create_time = Column(DateTime)
    prince = Column(Float)
    create_user=Column(Integer)
    img_path=Column(VARCHAR(1000))

class Order(Base):
    __tablename__ = 'order'

    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer)
    itemid=Column(Integer)
    quantity=Column(Integer)
    order_type = Column(VARCHAR(200))
    status=Column(VARCHAR(1))
    toal_price=Column(Float)
    address = Column(VARCHAR(1000))
    phone =Column(Integer)
    create_time = Column(DateTime)
