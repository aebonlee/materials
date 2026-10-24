MERGE INTO 대상테이블 AS t
USING 원천 AS s
ON t.키 = s.키                       -- 무엇이 "같은 것"인가
WHEN MATCHED THEN UPDATE SET *        -- 있으면 덮어쓴다
WHEN NOT MATCHED THEN INSERT *;       -- 없으면 넣는다

-- 조건을 더 붙인 완성형 — 조건 있는 MATCHED 절을 먼저, 조건 없는 절은 맨 끝에 둡니다
MERGE INTO 대상테이블 AS t
USING 원천 AS s
ON t.키 = s.키
WHEN MATCHED AND s.amount < 0 THEN DELETE
WHEN MATCHED AND s.updated_at > t.updated_at THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
