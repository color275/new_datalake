{{
  config(
    tags="daily"
  )
}}

WITH customer AS (
    SELECT 
        customer_id,
        username,
        first_name,
        last_name,
        email,
        CONCAT(first_name, ' ', last_name) AS full_name,
        EXTRACT(YEAR FROM date_joined) AS signup_year,
        CASE
            WHEN phone_number LIKE '+%' THEN SUBSTRING(phone_number FROM 1 FOR POSITION('-' IN phone_number) - 1)
            ELSE NULL
        END AS country_code,
        last_update_time
    from {{source('src','customer')}}
)

SELECT * FROM customer