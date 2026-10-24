-- 파일 경로를 FROM에 그대로 적습니다
SELECT count(*) FROM 'events.csv';
SELECT count(*) FROM 'events.parquet';

-- 여러 파일을 한꺼번에 (와일드카드)
SELECT count(*) FROM 'data/*.parquet';

-- 옵션을 주려면 함수 형태로
SELECT * FROM read_csv('events.csv', sample_size = -1);

-- 결과를 파일로 내보내기 (압축을 적지 않으면 snappy)
COPY (SELECT * FROM 'events.csv') TO 'out.parquet' (FORMAT parquet);
