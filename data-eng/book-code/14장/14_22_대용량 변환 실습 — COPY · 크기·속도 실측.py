# 2단계 — speed.py 끝에 이어 붙입니다
csv = os.path.getsize('events.csv')
pq = os.path.getsize('events.parquet')
print(f'CSV    : {csv/1024/1024:,.1f} MB')
print(f'Parquet: {pq/1024/1024:,.1f} MB')
print(f'비율   : {pq/csv:.1%}  ({csv/pq:.1f}배 작아짐)')
