# 정답 예시 — 총 개수와 용량 (s3_demo.py 끝에 이어 붙입니다)
paginator = s3.get_paginator('list_objects_v2')
total, size = 0, 0
for page in paginator.paginate(Bucket='raw'):
    for obj in page.get('Contents', []):
        total += 1
        size += obj['Size']
print(f'{total}개 · {size:,} bytes')
