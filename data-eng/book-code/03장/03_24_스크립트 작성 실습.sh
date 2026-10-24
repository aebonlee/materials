# ERROR가 하나도 없는 로그를 하나 더 만들어 확인합니다
printf "INFO x\nINFO y\n" > logs/app3.log
./report_tool.sh
#   ERROR 합계: 2건        ← || true가 있으면 정상
#   (|| true를 지우면 여기서 아무 말 없이 멈춥니다)
