-- 서브쿼리 중첩 — 안쪽부터 거꾸로 읽어야 합니다
SELECT ym, total FROM (
  SELECT ym, SUM(amount) AS total FROM monthly_sales GROUP BY ym
) t
WHERE total >= (
  SELECT AVG(total) FROM (
    SELECT ym, SUM(amount) AS total FROM monthly_sales GROUP BY ym
  ) t2
);
-- 같은 집계를 두 번 적고 있습니다. 고칠 때 한쪽만 고치면 조용히 틀립니다.
