
# Add the following to your bash/zshrc profile to enable make autocomplete
#
#  			zstyle ':completion:*:*:make:*' tag-order 'targets'
#  			autoload -U compinit && compinit



.PHONY: create-kind-cluster
create-kind-cluster:
	chmod +x kind_create_cluster_and_namespace.sh
	@./kind_create_cluster_and_namespace.sh


.PHONY: create-k8s-docker-registry-secret
create-k8s-docker-registry-secret:
	chmod +x create_docker_registry_k8s_secret.sh
	@./create_docker_registry_k8s_secret.sh -n dev-local


.PHONY: display-docker-registry-secret
display-docker-registry-secret:
	kubectl get secret regcred -n dev-local --output="jsonpath={.data.\.dockerconfigjson}" | base64 --decode


.PHONY: delete-docker-registry-secret
delete-docker-registry-secret:
	kubectl delete secret regcred -n dev-local


# ================================================================================================
# ======					<	Airbyte Helm Deployments  >						==================
#=================================================================================================

# Deploy Airbyte to K8s (uses default chart version and namespace specified in airbyte_k8s script)
# You can pass your own arguments as per instruction in the script
deploy-airbyte-to-k8s:
	cd razer_airbyte/k8s && chmod +x ./airbyte_k8s.sh && ./airbyte_k8s.sh -i


# Forward Airbyte webapp port
airbyte-port-forward:
	cd razer_airbyte/k8s && chmod +x ./port_forward.sh && ./port_forward.sh


# Remove Airbyte K8s deployments (uses default release name and namespace specified in airbyte_k8s script)
# You can pass your own arguments as per instruction in the script
delete-airbyte-deployment:
	cd razer_airbyte/k8s && chmod +x ./airbyte_k8s.sh && ./airbyte_k8s.sh -d airbyte dev-local


# Restart Airbyte deployments | recreate pods
resart-airbyte-deployment:
	cd razer_airbyte/k8s && chmod +x ./restart_airbyte_deployments.sh && ./restart_airbyte_deployments.sh

