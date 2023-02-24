### Script for Installing and Deleting Helm Charts



This script is used to install and delete Helm charts using the `helm` CLI.

### Prerequisites

- `bash`
- `helm`
- `Kind` and `Docker` (for local K8s development)


### Usage

To use this script, run the command ./script.sh with the following arguments:

### Installing a chart

```shell
./airbyte_k8s.sh -i <chart-name> [chart-version] [namespace]
```

- `-i`: Indicates that you want to install a chart.
- `<chart-name>`: The name of the chart to be installed. If not provided, the default chart name (airbyte) will be used.
- `[chart-version]`: The version of the chart to be installed. If not provided, the default chart version (0.43.29) will be used.
- `[namespace]`: The namespace in which to install the chart. If not provided, the default namespace (airbyte) will be used.


### Deleting a chart

```shell
./airbyte_k8s.sh -d <chart-name> [namespace]
```

- `-d`: Indicates that you want to delete a chart.
- `<chart-name>`: The name of the chart to be deleted.
- `[namespace]`: The namespace from which to delete the chart. If not provided, the script will prompt for a namespace.

### Examples

To install a chart named my-airbyte-worker-chart in the default namespace, run:
```shell
./airbyte_k8s.sh -i my-airbyte-worker-chart
```
To install a chart named airbyte with version 1.0.0 in the my-namespace namespace, run:
```shell
./airbyte_k8s.sh -i airbyte 1.0.0 my-namespace
```
To delete a chart named my-chart from the default namespace, run:
```shell
./airbyte_k8s.sh -d my-chart
```
To delete a chart named my-chart from the my-namespace namespace, run:
```shell
./airbyte_k8s.sh -d my-chart my-namespace
```

## Miscellaneous 

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