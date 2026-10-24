# 일부러 없는 주소로 시험 — 3번 재시도 후 멈춰야 합니다
python3 -c "
import crawler_pipeline as c
try:
    c.fetch('https://quotes.toscrape.com/no-such-page-xyz')
except Exception as e:
    print('예상대로 실패:', type(e).__name__)
"
