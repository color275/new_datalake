from fastapi import APIRouter
from fastapi import HTTPException
from models import *
from database import PrimaryEngineConn, ReadonlyEngineConn
from datetime import datetime
import random
from config import *
from datetime import datetime, timedelta
from sqlalchemy import desc
from sqlalchemy import func
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter(
    prefix="/product",
)

primary = PrimaryEngineConn()
readonly = ReadonlyEngineConn()

@router.get("/")
async def get_all(login_id: int, session: Session = Depends(readonly.get_session)):
    result = session.query(Product).all()
    return result

@router.get("/get")
async def get_product(login_id: int, product_id: int, session: Session = Depends(readonly.get_session)):
    product = session.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_dict = product.__dict__
    product_dict.pop("_sa_instance_state")

    product_dict.update(host())

    return product_dict

# @router.post("/order")
# async def make_order(customer_id: int, product_id: int):
#     response = httpx.post(f"http://{ORDER_SERVICE}/order/pay", params={"customer_id": customer_id, "product_id": product_id})

#     return response.json()



