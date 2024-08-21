{{
  config(
    tags="hourly"
  )
}}

WITH product_sales AS (
    SELECT
        o.product_id,
        COUNT(o.order_id) AS total_sales,
        SUM(o.order_price * o.order_cnt) AS total_revenue
    FROM {{ ref('stg_orders') }} o
    JOIN {{ ref('stg_marketing') }} m ON o.product_id = m.product_id
    WHERE o.order_dt::date BETWEEN m.start_date::date AND m.end_date::date
    GROUP BY o.product_id
),
marketing AS (
    SELECT
        m.product_id,
        m.campaign_name,
        m.budget,
        m.start_date::date AS start_date,
        m.end_date::date AS end_date,
        p.name AS product_name,
        COALESCE(ps.total_sales, 0) AS total_sales,
        COALESCE(ps.total_revenue, 0) AS total_revenue
    FROM {{ ref('stg_marketing') }} m
    JOIN {{ ref('stg_product') }} p ON m.product_id = p.product_id
    LEFT JOIN product_sales ps ON m.product_id = ps.product_id
)
SELECT
    product_id,
    product_name,
    campaign_name,
    budget,
    start_date,
    end_date,
    total_sales,
    total_revenue
FROM marketing
ORDER BY product_id