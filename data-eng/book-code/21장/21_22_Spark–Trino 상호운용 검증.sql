-- [Trino CLI] 두 이름(과 Spark의 demo)이 모두 같은 실체
SELECT count(*) FROM iceberg.lakehouse.orders;
SELECT count(*) FROM iceberg2.lakehouse.orders;
