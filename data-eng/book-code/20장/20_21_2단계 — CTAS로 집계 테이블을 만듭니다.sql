CREATE TABLE iceberg.lakehouse.daily_sales AS
SELECT order_date, count(*) AS order_cnt, sum(amount) AS revenue
FROM iceberg.lakehouse.orders
GROUP BY order_date;

SELECT * FROM iceberg.lakehouse.daily_sales ORDER BY order_date;
