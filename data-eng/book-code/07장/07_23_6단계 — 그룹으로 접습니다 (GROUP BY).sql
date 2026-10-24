SELECT category,
       COUNT(*)   AS item_count,
       AVG(price) AS avg_price,
       SUM(stock) AS total_stock,
       MAX(price) AS max_price
FROM products
GROUP BY category;
