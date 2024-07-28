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
        where o.last_update_time >= date_sub(now(), interval {minute} minute)
        order by o.last_update_time desc
        limit 20
    """

    result = session.execute(text(query))
    rows = result.fetchall()
    columns = result.keys()

    if not rows:
        raise HTTPException(status_code=404, detail="recent 1 minute orders not found")

    return_val = create_dict_from_rows(rows, columns)

    return return_val

@router.post("/pay")
async def order(login_id: int, customer_id: int, product_id: int, session: Session = Depends(primary.get_session)):
    customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
    product = session.query(Product).filter(Product.product_id == product_id).first()

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
        and o.last_update_time >= date_sub(now(), interval {minute} minute)
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
        and o.last_update_time >= date_sub(now(), interval {minute} minute)
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


@router.get("/sql")
async def get_sql(sql_id: int,  session: Session = Depends(readonly.get_session)):
    sqls = [
 "SELECT /* id: 1 */ * FROM product LIMIT 10;"
,"SELECT /* id: 2 */ * FROM customer LIMIT 10;"
,"SELECT /* id: 3 */ * FROM orders WHERE orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 4 */ * FROM product JOIN customer ON product.id = customer.id LIMIT 10;"
,"SELECT /* id: 5 */ * FROM product JOIN orders ON product.id = orders.prd_id LIMIT 10;"
,"SELECT /* id: 6 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 7 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id LIMIT 10;"
,"SELECT /* id: 8 */ * FROM product WHERE price > 100 LIMIT 10;"
,"SELECT /* id: 9 */ * FROM customer WHERE age > 30 LIMIT 10;"
,"SELECT /* id: 10 */ * FROM orders WHERE order_price > 500 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 11 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price > 100 LIMIT 10;"
,"SELECT /* id: 12 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price > 500 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 13 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age > 30 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 14 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price > 500 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 15 */ * FROM product WHERE price BETWEEN 50 AND 100 LIMIT 10;"
,"SELECT /* id: 16 */ * FROM customer WHERE age BETWEEN 20 AND 30 LIMIT 10;"
,"SELECT /* id: 17 */ * FROM orders WHERE order_price BETWEEN 300 AND 600 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 18 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price BETWEEN 50 AND 100 LIMIT 10;"
,"SELECT /* id: 19 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price BETWEEN 300 AND 600 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 20 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age BETWEEN 20 AND 30 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 21 */ * FROM product WHERE price > 200 LIMIT 10;"
,"SELECT /* id: 22 */ * FROM customer WHERE age > 40 LIMIT 10;"
,"SELECT /* id: 23 */ * FROM orders WHERE order_price > 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 24 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price > 200 LIMIT 10;"
,"SELECT /* id: 25 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price > 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 26 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age > 40 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 27 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price > 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 28 */ * FROM product WHERE price BETWEEN 100 AND 200 LIMIT 10;"
,"SELECT /* id: 29 */ * FROM customer WHERE age BETWEEN 30 AND 40 LIMIT 10;"
,"SELECT /* id: 30 */ * FROM orders WHERE order_price BETWEEN 600 AND 900 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 31 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price BETWEEN 100 AND 200 LIMIT 10;"
,"SELECT /* id: 32 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price BETWEEN 600 AND 900 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 33 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age BETWEEN 30 AND 40 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 34 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price BETWEEN 600 AND 900 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 35 */ * FROM product WHERE price < 50 LIMIT 10;"
,"SELECT /* id: 36 */ * FROM customer WHERE age < 20 LIMIT 10;"
,"SELECT /* id: 37 */ * FROM orders WHERE order_price < 200 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 38 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price < 50 LIMIT 10;"
,"SELECT /* id: 39 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price < 200 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 40 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age < 20 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 41 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price < 200 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 42 */ * FROM product WHERE price = 50 LIMIT 10;"
,"SELECT /* id: 43 */ * FROM customer WHERE age = 20 LIMIT 10;"
,"SELECT /* id: 44 */ * FROM orders WHERE order_price = 200 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 45 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price = 50 LIMIT 10;"
,"SELECT /* id: 46 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price = 200 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 47 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age = 20 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 48 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price = 200 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 49 */ * FROM product WHERE price <> 50 LIMIT 10;"
,"SELECT /* id: 50 */ * FROM customer WHERE age <> 20 LIMIT 10;"
,"SELECT /* id: 51 */ * FROM orders WHERE order_price <> 200 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 52 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price <> 50 LIMIT 10;"
,"SELECT /* id: 53 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price <> 200 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 54 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age <> 20 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 55 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price <> 200 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 56 */ * FROM product WHERE price IN (50, 100, 150) LIMIT 10;"
,"SELECT /* id: 57 */ * FROM customer WHERE age IN (20, 30, 40) LIMIT 10;"
,"SELECT /* id: 58 */ * FROM orders WHERE order_price IN (200, 400, 600) AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 59 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price IN (50, 100, 150) LIMIT 10;"
,"SELECT /* id: 60 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price IN (200, 400, 600) AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 61 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age IN (20, 30, 40) AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 62 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price IN (200, 400, 600) AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 63 */ * FROM product WHERE price NOT IN (50, 100, 150) LIMIT 10;"
,"SELECT /* id: 64 */ * FROM customer WHERE age NOT IN (20, 30, 40) LIMIT 10;"
,"SELECT /* id: 65 */ * FROM orders WHERE order_price NOT IN (200, 400, 600) AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 66 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price NOT IN (50, 100, 150) LIMIT 10;"
,"SELECT /* id: 67 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price NOT IN (200, 400, 600) AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 68 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age NOT IN (20, 30, 40) AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 69 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price NOT IN (200, 400, 600) AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 70 */ * FROM product WHERE price IS NULL LIMIT 10;"
,"SELECT /* id: 71 */ * FROM customer WHERE age IS NULL LIMIT 10;"
,"SELECT /* id: 72 */ * FROM orders WHERE order_price IS NULL AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 73 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price IS NULL LIMIT 10;"
,"SELECT /* id: 74 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price IS NULL AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 75 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age IS NULL AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 76 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price IS NULL AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 77 */ * FROM product WHERE price IS NOT NULL LIMIT 10;"
,"SELECT /* id: 78 */ * FROM customer WHERE age IS NOT NULL LIMIT 10;"
,"SELECT /* id: 79 */ * FROM orders WHERE order_price IS NOT NULL AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 80 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price IS NOT NULL LIMIT 10;"
,"SELECT /* id: 81 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price IS NOT NULL AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 82 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age IS NOT NULL AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 83 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price IS NOT NULL AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 84 */ * FROM product WHERE price >= 100 LIMIT 10;"
,"SELECT /* id: 85 */ * FROM customer WHERE age >= 30 LIMIT 10;"
,"SELECT /* id: 86 */ * FROM orders WHERE order_price >= 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 87 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price >= 100 LIMIT 10;"
,"SELECT /* id: 88 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price >= 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 89 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age >= 30 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 90 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price >= 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 91 */ * FROM product WHERE price < 100 LIMIT 10;"
,"SELECT /* id: 92 */ * FROM customer WHERE age < 30 LIMIT 10;"
,"SELECT /* id: 93 */ * FROM orders WHERE order_price < 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 94 */ * FROM product JOIN customer ON product.id = customer.id WHERE product.price < 100 LIMIT 10;"
,"SELECT /* id: 95 */ * FROM product JOIN orders ON product.id = orders.prd_id WHERE orders.order_price < 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 96 */ * FROM customer JOIN orders ON customer.id = orders.cust_id WHERE customer.age < 30 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 97 */ * FROM product JOIN orders ON product.id = orders.prd_id JOIN customer ON orders.cust_id = customer.id WHERE orders.order_price < 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
,"SELECT /* id: 98 */ * FROM product WHERE price <= 100 LIMIT 10;"
,"SELECT /* id: 99 */ * FROM customer WHERE age <= 30 LIMIT 10;"
,"SELECT /* id: 100 */ * FROM orders WHERE order_price <= 1000 AND orders.last_update_time >= date_sub(now(), interval 1 minute) LIMIT 10;"
]

    result = session.execute(text(sqls[sql_id]))
    rows = result.fetchall()
    columns = result.keys()

    return_val = create_dict_from_rows(rows, columns)

    # if not return_val:
    #     raise HTTPException(status_code=404, detail="Data not found")

    return return_val
