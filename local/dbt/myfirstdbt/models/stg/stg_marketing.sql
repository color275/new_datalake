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
    FROM {{source('stg','marketing')}}
)
SELECT * FROM marketing