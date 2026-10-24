cd ~/data-eng/week1/app

# slim이 아닌 전체 베이스로도 빌드해 비교
sed "s/python:3.12-slim/python:3.12/" Dockerfile > Dockerfile.fat
docker build -t data-app:fat -f Dockerfile.fat .

# 크기 비교
docker images data-app
