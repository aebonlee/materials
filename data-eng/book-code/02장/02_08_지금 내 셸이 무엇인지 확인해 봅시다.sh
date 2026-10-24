# 지금 쓰고 있는 셸
echo $SHELL

# 이 컴퓨터에 설치된 셸 목록
cat /etc/shells

# bash 버전 (WSL2·리눅스 우분투는 보통 5.x, macOS의 bash는 3.2로 오래된 판입니다)
bash --version | head -n 1
