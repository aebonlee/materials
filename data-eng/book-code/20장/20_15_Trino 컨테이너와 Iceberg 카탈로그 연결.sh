# 카탈로그가 실제로 올라갔는지 · 설정 경고가 없는지
docker compose logs trino | grep -E "Added catalog|has been replaced"
