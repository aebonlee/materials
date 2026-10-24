systemctl --user daemon-reload        # Quadlet 파일 → 서비스 생성
systemctl --user start web.service    # 파일 이름이 서비스 이름
systemctl --user status web.service
curl http://localhost:8080
