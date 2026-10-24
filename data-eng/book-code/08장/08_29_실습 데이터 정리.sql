-- 3단계에서 동점 실험용으로 넣은 행을 지웁니다
SELECT * FROM monthly_sales WHERE category = '생활';
DELETE FROM monthly_sales WHERE category = '생활';
SELECT COUNT(*) FROM monthly_sales;
