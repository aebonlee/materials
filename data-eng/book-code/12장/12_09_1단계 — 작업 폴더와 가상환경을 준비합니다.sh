# 시작 전 점검 2·3단계에서 만들었으면 켜기만 합니다
cd ~/data-eng/week3
source .venv/bin/activate   # Windows(WSL2)·macOS·리눅스 모두 같습니다
python3 -c "import sys, pandas as pd; print(pd.__version__, sys.prefix)"
