SELECT category, ym, amount,
       RANK() OVER (PARTITION BY ym ORDER BY amount DESC)            AS rank_in_month,
       SUM(amount) OVER (PARTITION BY category ORDER BY ym)          AS running_total,
       LAG(amount)  OVER (PARTITION BY category ORDER BY ym)         AS prev_amount,
       amount - LAG(amount) OVER (PARTITION BY category ORDER BY ym) AS diff
FROM monthly_sales
ORDER BY category, ym;
