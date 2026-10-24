-- CTE만 따로 실행해 중간 결과를 눈으로 확인할 수도 있습니다
WITH monthly_total AS (
  SELECT ym, SUM(amount) AS total FROM monthly_sales GROUP BY ym
)
SELECT * FROM monthly_total;
