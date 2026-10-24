# 순서만 미리 봅니다 — 줄 앞의 # 때문에 붙여 넣어도 실행되지 않습니다
# 1) Docker Desktop(리눅스는 Docker 엔진)을 켠다
# docker version --format '{{.Server.Version}}'
# 2) MinIO 이미지 두 개를 받아 둔다 (216MB · 76.5MB)
# docker pull pgsty/minio
# docker pull pgsty/mc
# 3) 17장 실습 1단계에서 ~/lakehouse 폴더를 만든다
