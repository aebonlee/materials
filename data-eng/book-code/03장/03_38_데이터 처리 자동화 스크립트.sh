cat > backup.sh << 'EOF'
#!/bin/bash
src="$1"

if [ ! -e "$src" ]; then
  echo "백업할 대상이 없습니다: $src"
  exit 1
fi

dest="backup_$(date +%Y%m%d)"
mkdir -p "$dest" || { echo "백업 폴더를 만들지 못했습니다: $dest"; exit 1; }
cp -r "$src" "$dest"/ || { echo "복사에 실패했습니다: $src -> $dest"; exit 1; }
echo "$src -> $dest 백업 완료"
EOF

chmod +x backup.sh
./backup.sh logs
ls
