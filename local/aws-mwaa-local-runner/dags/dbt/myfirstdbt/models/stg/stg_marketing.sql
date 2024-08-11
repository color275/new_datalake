{{
  config(
    tags="daily"
  )
}}

WITH marketing AS (
    SELECT 
        product_id,
        campaign_name,
        budget,
        start_date,
        end_date
    FROM src.marketing
)
SELECT * FROM marketing