# 아래 두 개는 같은 일을 합니다
with conn.cursor() as cur:
    cur.execute(...)

cur = conn.cursor()
try:
    cur.execute(...)
finally:
    cur.close()          # with가 이 뒷정리를 대신해 줍니다
