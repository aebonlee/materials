-- [Trino CLI]
INSERT INTO iceberg.lakehouse.orders VALUES
  (8, 'jung', 27000, DATE '2026-08-04', 'app');

SELECT count(*) FROM iceberg.lakehouse.orders;
