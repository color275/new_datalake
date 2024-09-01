{{
  config(
    materialized='incremental',
    unique_key=['order_dt','product_id'],
    incremental_strategy='delete+insert',
    tags="hourly",
    pre_hook="{{ insert_trans_history() }}",
    post_hook="{{ update_trans_history() }}"
  )
}}

{% set start = to_kst_str(var('data_interval_start', 'today_00:00')) %}
{% set end = to_kst_str(var('data_interval_end', 'tomorrow_00:00')) %}

WITH customer AS (
    SELECT * FROM {{ ref('stg_customer') }}
),
orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
product AS (
    SELECT * FROM {{ ref('stg_product') }}
)

{% if not is_incremental() %}

SELECT 
    orders.order_dt AS order_dt,
    product.product_id,
    product.name AS product_name,
    product.upper_category AS product_category,
    product.price_category,
    SUM(orders.order_cnt) AS total_order_count,
    SUM(orders.total_order_value) AS total_order_value,
    {{ now_string() }} as last_batch_time
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

{% else %}

SELECT 
    orders.order_dt AS order_dt,
    product.product_id,
    product.name AS product_name,
    product.upper_category AS product_category,
    product.price_category,
    SUM(orders.order_cnt) AS total_order_count,
    SUM(orders.total_order_value) AS total_order_value,
    {{ now_string() }} as last_batch_time
FROM orders
JOIN customer ON orders.customer_id = customer.customer_id
JOIN product ON orders.product_id = product.product_id
WHERE 
        orders.last_update_time >= {{ start }}
    AND orders.last_update_time < {{ end }}
GROUP BY 
    orders.order_dt,
    product.product_id,
    product.name,
    product.upper_category,
    product.price_category
ORDER BY 
    order_dt,
    product_id

{% endif %}