-- GROUP BY — 3행으로 접힙니다
SELECT category, SUM(amount) AS total
FROM monthly_sales
GROUP BY category;

-- Window — 9행 그대로, 옆에 합계가 붙습니다
SELECT category, ym, amount,
       SUM(amount) OVER (PARTITION BY category) AS cat_total
FROM monthly_sales
ORDER BY category, ym;
