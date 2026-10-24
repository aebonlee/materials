# 6단계(읽기 비교) — speed.py 끝에 이어 붙입니다. buy만 읽을 때 — 다른 폴더는 아예 열지 않습니다
parted = bench("SELECT sum(value) FROM 'events_parted/*/*.parquet' WHERE event_type = 'buy'")
single = bench("SELECT sum(value) FROM 'events.parquet' WHERE event_type = 'buy'")
print(f'파티션됨 : {parted:.4f} 초')
print(f'단일 파일: {single:.4f} 초')
