-- 그룹 결과에 조건을 걸 때는 WHERE가 아니라 HAVING
SELECT category, COUNT(*) AS cnt
FROM products
GROUP BY category
HAVING COUNT(*) >= 3;

-- WHERE와 HAVING을 함께 (순서: WHERE로 행을 거르고 → 묶고 → HAVING으로 그룹을 거른다)
SELECT category, AVG(price) AS avg_price
FROM products
WHERE stock > 0
GROUP BY category
HAVING AVG(price) > 20000;
