# 2단계(일부러 실패) — transform.py 끝에 이어 붙입니다
# strip을 빼면 몇 건이 새는지 확인해 봅니다
without_strip = df[df['category'] == '식품']
with_strip = df[df['category'].str.strip() == '식품']
print('strip 없이:', len(without_strip))
print('strip 하고:', len(with_strip))
print('놓친 건수 :', len(with_strip) - len(without_strip))
