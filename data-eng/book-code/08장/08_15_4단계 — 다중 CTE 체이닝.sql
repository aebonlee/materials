WITH cat_total AS (
  SELECT category, SUM(amount) AS total
  FROM monthly_sales
  GROUP BY category
),
grand AS (
  SELECT SUM(total) AS grand_total FROM cat_total
)
SELECT c.category,
       c.total,
       ROUND(c.total * 100.0 / g.grand_total, 1) AS pct
FROM cat_total c
CROSS JOIN grand g
ORDER BY c.total DESC;
