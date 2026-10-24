-- 행이 유지되니 "이 달이 카테고리에서 몇 %인가"를 한 번에 구할 수 있습니다
SELECT category, ym, amount,
       SUM(amount) OVER (PARTITION BY category) AS cat_total,
       ROUND(amount * 100.0 / SUM(amount) OVER (PARTITION BY category), 1) AS pct
FROM monthly_sales
ORDER BY category, ym;
