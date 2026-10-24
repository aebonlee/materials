-- 전자 카테고리만
SELECT name, price FROM products WHERE category = '전자';

-- 두 조건을 모두 만족 (AND)
SELECT name, price, stock FROM products
WHERE stock > 0 AND price <= 20000;

-- 범위
SELECT name, price FROM products WHERE price BETWEEN 20000 AND 50000;

-- 목록에 포함
SELECT name FROM products WHERE category IN ('전자', '잡화');

-- 부분 일치 (%는 아무 글자 여러 개)
SELECT name FROM products WHERE name LIKE '%키보드%';
