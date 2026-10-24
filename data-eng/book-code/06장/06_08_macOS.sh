lsof -nP -iTCP -sTCP:LISTEN | grep -E ':(5432|8080|8081) '
