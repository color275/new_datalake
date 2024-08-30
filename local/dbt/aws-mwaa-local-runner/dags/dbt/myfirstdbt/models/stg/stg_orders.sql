{{
  config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    tags="hourly"
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
-- 테이블이 존재하지 않으면 초기 로딩 수행
{% if not is_incremental() %}

SELECT * 
FROM orders

{% else %}

-- 증분 로딩 시 MERGE 사용
SELECT * 
FROM orders
where last_update_time >= ( 
                        select max(last_update_time) 
                        -- this : stg.stg_orders
                        from {{ this }}
                   )

{% endif %}