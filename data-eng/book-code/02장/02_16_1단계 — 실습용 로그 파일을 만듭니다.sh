cd ~/data-eng/week1

# EOF까지 통째로 복사해 붙여넣으세요
cat > access.log << 'EOF'
INFO login user=kim
ERROR db timeout
INFO login user=lee
ERROR db timeout
INFO logout user=kim
WARN slow query 1200ms
ERROR db timeout
INFO login user=park
EOF

# 잘 만들어졌는지 확인
cat access.log
wc -l access.log
