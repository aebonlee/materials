cat > greet.sh << 'EOF'
#!/bin/bash

# 인자 개수를 확인 — 없으면 사용법을 안내하고 실패로 종료
if [ $# -lt 1 ]; then
  echo "사용법: $0 이름"
  exit 1
fi

name="$1"
echo "안녕하세요, $name 님!"
EOF

./greet.sh
echo $?
./greet.sh 홍길동
echo $?
