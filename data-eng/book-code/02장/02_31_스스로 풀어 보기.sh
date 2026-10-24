echo 'echo hi' > hello.sh
ls -l hello.sh        # 권한에 x가 없다

chmod +x hello.sh
ls -l hello.sh        # x가 생겼다
./hello.sh
