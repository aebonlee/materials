-- 공동 1위를 모두 보고 싶다면 RANK로 바꿉니다
WITH ranked AS (
  SELECT category, ym, amount,
         RANK() OVER (PARTITION BY ym ORDER BY amount DESC) AS rnk
  FROM monthly_sales
)
SELECT ym, category, amount
FROM ranked
WHERE rnk = 1
ORDER BY ym, category;
