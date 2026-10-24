# 지금 떠 있는 Compose 묶음 보기
docker compose ls

# 1단계 연습용(compose-test) 내리기
cd ~/data-eng/week1/compose-test && docker compose down

# 통합 환경 내리기 — -v는 week1_pgdata 볼륨까지 지웁니다(되돌릴 수 없음)
cd ~/data-eng/week1 && docker compose down -v

# 확인
docker compose ls
