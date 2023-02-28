
## Instructions 

Instruction of how to obtain prereq for Mac OS users
```shell
brew install helm
brew install kind
```

For local development, to create cluster, namespace and set kubectl context you can use the following convinence function
```shell
./kind_create_cluster_and_namespace.sh <cluster_name> [namespace] 
```
- `<cluster-name>`: The name of the K8s cluster If not provided, the default name will be (airbyte-cluster)
- `[namespace]`: The namespace in which to install the airbyte charts. If not provided, the default namespace (airbyte) will be used.

## Useful Tools 

Use open source **[OpenLense](https://github.com/MuhammedKalkan/OpenLens)** to monitor your local K8 clusters