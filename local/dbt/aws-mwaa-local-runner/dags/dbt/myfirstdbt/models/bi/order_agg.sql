{{
  config(
    tags="hourly"
  )
}}


SELECT 
    p.name AS product_name,
    p.category AS product_category,
    SUM(o.total_order_count) AS total_products_ordered,
    SUM(o.total_order_value) AS total_value_ordered
FROM 
    {{ ref("f_orders") }} o,
    {{ ref("stg_product") }} p
WHERE 
    o.product_id = p.product_id
    and  o.order_dt = TO_CHAR(NOW(), 'YYYY-MM-DD')
GROUP BY 
    p.name, p.category
ORDER BY 
    total_value_ordered DESC