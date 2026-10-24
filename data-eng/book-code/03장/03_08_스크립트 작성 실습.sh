cd ~/data-eng/week1

cat > greet.sh << 'EOF'
#!/bin/bash
name="$1"
echo "안녕하세요, $name 님!"
EOF

chmod +x greet.sh
./greet.sh 데이터엔지니어
