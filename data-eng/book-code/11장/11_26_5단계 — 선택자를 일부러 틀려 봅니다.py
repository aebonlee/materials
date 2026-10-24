# selector_test.py — 존재하지 않는 선택자를 써 봅니다 (마지막 줄에서 일부러 터집니다)
import requests
from bs4 import BeautifulSoup

res = requests.get('https://quotes.toscrape.com/', timeout=10)
soup = BeautifulSoup(res.text, 'html.parser')

print(soup.select('div.quotes'))          # 없는 클래스 → 빈 리스트 []
print(soup.select_one('span.txt'))        # 없는 클래스 → None
print(soup.select_one('span.txt').get_text())   # ← 여기서 터집니다
