-- 방법 A: 스냅샷 id로 — 아래 숫자를 3단계에서 복사한 첫 snapshot_id로 바꿉니다
SELECT * FROM demo.lakehouse.orders VERSION AS OF 1234567890123456789 ORDER BY order_id;

-- 방법 B: 시각으로 — 따옴표 안을 첫 스냅샷의 committed_at 값으로 바꿉니다 (UPDATE 이전 시각)
SELECT * FROM demo.lakehouse.orders TIMESTAMP AS OF '2026-10-19 11:00:00.000' ORDER BY order_id;

-- 현재 상태와 비교
SELECT * FROM demo.lakehouse.orders ORDER BY order_id;
