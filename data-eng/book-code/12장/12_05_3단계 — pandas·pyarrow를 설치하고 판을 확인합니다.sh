pip install pandas pyarrow
python3 -c "import pandas, pyarrow; print('pandas', pandas.__version__, 'pyarrow', pyarrow.__version__)"
pip list | grep -i -E "pandas|pyarrow|numpy"
