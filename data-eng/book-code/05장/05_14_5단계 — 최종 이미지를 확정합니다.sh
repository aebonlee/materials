# 실험용 이미지 정리
docker rmi data-app:bad data-app:bad2 data-app:good2 data-app:fat data-app:multi

# 최종 판(0.3)에 이름표를 하나 더 붙여 봅니다 — 6장의 Compose는 이 이미지가 아니라 app 폴더를 다시 빌드합니다
docker tag data-app:0.3 data-app:latest
docker images data-app

# 마지막으로 한 번 실행해 확인
docker run --rm data-app:latest
