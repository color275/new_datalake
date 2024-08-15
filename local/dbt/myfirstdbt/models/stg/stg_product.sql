WITH product AS (
    SELECT
        product_id,
        name,
        category,
        price,
        -- 카테고리를 대문자로 변환
        UPPER(category) AS upper_category,
        -- 가격 범주화 (예: 0-10000, 10001-20000, 20001 이상)
        CASE
            WHEN price <= 10000 THEN 'Low'
            WHEN price <= 20000 THEN 'Medium'
            ELSE 'High'
        END AS price_category
    FROM {{source('src','product')}}
)

SELECT * FROM product