cd ~/data-eng/week3
ls -lh
source .venv/bin/activate        # Windows(WSL2)·macOS·리눅스 같습니다
python3 -c "import pandas as pd; d = pd.read_parquet('orders_step1.parquet'); print(d.shape, d['order_date'].dtype)"
