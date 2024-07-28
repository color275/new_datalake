# locust --host=http://localhost:8000
from locust import HttpUser, task, between
import os
import json
import random
from urllib.parse import urlparse

class MyUser(HttpUser):
    wait_time = between(1, 1)    
    # wait_time = between(0, 0)

    # @task
    # def get_customer(self):
    #     params = {
    #         'login_id': random.randint(1, 100),
    #         'customer_id': random.randint(1, 100)
    #     }
    #     response = self.client.get(f"/customer/get", params=params, name="/customer/get")    
    
    @task(10)
    def get_product(self):
        params = {
            'login_id': random.randint(1, 100),
            'product_id': random.randint(1, 20)
        }
        response = self.client.get(f"/product/get", params=params, name="/product/get")    

    # @task
    # def get_order_details(self):
    #     params = {
    #         'login_id': random.randint(1, 100),
    #         'order_id': random.randint(1, 1000)
    #     }
    #     response = self.client.get(f"/order/get", params=params, name="/order/get")

    @task(3)
    def order(self):

        customer_id = random.randint(1, 100)

        products_with_weights = [
            (7, 6),   
            (11, 4),  
            (14, 3),  
            (20, 2),  
            (1, 1),   
            (2, 1),
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (8, 1),
            (9, 1),
            (10, 1),
            (12, 1),
            (13, 1),
            (15, 1),
            (16, 1),
            (17, 1),
            (18, 1),
            (19, 1)
        ]

        # 상품 선택 (가중치에 따라 선택될 확률이 결정됨)
        product_id = random.choices(*zip(*products_with_weights))[0]


        params = {
            'login_id': customer_id,
            'customer_id': customer_id,
            'product_id': product_id
        }
        response = self.client.post("/order/pay", params=params, name="/order/pay")

    @task(1)
    def order_update(self):
        params = {
            'login_id': random.randint(1, 100),
            'order_id': random.randint(1, 1000),
            'order_cnt': random.randint(1, 10),
            'order_price': random.randint(1000, 100000)
        }
        response = self.client.put("/order/update", params=params, name="/order/update")        


    @task(1)
    def get_order_recent(self):
        params = {
            'login_id': random.randint(1, 100),
            'minute': random.randint(1, 20)
        }
        response = self.client.get(f"/order/recent", params=params, name=f"/order/recent")

    @task(1)
    def get_vip(self):
        params = {
            'login_id': random.randint(1, 100),
            'minute': random.randint(1, 20)
        }
        response = self.client.get(f"/order/vip", params=params, name=f"/order/vip")

    @task(1)
    def get_popular(self):
        params = {
            'login_id': random.randint(1,
                                        100),
            'minute': random.randint(1, 20)
        }
        response = self.client.get(f"/order/popular", params=params, name=f"/order/popular")


    @task(1)
    def get_sql(self):

        params = {
            'sql_id': random.randint(0, 99)
        }
        response = self.client.get(f"/order/sql", params=params, name=f"/order/sql")







