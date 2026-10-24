-- 동점을 하나 만들어 세 함수의 차이를 봅니다
INSERT INTO monthly_sales (category, ym, amount) VALUES ('생활', '2026-01', 1200);

SELECT category, amount,
       ROW_NUMBER() OVER (ORDER BY amount DESC) AS rn,
       RANK()       OVER (ORDER BY amount DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY amount DESC) AS dense
FROM monthly_sales WHERE ym = '2026-01'
ORDER BY amount DESC;
