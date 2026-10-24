WITH monthly_total AS (
  SELECT ym, SUM(amount) AS total
  FROM monthly_sales
  GROUP BY ym
)
SELECT ym, total
FROM monthly_total
WHERE total >= (SELECT AVG(total) FROM monthly_total)
ORDER BY ym;
