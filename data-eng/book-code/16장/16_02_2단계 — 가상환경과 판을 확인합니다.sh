source .venv/bin/activate        # Windows(WSL2)·macOS·리눅스 같습니다
python3 -c "import sys, pandas, pyarrow, duckdb; print(pandas.__version__, pyarrow.__version__, duckdb.__version__, sys.prefix)"
