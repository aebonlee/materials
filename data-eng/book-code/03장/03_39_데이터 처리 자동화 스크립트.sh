# 화면에 이렇게 나옵니다 (날짜는 오늘 날짜입니다)
./backup.sh logs
#   logs -> backup_20260922 백업 완료

ls
#   access.log  backup.sh  backup_20260922  count_errors.sh  logs  ...

# 안에 들어갔는지 확인
ls backup_*/logs
#   app1.log  app2.log  app3.log  notes_backup.txt
