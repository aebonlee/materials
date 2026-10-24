-- 같은 결과를 CTE로 — 위에서 아래로 읽힙니다
WITH monthly_total AS (
  SELECT ym, SUM(amount) AS total FROM monthly_sales GROUP BY ym
)
SELECT ym, total
FROM monthly_total
WHERE total >= (SELECT AVG(total) FROM monthly_total);

-- 여러 개를 이을 때는 쉼표로 (WITH를 다시 쓰지 않습니다) — 모양만 보여 주는 예라 실행하지 않습니다
WITH a AS (...),
     b AS (SELECT … FROM a)     -- 앞의 CTE를 참조할 수 있습니다
SELECT * FROM b;
