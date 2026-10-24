# docker pull은 한 번에 이미지 하나만 받으므로 for로 돌립니다
for i in dpage/pgadmin4:9.18 postgres:16 nginx:1.27 curlimages/curl:8.10.1; do docker pull $i; done

# 받은 것 확인
docker images --format '{{.Repository}}:{{.Tag}}' | grep -E 'pgadmin4|postgres|nginx|curl'
