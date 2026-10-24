# uv를 쓰는 분은 — 같은 폴더에서 (이 책의 기준은 위의 pip입니다)
uv venv .venv
source .venv/bin/activate
uv pip install requests beautifulsoup4 pymysql
python3 -c "import requests, bs4, pymysql; print('ok')"
