
.PHONY: create-kind-cluster
create-kind-cluster:
	chmod +x kind_create_cluster_and_namespace.sh
	@./kind_create_cluster_and_namespace.sh


.PHONY: create-secret
create-k8s-docker-registry-secret:
	chmod +x create_docker_registry_k8s_secret.sh
	@./create_docker_registry_k8s_secret.sh -n dev-local
