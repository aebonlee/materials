# 우분투(WSL2) 터미널에서 — 리눅스 탭의 1~5단계와 같습니다
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker

# WSL2에서 데몬 켜기 — systemd가 켜져 있으면 한 번만
sudo systemctl enable --now docker
# systemd가 꺼진 WSL2라면 위 대신, 우분투를 새로 열 때마다
#   sudo service docker start
docker version
docker run --rm hello-world
