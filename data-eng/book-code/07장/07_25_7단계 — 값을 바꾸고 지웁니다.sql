-- 습관: 먼저 SELECT로 대상을 확인합니다
SELECT * FROM products WHERE name = '모니터 받침대';

-- 확인했으면 UPDATE
UPDATE products SET stock = 15 WHERE name = '모니터 받침대';
SELECT name, stock FROM products WHERE name = '모니터 받침대';

-- 삭제도 같은 순서로
INSERT INTO products (name, category, price, stock) VALUES ('임시상품', '잡화', 1000, 1);
SELECT * FROM products WHERE name = '임시상품';
DELETE FROM products WHERE name = '임시상품';
SELECT COUNT(*) FROM products;
