from fastapi import APIRouter, HTTPException, Depends, FastAPI
from models import Order, Customer, Product
from database import PrimaryEngineConn, ReadonlyEngineConn
from datetime import datetime
import random
from config import host, create_dict_from_rows
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter(prefix="/order")

primary = PrimaryEngineConn()
readonly = ReadonlyEngineConn()


@router.get("/")
async def get_all(login_id: int, session: Session = Depends(readonly.get_session)):
    result = session.query(Order).all()
    return result


@router.get("/get")
async def get_order(login_id: int, order_id: int, session: Session = Depends(readonly.get_session)):
    order = session.query(Order).filter(Order.order_id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Data not found")

    order_dict = order.__dict__
    order_dict.pop("_sa_instance_state")
    order_dict.update(host())

    session.close()
    return order_dict


@router.get("/recent")
async def get_recent_orders(login_id: int, minute: int, session: Session = Depends(readonly.get_session)):
    query = f"""
        select /* sqlid : order-recent */ o.*, c.username as customer_name, p.name as product_name
        from orders o
        join customer c on o.customer_id = c.customer_id
        join product p on o.product_id = p.product_id
        -- 수정된 부분 시작
        where o.last_update_time >= now() - interval '{minute} minute'
        -- 수정된 부분 끝
        order by o.last_update_time desc
        limit 20
    """

    result = session.execute(text(query))
    rows = result.fetchall()
    columns = result.keys()

    if not rows:
        raise HTTPException(
            status_code=404, detail="recent 1 minute orders not found")

    return_val = create_dict_from_rows(rows, columns)

    return return_val


@router.post("/pay")
async def order(login_id: int, customer_id: int, product_id: int, session: Session = Depends(primary.get_session)):
    customer = session.query(Customer).filter(
        Customer.customer_id == customer_id).first()
    product = session.query(Product).filter(
        Product.product_id == product_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Data not found")
    if not product:
        raise HTTPException(status_code=404, detail="Data not found")

    order_cnt = random.randint(1, 5)
    order_dt = datetime.now().strftime("%Y-%m-%d")
    order = Order(
        promo_id=None,
        order_cnt=order_cnt,
        order_price=order_cnt * product.price,
        order_dt=order_dt,
        last_update_time=datetime.now(),
        customer_id=customer_id,
        product_id=product_id
    )

    session.add(order)
    session.commit()
    session.close()

    msg = {"message": "Order placed successfully"}
    msg.update(host())

    return msg


@router.put("/update")
async def update_order(login_id: int, order_id: int, order_cnt: int, order_price: int, session: Session = Depends(primary.get_session)):
    order = session.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")

    order.order_cnt = order_cnt
    order.order_price = order_price
    order.last_update_time = datetime.now()

    session.commit()
    session.close()

    return {"message": "주문 업데이트가 완료되었습니다."}


@router.get("/popular")
async def get_popular_products(login_id: int, minute: int, session: Session = Depends(readonly.get_session)):
    query = f"""
        select /* sqlid : order-popular */ p.product_id, p.name, count(o.order_cnt) order_cnt
        from product p,
            orders o
        where p.product_id = o.product_id
        -- 수정된 부분 시작
        and o.last_update_time >= now() - interval '{minute} minute'
        -- 수정된 부분 끝
        group by p.product_id, p.name
        order by order_cnt desc
        limit 10
    """

    result = session.execute(text(query))
    rows = result.fetchall()
    columns = result.keys()

    return_val = create_dict_from_rows(rows, columns)

    if not return_val:
        raise HTTPException(status_code=404, detail="Data not found")

    return return_val


@router.get("/vip")
async def get_top_vip_customers(login_id: int, minute: int, session: Session = Depends(readonly.get_session)):
    query = f"""
        select /* sqlid : order-vip */ c.customer_id, c.username, count(o.order_cnt) order_cnt
        from customer c,
            orders o
        where c.customer_id = o.customer_id
        -- 수정된 부분 시작
        and o.last_update_time >= now() - interval '{minute} minute'
        -- 수정된 부분 끝
        group by c.customer_id, c.username
        order by order_cnt desc
        limit 10;
    """

    result = session.execute(text(query))
    rows = result.fetchall()
    columns = result.keys()

    return_val = create_dict_from_rows(rows, columns)

    if not return_val:
        raise HTTPException(status_code=404, detail="Data not found")

    return return_val
