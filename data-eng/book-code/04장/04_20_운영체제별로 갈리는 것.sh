# apt(공식 저장소 · docker.io)로 깔았을 때
sudo usermod -aG docker $USER
newgrp docker                 # 지금 터미널에만 적용. 완전히 적용하려면 로그아웃 후 다시 로그인
docker ps

# snap으로 깔았을 때는 그룹을 먼저 만들고 서비스를 다시 켭니다
sudo addgroup --system docker
sudo adduser $USER docker
newgrp docker
sudo snap disable docker && sudo snap enable docker
docker ps
