# daily_report.sh의 백업 줄 앞에 넣습니다
echo "" >> "$out"
top_user=$(grep "user=" "$log" | cut -d ' ' -f 3 | cut -d = -f 2 \
           | sort | uniq -c | sort -k1,1rn -k2,2 | head -n 1)
echo "[가장 많이 나온 사용자] $top_user" >> "$out"

# 확인 — [가장 많이 나온 사용자]    2 kim
./daily_report.sh && cat report_*.txt
