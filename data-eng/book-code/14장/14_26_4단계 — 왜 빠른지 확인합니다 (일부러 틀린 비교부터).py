# 4단계 — speed.py 끝에 이어 붙입니다
# 먼저 일부러 틀린 비교 — 「전부 읽기」를 count(*)로 잽니다
one_col = bench("SELECT sum(value) FROM 'events.parquet'")
all_cnt = bench("SELECT count(*) FROM (SELECT * FROM 'events.parquet')")
print(f'한 열만            : {one_col:.4f} 초')
print(f'전부 읽기(count(*)): {all_cnt:.4f} 초')

# 다섯 열을 정말로 읽게 합니다 — 열마다 집계를 하나씩
five = "SELECT max(event_id), max(user_id), max(event_type), sum(value), max(ts) FROM "
all_col = bench(five + "'events.parquet'")
print(f'다섯 열 전부       : {all_col:.4f} 초  (한 열의 {all_col/one_col:.1f}배)')

# CSV는 어느 쪽이든 전체를 파싱해야 합니다
csv_one = bench("SELECT sum(value) FROM 'events.csv'")
csv_all = bench(five + "'events.csv'")
print(f'\nCSV 한 열만  : {csv_one:.3f} 초')
print(f'CSV 다섯 열  : {csv_all:.3f} 초')
