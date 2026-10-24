-- 정답 예시 — 먼저 직접 해 보신 다음에 보세요
WITH cat_avg AS (
  SELECT category, AVG(amount) AS avg_amount
  FROM monthly_sales
  GROUP BY category
),
overall AS (
  SELECT AVG(avg_amount) AS overall_avg FROM cat_avg
)
SELECT c.category, ROUND(c.avg_amount, 1) AS avg_amount
FROM cat_avg c
CROSS JOIN overall o
WHERE c.avg_amount > o.overall_avg
ORDER BY c.avg_amount DESC;
