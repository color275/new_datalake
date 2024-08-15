WITH orders AS (
    SELECT
        order_id,
        promo_id,
        order_cnt,
        order_price,
        order_dt,
        customer_id,
        product_id,
        -- 총 주문 금액 계산
        order_cnt * order_price AS total_order_value
    FROM {{source('src','orders')}}
)
SELECT * FROM orders