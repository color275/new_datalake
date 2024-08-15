WITH customer_data AS (
    SELECT 
        customer_id,
        first_name,
        last_name,
        email,
        phone_number,
        address
    FROM src.customer
),
order_data AS (
    SELECT
        order_id,
        promo_id,
        order_cnt,
        order_price,
        order_dt,
        customer_id,
        product_id
    FROM src.orders
),
product_data AS (
    SELECT
        product_id,
        name AS product_name,
        category,
        price
    FROM src.product
)
SELECT 
    o.order_id,
    o.order_dt,
    o.order_cnt,
    o.order_price,
    c.first_name,
    c.last_name,
    c.email,
    c.phone_number,
    c.address,
    p.product_name,
    p.category,
    p.price
FROM order_data o
JOIN customer_data c ON o.customer_id = c.customer_id
JOIN product_data p ON o.product_id = p.product_id