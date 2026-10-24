sudo systemctl enable --now docker
docker version --format '{{.Server.Version}}'
docker info | grep -i "total memory"
