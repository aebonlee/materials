-- 정답 예시
SELECT category, ym, amount,
       ROUND(AVG(amount) OVER (
         PARTITION BY category ORDER BY ym
         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ), 1) AS moving_avg_3m
FROM monthly_sales
WHERE category = '전자'
ORDER BY ym;
