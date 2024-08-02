import random
import datetime
import psycopg2
import time
import os
from faker import Faker
from dotenv import load_dotenv

# Example usage
# 1. product
# 2. basket
# 3. order
weights = [7, 2, 1]
product_ids = list(range(1, 21))  # 상품 ID 1부터 20까지
product_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

fake = Faker()

load_dotenv()
db_config = {
    'host': os.getenv('POSTGRES_HOST'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'database': os.getenv('POSTGRES_DB'),
}

def connect_to_database(config):
    try:
        connection = psycopg2.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            dbname=config['database']
        )
        return connection
    except psycopg2.Error as err:
        print(f"Error: {err}")
        return None

def get_max_order_id(connection):
    query = "SELECT MAX(order_id) AS max_id FROM ly1_raw.orders"
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if result[0] is None:
                return 1
            return result[0] + 1
        except psycopg2.Error as err:
            print(f"Error: {err}")
            return 1

def insert_order_to_database(connection, promo_id, order_cnt, order_price, order_dt, customer_id, product_id):
    query = """
    INSERT INTO ly1_raw.orders (promo_id, order_cnt, order_price, order_dt, customer_id, product_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (promo_id, order_cnt, order_price, order_dt, customer_id, product_id)
    
    with connection.cursor() as cursor:
        try:
            cursor.execute(query, values)
            connection.commit()
            print("Order inserted successfully.")
        except psycopg2.Error as err:
            print(f"Error: {err}")

def get_weights_for_product(connection, product_id):
    query = """
    SELECT products_weight, basket_weight, order_weight 
    FROM ly1_raw.product_type_weights 
    WHERE product_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            return None

def generate_log_entry(order_id_counter, timestamp, fake, connection):
    client_ip = fake.ipv4()
    product_id = random.choices(product_ids, weights=product_weights, k=1)[0]  # 가중치에 따라 상품 ID 선택
    customer_id = random.randint(1, 100)

    weights = get_weights_for_product(connection, product_id)
    if not weights:
        return None, order_id_counter

    request_types = ['products', 'basket', 'order']
    request_type = random.choices(request_types, weights=weights, k=1)[0]
    print(request_type)

    if request_type == 'products':
        request_line = f'"GET /products?product_id={product_id}&customer_id={customer_id} HTTP/1.1"'
    elif request_type == 'basket':
        request_line = f'"GET /basket?product_id={product_id}&customer_id={customer_id} HTTP/1.1"'
    else:  # 'order'
        request_line = f'"GET /order?order_id={order_id_counter}&product_id={product_id}&customer_id={customer_id} HTTP/1.1"'
        order_id_counter += 1

    log_entry = f"{timestamp} {client_ip} - - {request_line} 200 1576\n"
    return log_entry, order_id_counter, request_type, product_id, customer_id

def update_random_order(connection):
    select_query = "SELECT order_id FROM ly1_raw.orders ORDER BY RANDOM() LIMIT 1"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result:
            order_id = result[0]
            new_order_cnt = random.randint(1, 10)
            new_order_price = random.randint(5, 50) * 1000
            new_order_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            last_update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            update_query = """
            UPDATE ly1_raw.orders SET
                order_cnt = %s,
                order_price = %s,
                order_dt = %s,
                last_update_time = %s
            WHERE order_id = %s
            """
            update_values = (new_order_cnt, new_order_price, new_order_dt, last_update_time, order_id)
            cursor.execute(update_query, update_values)
            connection.commit()
            print(f"Order {order_id} updated successfully.")

            
def write_logs_with_db_insertion(db_config, cnt_per_sec):
    db_connection = connect_to_database(db_config)
    if db_connection is None:
        return
    
    order_id_counter = get_max_order_id(db_connection)
    
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"./accesslog/access.log.{today_date}"

    i = 0
    while True:
        timestamp = datetime.datetime.now().strftime("|%Y-%m-%d %H:%M:%S|")
        log_entry, order_id_counter, request_type, product_id, customer_id = generate_log_entry(order_id_counter, timestamp, fake, db_connection)
        
        with open(filename, 'a') as file:
            file.write(log_entry)
            
        if request_type == "order":
            promo_id = f'PROMO{random.randint(1, 20):02d}'
            order_cnt = random.randint(1, 10)
            order_price = random.randint(5, 50) * 1000
            order_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if random.choices([True, False], weights=[9, 1], k=1)[0]:
                insert_order_to_database(db_connection, promo_id, order_cnt, order_price, order_dt, customer_id, product_id)
            else:
                update_random_order(db_connection)
        
        i += 1
        if i % cnt_per_sec == 0:
            time.sleep(1)
            i = 0

# 초당 5건
cnt_per_sec = 5

write_logs_with_db_insertion(db_config, cnt_per_sec)