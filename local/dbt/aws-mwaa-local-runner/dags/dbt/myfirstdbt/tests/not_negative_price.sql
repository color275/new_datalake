-- 특정 테이블에서 음수 레코드가 있는지 확인. 
-- 만약 결과가 반환되면, 테스트는 실패한 것으로 간주
SELECT *
FROM {{ ref('stg_orders') }}
WHERE order_price < 0