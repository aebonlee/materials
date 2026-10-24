docker run -d --name de-mongo \
  -p 27017:27017 \
  -v de-mongo-data:/data/db \
  mongo:7.0

docker ps

# 접속할 준비가 됐는지 — 1이 나오면 준비 완료
docker exec de-mongo mongosh --quiet --eval "db.runCommand({ ping: 1 }).ok"
