cd ~/data-eng/week1

cat > report_tool.sh << 'EOF'
#!/bin/bash

# 사용법 안내 — 여러 곳에서 부르게 되므로 함수로 둡니다
usage() {
  echo "사용법: $0 [summary|detail|help] [폴더]"
}

# 파일 하나의 ERROR 건수를 세어 돌려줍니다
count_errors() {
  local file="$1"          # 함수에 넘긴 첫 값
  grep -c ERROR "$file" || true
}

usage
echo "app1의 ERROR: $(count_errors logs/app1.log)건"
EOF

chmod +x report_tool.sh
./report_tool.sh
#   사용법: ./report_tool.sh [summary|detail|help] [폴더]
#   app1의 ERROR: 1건
