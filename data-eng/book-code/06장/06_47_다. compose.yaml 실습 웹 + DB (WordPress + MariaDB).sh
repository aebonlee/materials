podman pod ps                                   # compose가 만든 pod 이름 확인 (podman-compose는 기본으로 pod_폴더이름)
podman kube generate pod_wp-lab > wp-kube.yaml   # pod 안의 컨테이너는 pod 이름으로 뽑습니다
podman kube play wp-kube.yaml                   # 같은 구성을 K8s YAML로 재실행
