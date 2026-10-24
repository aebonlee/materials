cat > report_tool.sh << 'EOF'
#!/bin/bash

usage() {
  echo "사용법: $0 [summary|detail|help] [폴더]"
}

count_errors() {
  local file="$1"
  grep -c ERROR "$file" || true
}

mode="${1:-summary}"      # 안 주면 summary
dir="${2:-logs}"          # 안 주면 logs

case "$mode" in
  summary)
    total=0
    for f in "$dir"/*.log; do
      total=$(( total + $(count_errors "$f") ))
    done
    echo "ERROR 합계: ${total}건"
    ;;
  help)
    usage
    ;;
  *)
    echo "모르는 모드: $mode"
    usage
    exit 2
    ;;
esac
EOF

./report_tool.sh
#   ERROR 합계: 2건
./report_tool.sh help
#   사용법: ./report_tool.sh [summary|detail|help] [폴더]
./report_tool.sh zzz
#   모르는 모드: zzz
#   사용법: ./report_tool.sh [summary|detail|help] [폴더]
echo $?
#   2
