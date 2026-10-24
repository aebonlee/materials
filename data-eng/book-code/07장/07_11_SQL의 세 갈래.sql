-- DDL: 구조를 만든다 (Data Definition Language)
CREATE TABLE products (...);
ALTER TABLE products ADD COLUMN memo TEXT;
DROP TABLE products;

-- DML: 데이터를 바꾼다 (Data Manipulation Language)
INSERT INTO products (name) VALUES ('텀블러');
UPDATE products SET price = 20000 WHERE id = 1;
DELETE FROM products WHERE id = 1;

-- 조회
SELECT name, price FROM products WHERE price > 20000;
