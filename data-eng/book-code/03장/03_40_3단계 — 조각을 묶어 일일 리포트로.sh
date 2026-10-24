cat > daily_report.sh << 'EOF'
#!/bin/bash
set -euo pipefail   # 실패하면 중단(-e) · 없는 변수면 중단(-u) · 파이프 중간 실패도 실패(pipefail)

log="${1:-access.log}"
today=$(date +%Y%m%d)
out="report_${today}.txt"

echo "===== $today 일일 리포트 =====" > "$out"
./count_errors.sh "$log" >> "$out"
echo "" >> "$out"
echo "[로그 레벨별 집계]" >> "$out"
cut -d ' ' -f 1 "$log" | sort | uniq -c | sort -k1,1rn -k2,2 >> "$out"

./backup.sh "$log" > /dev/null
echo "" >> "$out"
echo "백업 완료" >> "$out"

echo "리포트 생성: $out"
EOF

chmod +x daily_report.sh
./daily_report.sh
cat report_*.txt
