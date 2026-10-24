-- 마우스를 주문한 건수 — 이제 정확한 조인으로
SELECT COUNT(*) AS cnt
FROM order_items oi
JOIN products p ON p.id = oi.product_id
WHERE p.name = '무선 마우스';

-- 고객별 주문 금액 합계
SELECT c.name,
       COUNT(DISTINCT o.id)            AS order_count,
       SUM(oi.quantity * oi.unit_price) AS total_amount
FROM customers c
JOIN orders o      ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
GROUP BY c.id, c.name
ORDER BY total_amount DESC;
