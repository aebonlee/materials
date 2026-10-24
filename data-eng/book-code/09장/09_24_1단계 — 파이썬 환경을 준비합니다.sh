# 실습 폴더 (제1부에 만든 구조를 이어 씁니다)
mkdir -p ~/data-eng/week2
cd ~/data-eng/week2

# 가상환경 — 시스템 파이썬을 어지럽히지 않기 위해
python3 -m venv .venv
source .venv/bin/activate        # Windows(WSL2)·macOS·리눅스 모두 같습니다

pip install pymongo
python3 -c "import pymongo; print(pymongo.version)"

# 가상환경의 파이썬이 실제로 쓰이는지 — 끝이 .venv 여야 합니다
python3 -c "import sys; print(sys.prefix)"
