-- 없는 고객(99번)으로 주문을 넣어 봅니다 (실패해야 정상)
INSERT INTO orders (customer_id, ordered_at) VALUES (99, '2026-09-03 09:00:00');

-- 주문이 걸려 있는 고객을 지워 봅니다 (실패해야 정상)
DELETE FROM customers WHERE id = 1;
