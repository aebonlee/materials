./check_file.sh access.log
#   access.log 파일이 존재합니다.
echo $?
#   0

./check_file.sh no-such-file.txt
#   no-such-file.txt 파일이 없습니다.
echo $?
#   1
