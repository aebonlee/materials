# 연습용 로그 몇 개 만들기
mkdir -p logs
echo "ERROR a" > logs/app1.log
printf "INFO b\nERROR c\n" > logs/app2.log

cat > scan_logs.sh << 'EOF'
#!/bin/bash
dir="${1:-logs}"        # 인자가 없으면 logs를 기본값으로

for f in "$dir"/*.log; do
  lines=$(wc -l < "$f" | tr -d " ")
  errors=$(grep -c ERROR "$f")
  echo "$f : 전체 ${lines}줄 · ERROR ${errors}건"
done
EOF

chmod +x scan_logs.sh
./scan_logs.sh
