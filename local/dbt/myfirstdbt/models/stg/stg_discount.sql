{{
  config(
    tags="daily"
  )
}}

WITH discount AS (
    SELECT 
        product_id,
        discount_rate,
        start_date,
        end_date
    FROM stg.discount
)
SELECT * FROM discount