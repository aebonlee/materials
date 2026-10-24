# 1. 패키지 목록 갱신 + 설치에 필요한 도구
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# 2. Docker 공식 GPG 서명 키 등록 (패키지 위변조 검증용)
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 3. 공식 저장소를 apt 소스 목록에 추가 — 아키텍처와 우분투 코드명은 $( )가 자동으로 넣습니다
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list

# 4. 엔진·CLI·containerd·Buildx·Compose 플러그인 설치
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 5. 내 계정을 docker 그룹에 넣어 sudo 없이 쓰기 — 완전 적용은 로그아웃 후 다시 로그인
sudo usermod -aG docker $USER
newgrp docker
docker ps                     # 헤더만 나오고 비어 있으면 정상
