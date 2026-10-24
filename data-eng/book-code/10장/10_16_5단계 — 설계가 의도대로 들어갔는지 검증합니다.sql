SELECT table_name, constraint_name, referenced_table_name
FROM information_schema.key_column_usage
WHERE table_schema = 'shop'
  AND referenced_table_name IS NOT NULL;

-- 복합 PK가 제대로 잡혔는지
SELECT index_name, seq_in_index, column_name
FROM information_schema.statistics
WHERE table_schema = 'shop'
  AND table_name = 'order_items'
  AND index_name = 'PRIMARY'
ORDER BY seq_in_index;
