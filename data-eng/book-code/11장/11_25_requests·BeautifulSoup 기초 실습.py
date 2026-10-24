# 아래 두 개는 같은 일을 합니다
tags = [t.get_text(strip=True) for t in q.select('a.tag')]

tags = []
for t in q.select('a.tag'):
    tags.append(t.get_text(strip=True))
