docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep -E 'NAMES|8080|trino'
