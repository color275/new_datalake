-- 이 분석은 지난 1년 동안의 월별 고객 가입 추세를 계산합니다.
WITH customer AS (
    SELECT 
        customer_id,
        date_joined
    FROM {{ ref('stg_customer') }}
)

SELECT
    DATE_TRUNC('month', date_joined) AS month,
    COUNT(customer_id) AS customer_count
FROM customer
WHERE date_joined >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year'
GROUP BY month
ORDER BY month