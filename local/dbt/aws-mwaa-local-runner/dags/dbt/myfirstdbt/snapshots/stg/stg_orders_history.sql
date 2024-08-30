{% snapshot stg_orders_history %}

{{
    config(
        target_schema='stg',
        unique_key='order_id',
        strategy='timestamp',
        updated_at='last_update_time'
    )
}}

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
        order_cnt * order_price AS total_order_value,
        {{ timestamp_to_string('last_update_time') }} AS last_update_time,
        {{ now_string() }} as last_batch_time
    FROM {{source('src','orders')}}
)
SELECT * 
FROM orders

{% endsnapshot %}