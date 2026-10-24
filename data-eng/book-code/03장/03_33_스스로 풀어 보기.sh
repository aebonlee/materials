#!/bin/bash
name="$1"                 # 등호 양옆 공백 없음
if [ -z "$name" ]; then   # [ 뒤 · ] 앞에 공백
  echo "이름을 주세요"
  exit 1
fi
echo "안녕하세요, $name 님"
