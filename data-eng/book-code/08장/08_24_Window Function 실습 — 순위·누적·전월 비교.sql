-- 같은 OVER 절을 여러 번 쓰면 WINDOW 절로 이름을 붙일 수 있습니다
SELECT category, ym, amount,
       SUM(amount) OVER w AS running_total,
       LAG(amount) OVER w AS prev_amount
FROM monthly_sales
WINDOW w AS (PARTITION BY category ORDER BY ym)
ORDER BY category, ym;
