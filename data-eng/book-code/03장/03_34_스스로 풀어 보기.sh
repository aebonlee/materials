#!/bin/bash
set -euo pipefail
dir="${1:-logs}"

for f in "$dir"/*.log; do
  n=$(grep -c ERROR "$f" || true)
  if [ "$n" -ge 1 ]; then
    echo "$f"
  fi
done

# 결과
#   logs/app1.log
#   logs/app2.log
