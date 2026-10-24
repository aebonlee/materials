# 화면에 이렇게 나옵니다
./count_errors.sh access.log
#   전체 라인: 8
#   에러 라인: 3

# 없는 파일을 주면 — 안내하고 실패(1)로 끝납니다
./count_errors.sh no-such.log
#   로그 파일을 찾을 수 없습니다: no-such.log
echo $?
#   1
