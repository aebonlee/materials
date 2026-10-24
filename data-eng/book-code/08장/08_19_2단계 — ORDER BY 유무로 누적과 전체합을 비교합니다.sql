SELECT category, ym, amount,
       SUM(amount) OVER (PARTITION BY category)               AS total_no_order,
       SUM(amount) OVER (PARTITION BY category ORDER BY ym)   AS running_total
FROM monthly_sales
WHERE category = '전자'
ORDER BY ym;
