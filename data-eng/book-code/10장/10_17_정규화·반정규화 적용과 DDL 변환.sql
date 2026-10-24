-- 지금 주문 금액
SELECT oi.order_id, p.name, oi.unit_price AS 주문시점가격, p.price AS 현재가격
FROM order_items oi JOIN products p ON p.id = oi.product_id
WHERE oi.order_id = 1;

-- 상품 가격이 인상됐다고 해 봅시다
UPDATE products SET price = 95000 WHERE id = 3;

-- 다시 조회 — 과거 주문 금액은 그대로여야 합니다
SELECT oi.order_id, p.name, oi.unit_price AS 주문시점가격, p.price AS 현재가격
FROM order_items oi JOIN products p ON p.id = oi.product_id
WHERE oi.order_id = 1;

-- 원복
UPDATE products SET price = 89000 WHERE id = 3;
