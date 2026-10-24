which docker                  # /usr/bin/docker → apt로 깔았다 · /snap/bin/docker → snap으로 깔았다
dpkg -l docker-ce docker.io 2>/dev/null | grep ^ii   # 어느 패키지인지
snap list docker 2>/dev/null                          # snap이면 여기 나온다
