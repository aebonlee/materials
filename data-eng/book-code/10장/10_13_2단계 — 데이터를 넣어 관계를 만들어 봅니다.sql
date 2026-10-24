INSERT INTO customers (name, tel) VALUES
  ('김하나', '010-1111-2222'),
  ('이두리', '010-3333-4444');

INSERT INTO orders (customer_id, ordered_at) VALUES
  (1, '2026-09-01 10:00:00'),
  (1, '2026-09-02 14:30:00'),
  (2, '2026-09-02 16:10:00');

-- 주문 1: 마우스(2번) 1개 + 키보드(3번) 1개
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (1, 2, 1, 28000),
  (1, 3, 1, 89000),
  (2, 4, 1, 19000),
  (3, 2, 1, 28000);

SELECT COUNT(*) FROM order_items;
