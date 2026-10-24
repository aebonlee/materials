echo '#!/bin/bash' > hello.sh
echo 'echo Hello, Data Engineering!' >> hello.sh

# 내용 확인
cat hello.sh

# 실행 권한 부여 전 — 여기서 한 번 실패해 보는 것이 목적입니다
ls -l hello.sh
./hello.sh

# 권한을 주고 다시 실행
chmod +x hello.sh
ls -l hello.sh
./hello.sh
