CREATE TABLE bad_orders (
  order_id      INT,
  customer_name VARCHAR(50),
  customer_tel  VARCHAR(20),
  product_names VARCHAR(200),   -- '마우스,키보드'처럼 여러 값을 한 칸에
  total_price   INT
);

INSERT INTO bad_orders VALUES
  (1, '김하나', '010-1111-2222', '마우스,키보드', 117000),
  (2, '김하나', '010-1111-2222', '텀블러',        19000),
  (3, '이두리', '010-3333-4444', '마우스',        28000);

SELECT * FROM bad_orders;
