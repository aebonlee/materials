sudo systemctl enable --now docker
docker version --format '{{.Server.Version}}'
