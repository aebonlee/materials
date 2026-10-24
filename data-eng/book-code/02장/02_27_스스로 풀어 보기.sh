grep 'user=' access.log | cut -d ' ' -f 3 | cut -d = -f 2 | sort -u
