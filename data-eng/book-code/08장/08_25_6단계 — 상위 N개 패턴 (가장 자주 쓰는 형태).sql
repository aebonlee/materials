-- 이렇게 쓰면 실패합니다 (WHERE는 Window 계산보다 먼저입니다)
SELECT category, ym, amount,
       ROW_NUMBER() OVER (PARTITION BY ym ORDER BY amount DESC) AS rn
FROM monthly_sales
WHERE rn = 1;
