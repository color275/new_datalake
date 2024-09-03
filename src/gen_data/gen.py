import psycopg2
import time
from datetime import datetime
import psycopg2.extras
import random
import sys
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 설정
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

# 최대 order_id 조회
def get_max_order_id():
    cur.execute("SELECT COALESCE(MAX(order_id), 0) FROM src.orders")
    max_order_id = cur.fetchone()[0]
    return max_order_id

# 기존 order_dt, customer_id, product_id를 가져오는 함수
def get_existing_order_data(order_id):
    cur.execute(
        "SELECT order_dt, customer_id, product_id FROM src.orders WHERE order_id = %s", (order_id,))
    return cur.fetchone()

# 초당 삽입할 데이터 건수 설정
def insert_bulk_data(batch_size):
    order_id_start = get_max_order_id() + 1  # 최대 order_id의 다음 번호부터 시작

    insert_count = 0
    update_count = 0
    delete_count = 0

    while True:
        start_time = time.time()
        insert_query = """
            INSERT INTO src.orders (order_id, str_order_id, promo_id, order_cnt, order_price, order_dt, last_update_time, customer_id, product_id)
            VALUES %s
        """
        values = []
        for i in range(batch_size):  # batch_size 만큼 삽입
            order_id = order_id_start + i
            str_order_id = f"abc{str(order_id).zfill(12)}"  # 'abc' + order_id 형식으로 만듦
            promo_id = f"PROMO{random.randint(1, 100):03d}"
            order_cnt = random.randint(1, 10)
            order_price = random.randint(1000, 100000)
            order_dt = datetime.now().strftime('%Y-%m-%d')  # 현재 날짜로 설정
            last_update_time = datetime.now()
            customer_id = random.randint(1, 100)
            product_id = random.randint(1, 20)

            action = random.choices(
                ["insert", "update", "delete"], weights=[50, 50, 0], k=1)[0]

            if action == "insert":
                values.append((order_id, str_order_id, promo_id, order_cnt, order_price,
                              order_dt, last_update_time, customer_id, product_id))
                insert_count += 1
            elif action == "update":
                if order_id_start > 1:
                    existing_order_id = random.randint(1, order_id_start - 1)
                    existing_data = get_existing_order_data(existing_order_id)
                    cur.execute("""
                        UPDATE src.orders
                        SET promo_id = %s, order_cnt = %s, order_price = %s, last_update_time = %s
                        WHERE order_id = %s
                    """, (promo_id, order_cnt, order_price, last_update_time, existing_order_id))
                    update_count += 1
            elif action == "delete":
                if order_id_start > 1:
                    cur.execute("DELETE FROM src.orders WHERE order_id = %s",
                                (random.randint(1, order_id_start - 1),))
                    delete_count += 1

        if values:
            psycopg2.extras.execute_values(cur, insert_query, values)

        conn.commit()

        order_id_start += batch_size  # 다음 벌크 삽입을 위해 order_id 업데이트

        elapsed_time = time.time() - start_time
        time.sleep(max(0, 1 - elapsed_time))  # 삽입 후 남은 시간을 대기

        print(
            f"Inserted: {insert_count}, Updated: {update_count}, Deleted: {delete_count}")


# 실행 시 batch_size 값을 파라미터로 받음
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <batch_size>")
        sys.exit(1)

    batch_size = int(sys.argv[1])
    try:
        insert_bulk_data(batch_size)
    except KeyboardInterrupt:
        print("데이터 삽입 중단")
    finally:
        cur.close()
        conn.close()


# import psycopg2
# import time
# from datetime import datetime
# import psycopg2.extras
# import random

# # 데이터베이스 연결 설정
# conn = psycopg2.connect(
#     dbname="ecommerce",
#     user="admin",
#     password="Admin1234",
#     host="0.0.0.0",
#     port="5432"
# )
# cur = conn.cursor()

# # 최대 order_id 조회
# def get_max_order_id():
#     cur.execute("SELECT COALESCE(MAX(order_id), 0) FROM src.orders")
#     max_order_id = cur.fetchone()[0]
#     return max_order_id

# # 초당 삽입할 데이터 건수 설정
# def insert_bulk_data(batch_size):
#     order_id_start = get_max_order_id() + 1  # 최대 order_id의 다음 번호부터 시작

#     insert_count = 0
#     update_count = 0
#     delete_count = 0

#     while True:
#         start_time = time.time()
#         insert_query = """
#             INSERT INTO src.orders (order_id, promo_id, order_cnt, order_price, order_dt, last_update_time, customer_id, product_id)
#             VALUES %s
#         """
#         values = []
#         for i in range(batch_size):  # batch_size 만큼 삽입
#             order_id = order_id_start + i
#             promo_id = f"PROMO{random.randint(1, 100):03d}"  # PROMO001, PROMO002 등
#             order_cnt = random.randint(1, 10)  # 1에서 10 사이의 랜덤 값
#             order_price = random.randint(1000, 100000)  # 1000원에서 100000원 사이의 랜덤 값
#             order_dt = datetime.now().strftime('%Y-%m-%d')
#             last_update_time = datetime.now()
#             customer_id = random.randint(1, 100)  # 1에서 100 사이의 랜덤 값
#             product_id = random.randint(1, 20)  # 1에서 20 사이의 랜덤 값

#             # 가중치 기반으로 작업 선택 (80% 삽입, 18% 업데이트, 2% 삭제)
#             action = random.choices(["insert", "update", "delete"], weights=[80, 18, 2], k=1)[0]

#             if action == "insert":
#                 values.append((order_id, promo_id, order_cnt, order_price, order_dt, last_update_time, customer_id, product_id))
#                 insert_count += 1
#             elif action == "update":
#                 if order_id_start > 1:
#                     cur.execute("""
#                         UPDATE src.orders
#                         SET promo_id = %s, order_cnt = %s, order_price = %s, order_dt = %s, last_update_time = %s, customer_id = %s, product_id = %s
#                         WHERE order_id = %s
#                     """, (promo_id, order_cnt, order_price, order_dt, last_update_time, customer_id, product_id, random.randint(1, order_id_start - 1)))
#                     update_count += 1
#             elif action == "delete":
#                 if order_id_start > 1:
#                     cur.execute("DELETE FROM src.orders WHERE order_id = %s", (random.randint(1, order_id_start - 1),))
#                     delete_count += 1

#         if values:
#             psycopg2.extras.execute_values(cur, insert_query, values)

#         conn.commit()

#         order_id_start += batch_size  # 다음 벌크 삽입을 위해 order_id 업데이트

#         elapsed_time = time.time() - start_time
#         time.sleep(max(0, 1 - elapsed_time))  # 삽입 후 남은 시간을 대기

#         # 작업의 결과 출력
#         print(f"Inserted: {insert_count}, Updated: {update_count}, Deleted: {delete_count}")

# # 데이터 삽입 시작
# try:
#     batch_size = 100  # 이 값을 조정하여 초당 삽입할 데이터 건수 설정
#     insert_bulk_data(batch_size)
# except KeyboardInterrupt:
#     print("데이터 삽입 중단")
# finally:
#     cur.close()
#     conn.close()