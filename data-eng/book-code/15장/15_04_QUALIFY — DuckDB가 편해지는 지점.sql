-- 8장에서 배운 방식 — CTE로 한 겹 감싼다 (어디서나 통함)
WITH ranked AS (
  SELECT region, customer_id, total,
         rank() OVER (PARTITION BY region ORDER BY total DESC) AS rnk
  FROM by_customer
)
SELECT * FROM ranked WHERE rnk <= 3;

-- DuckDB 방식 — QUALIFY로 한 줄
SELECT region, customer_id, total,
       rank() OVER (PARTITION BY region ORDER BY total DESC) AS rnk
FROM by_customer
QUALIFY rnk <= 3;
