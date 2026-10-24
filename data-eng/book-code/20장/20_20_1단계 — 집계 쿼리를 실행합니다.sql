-- 고객별 합계
SELECT customer, count(*) AS orders, sum(amount) AS total
FROM iceberg.lakehouse.orders
GROUP BY customer
ORDER BY total DESC;

-- 채널별 · 날짜별
SELECT order_date, channel, count(*) AS cnt, sum(amount) AS revenue
FROM iceberg.lakehouse.orders
GROUP BY order_date, channel
ORDER BY order_date, channel;

-- 8장에서 배운 윈도 함수도 그대로
SELECT order_date, customer, amount,
       sum(amount) OVER (ORDER BY order_date, order_id) AS running
FROM iceberg.lakehouse.orders
ORDER BY order_date, order_id;
