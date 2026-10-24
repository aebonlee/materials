-- 이름 없이 넣어 보기 (NOT NULL 위반 → 실패해야 정상)
INSERT INTO products (category, price) VALUES ('전자', 10000);

-- 가격에 글자를 넣어 보기 (타입 위반 → 실패해야 정상)
INSERT INTO products (name, category, price) VALUES ('테스트', '전자', '비쌈');
