from sqlalchemy import Column, BigInteger, Text, Integer, DateTime, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    promo_id = Column(String(255), default=None)
    order_cnt = Column(Integer, nullable=False)
    order_price = Column(Integer, nullable=False)
    order_dt = Column(String(255), nullable=False)
    last_update_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    customer_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    password = Column(String(128), nullable=False)
    last_login = Column(TIMESTAMP, default=None)
    is_superuser = Column(Integer, nullable=False)
    username = Column(String(150), unique=True, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Integer, nullable=False)
    is_active = Column(Integer, nullable=False)
    date_joined = Column(TIMESTAMP, nullable=False)
    phone_number = Column(String(20), default=None)
    age = Column(Integer, default=None)
    gender = Column(String(10), default=None)
    address = Column(String(200), default=None)
    last_update_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    name = Column(String(255), default=None)

class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)
    img_path = Column(String(255), default=None)
    category = Column(String(255), default=None)
    price = Column(Integer, nullable=False)
    last_update_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())