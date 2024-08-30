{{
  config(
    tags="daily"
  )
}}

WITH product AS (
    SELECT
        product_id,
        name,
        category,
        price,
        UPPER(category) AS upper_category,
        CASE
            WHEN price <= 10000 THEN 'Low'
            WHEN price <= 20000 THEN 'Medium'
            ELSE 'High'
        END AS price_category,
        last_update_time
    FROM {{source('src','product')}}
)

SELECT * FROM product