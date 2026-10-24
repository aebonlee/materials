-- 비싼 순으로 상위 3개
SELECT name, price FROM products ORDER BY price DESC LIMIT 3;

-- 카테고리로 먼저 묶고, 그 안에서 가격 낮은 순
SELECT category, name, price FROM products
ORDER BY category ASC, price ASC;

-- 4번째부터 2개 (페이지 넘기기에 쓰입니다)
SELECT name, price FROM products ORDER BY price DESC LIMIT 2 OFFSET 3;
