# ① if의 조건 자리에서는 안 멈춥니다 (logs/app3.log에는 ERROR가 없습니다)
bash -c 'set -e; if grep -c ERROR logs/app3.log >/dev/null; then echo "있음"; else echo "없음 — 안 멈췄다"; fi'
#   없음 — 안 멈췄다

# ② || 앞에서도 안 멈춥니다
bash -c 'set -e; grep -c ERROR logs/app3.log >/dev/null || echo "없음 — 안 멈췄다"; echo "계속 진행"'
#   없음 — 안 멈췄다
#   계속 진행

# ③ set -u 여도 기본값이 있으면 괜찮습니다 (인자를 안 준 상태)
bash -c 'set -u; dir="${1:-logs}"; echo "폴더: $dir"' --
#   폴더: logs

# ④ pipefail이 없으면 실패가 성공으로 보입니다
bash -c 'cat no-such.log 2>/dev/null | wc -l; echo "종료코드 $?"'
#   0
#   종료코드 0       ← cat은 실패했는데
bash -c 'set -o pipefail; cat no-such.log 2>/dev/null | wc -l; echo "종료코드 $?"'
#   0
#   종료코드 1
