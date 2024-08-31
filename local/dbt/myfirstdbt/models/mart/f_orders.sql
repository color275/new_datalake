{{
  config(
    tags="daily"
  )
}}

{% set start_date = var('start_date', '2022-01-01') %}

WITH customer AS (
    SELECT * FROM {{ ref('stg_customer') }}
),
orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
product AS (
    SELECT * FROM {{ ref('stg_product') }}
)

-- 주문 정보 요약 테이블 생성
SELECT 
    '{{ start_date }}' AS start_date,
    orders.order_dt AS order_dt,
    product.product_id,
    product.name AS product_name,
    product.upper_category AS product_category,
    product.price_category,
    SUM(orders.order_cnt) AS total_order_count,
    SUM(orders.total_order_value) AS total_order_value
FROM orders
JOIN customer ON orders.customer_id = customer.customer_id
JOIN product ON orders.product_id = product.product_id
GROUP BY 
    orders.order_dt,
    product.product_id,
    product.name,
    product.upper_category,
    product.price_category
ORDER BY 
    order_dt,
    product_id