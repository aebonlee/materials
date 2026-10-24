# 이미지 크기를 한 번에 뽑기
docker images data-app --format "{{.Tag}}\t{{.Size}}"
