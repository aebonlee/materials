-- 갱신 이상: 김하나가 번호를 바꿨는데 한 곳만 고쳤다고 해 봅시다
UPDATE bad_orders SET customer_tel = '010-9999-8888' WHERE order_id = 1;

SELECT customer_name, customer_tel FROM bad_orders WHERE customer_name = '김하나';
-- 같은 사람인데 번호가 둘입니다. 어느 것이 진짜인지 DB는 모릅니다.

-- 1NF 위반의 불편: 마우스를 주문한 건수를 세려면?
SELECT COUNT(*) FROM bad_orders WHERE product_names LIKE '%마우스%';
-- 2가 나옵니다. 그런데 LIKE는 인덱스를 못 타고, 나중에 "마우스패드"가 들어오면 그것까지 셉니다.
