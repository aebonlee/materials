-- CTE로 한 겹 감싸면 됩니다
WITH ranked AS (
  SELECT category, ym, amount,
         ROW_NUMBER() OVER (PARTITION BY ym ORDER BY amount DESC) AS rn
  FROM monthly_sales
)
SELECT ym, category, amount
FROM ranked
WHERE rn = 1
ORDER BY ym;
