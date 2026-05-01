-- what is the most popular product?
SELECT product_name, COUNT(quantity) AS "purchase_count" FROM products JOIN order_items
ON products.product_id = order_items.product_id
GROUP BY product_name
ORDER BY purchase_count DESC;

-- is there a relationship between the quantity and delivery date of an order?
SELECT (delivery_date::date - order_date::date) AS "date_diff", quantity
FROM shipping
JOIN orders ON shipping.order_id = orders.order_id
JOIN order_items ON orders.order_id = order_items.order_id
WHERE (delivery_date::date - order_date::date) IS NOT NULL
ORDER BY date_diff ASC;

-- what is the minimum, maximum, median, and average payment of all order? How does this compare to the quantity of items bought?
SELECT quantity, TO_CHAR(MAX(amount), '£999G999G990D00') AS "max", TO_CHAR(MIN(amount), '£999G999G990D00') AS "min", TO_CHAR(ROUND(AVG(amount), 2), '£999G999G990D00') AS "average", TO_CHAR(ROUND(CAST(percentile_cont(0.5) WITHIN GROUP (ORDER BY amount) AS numeric), 2), '£999G999G990D00') AS "median"
FROM payments 
JOIN orders ON payments.order_id = orders.order_id
JOIN order_items ON order_items.order_id = orders.order_id
GROUP BY quantity
ORDER BY quantity DESC;

-- what weeks got the most signups? 
SELECT COUNT(signup_date) AS "week_signup_count", TO_CHAR(date_trunc('week', signup_date), 'YYYY-MM-DD') AS "week_beginning" FROM customers
GROUP BY date_trunc('week', signup_date)
ORDER BY week_signup_count DESC;
-- how does this compare to the most on specific days?
SELECT COUNT(signup_date) AS "signup_count", signup_date FROM customers
GROUP BY signup_date
ORDER BY signup_count DESC;