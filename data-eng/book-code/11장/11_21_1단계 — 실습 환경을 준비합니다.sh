cd ~/data-eng/week2
source .venv/bin/activate         # 9장에서 만든 가상환경 — Windows(WSL2)·macOS·리눅스 같습니다

# 시작 전 점검 5단계에서 했으면 건너뜁니다
pip install requests beautifulsoup4 pymysql
python3 -c "import requests, bs4, pymysql; print('ok')"

# MySQL 컨테이너도 켜 둡니다 (시작 전 점검 2단계에서 켰으면 그대로)
docker start de-mysql
