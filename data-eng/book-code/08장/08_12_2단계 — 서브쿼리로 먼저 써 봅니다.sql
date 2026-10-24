-- 월별 합계가 전체 월 평균 이상인 달만
SELECT ym, total FROM (
  SELECT ym, SUM(amount) AS total FROM monthly_sales GROUP BY ym
) t
WHERE total >= (
  SELECT AVG(total) FROM (
    SELECT ym, SUM(amount) AS total FROM monthly_sales GROUP BY ym
  ) t2
)
ORDER BY ym;
