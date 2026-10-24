SELECT category, ym, amount,
       LAG(amount)  OVER (PARTITION BY category ORDER BY ym) AS prev_amount,
       amount - LAG(amount) OVER (PARTITION BY category ORDER BY ym) AS diff,
       ROUND(
         (amount - LAG(amount) OVER (PARTITION BY category ORDER BY ym)) * 100.0
         / LAG(amount) OVER (PARTITION BY category ORDER BY ym), 1
       ) AS pct_change
FROM monthly_sales
WHERE category IN ('전자', '잡화', '식품')
ORDER BY category, ym;
