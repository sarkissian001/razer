# Deploying Airbyte To K8s with Helm

### Description


Step-by-step guidance on how to deploy Airbyte into Kubernetes using Helm package manager


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
