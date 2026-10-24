# ① set -e — 없을 때와 있을 때
bash -c 'cat no-such.log; echo "여기까지 옵니다"'
#   cat: no-such.log: No such file or directory
#   여기까지 옵니다              ← 오류인데 계속 갔다

bash -c 'set -e; cat no-such.log; echo "여기는 못 옵니다"'
#   cat: no-such.log: No such file or directory
#                                ← 두 번째 줄이 아예 안 나온다

# ② set -u — 변수 이름을 일부러 틀려 봅니다 (name을 nmae로)
bash -c 'user_name="홍길동"; echo "안녕 [$user_nmae] 님"'
#   안녕 [] 님                   ← 빈칸인 채로 그냥 돈다

bash -c 'set -u; user_name="홍길동"; echo "안녕 [$user_nmae] 님"'
#   bash: line 1: user_nmae: unbound variable   (bash 판에 따라 앞부분이 다를 수 있습니다)

# ③ pipefail — 앞이 실패해도 wc는 성공하므로
bash -c 'cat no-such.log | wc -l; echo "종료코드 $?"'
#   cat: no-such.log: No such file or directory
#   0
#   종료코드 0                   ← 실패했는데 성공으로 보인다

bash -c 'set -o pipefail; cat no-such.log | wc -l; echo "종료코드 $?"'
#   cat: no-such.log: No such file or directory
#   0
#   종료코드 1
