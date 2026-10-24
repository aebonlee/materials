# 편집기 열기 (처음이면 어떤 편집기를 쓸지 물어봅니다 — nano를 고르면 쉽습니다)
crontab -e

# 아래 한 줄을 넣고 저장합니다. 경로는 위 pwd로 확인한 값으로 바꾸세요.
#   0 3 * * * /home/사용자명/data-eng/week1/daily_report.sh

# 등록된 목록 확인
crontab -l
