deactivate 2>/dev/null          # 제2부 가상환경이 켜져 있으면 끈다 (없으면 그냥 지나간다)
mkdir -p ~/data-eng/week3
cd ~/data-eng/week3
python3 -m venv .venv
source .venv/bin/activate        # Windows(WSL2)·macOS·리눅스 같습니다

python3 -c "import sys; print(sys.version.split()[0], sys.prefix)"
