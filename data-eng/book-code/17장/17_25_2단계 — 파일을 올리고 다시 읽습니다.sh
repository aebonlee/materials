echo "hello object storage" > data/hello.txt
docker compose exec mc mc cp /data/hello.txt local/raw/hello.txt
