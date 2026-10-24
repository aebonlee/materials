# 셔뱅(1번째 줄) 다음에 set 줄을 끼워 넣습니다
# 첫 줄 + 새 줄 + 나머지 를 이어 붙여 새 파일로 만드는 것입니다
{ head -1 report_tool.sh; echo 'set -euo pipefail'; tail -n +2 report_tool.sh; } > tmp
mv tmp report_tool.sh
chmod +x report_tool.sh

# 제대로 들어갔는지 앞 세 줄만 봅니다
head -3 report_tool.sh
#   #!/bin/bash
#   set -euo pipefail
#   (빈 줄)
