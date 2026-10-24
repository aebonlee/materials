wsl -l -v
#   NAME            STATE      VERSION
#   Ubuntu-22.04    Running    2        ← 반드시 2

# 1이면 올립니다 (몇 분 걸립니다)
wsl --set-version Ubuntu-22.04 2
