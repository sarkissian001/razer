#!/bin/bash

# Set default values
default_chart_name="airbyte"
default_chart_version="0.43.29"
default_namespace="airbyte"

# Define helper function
usage() {
  echo "Usage: $0 -I <chart-name> [chart-version] [namespace]"
  echo "  Installs the specified Helm chart with the given name and version."
  echo "  If a namespace is specified, the chart is installed to that namespace."
  echo "  If the chart already exists, it is skipped."
  echo "  If you do not provide chart_name | chart_version, the following default values will be applied: "
  echo "     chart_name: $default_chart_name | chart_version: $default_chart_version"
  echo "Usage: $0 -d <chart-name> [namespace]"
  echo "  Deletes the specified Helm chart with the given name."
  echo "  If a namespace is specified, the chart is deleted from that namespace."
}


# Define install function
install_chart() {
  if helm ls --all-namespaces | grep -q "^$chart_name\s"; then
    echo "Chart $chart_name already exists, skipping installation."
  else
    if [ -n "$namespace" ]; then
      helm install $chart_name airbyte/$chart_name --version $chart_version -f ./helm/values.yaml --namespace $namespace
    else
      helm install $chart_name airbyte/$chart_name --version $chart_version -f ./helm/values.yaml
    fi
  fi
}


# Define delete function
delete_chart() {
  echo "deleting chart [$chart_name] from namespace [$namespace]"
  helm uninstall $chart_name --namespace $namespace

}


# Handle arguments
if [ "$1" = "-i" ]; then
  # Install chart

  chart_name=${2:-$default_chart_name}
  chart_version=${3:-$default_chart_version}
  namespace=${4:-$default_namespace}

  echo "Using Chart Name : $chart_name"
  echo "Using Chart Version : $chart_version"
  echo "Using Namespace : $namespace"

  if ! helm repo list | awk '{print $1}' | grep -q "^airbyte$"; then
    # Add repository
    echo "Adding airbyte charts to helm repo (charts: https://airbytehq.github.io/helm-charts)"
    helm repo add airbyte https://airbytehq.github.io/helm-charts
    helm repo update
  else
    echo "Airbyte repository found."
  fi

  install_chart
  exit 0
elif [ "$1" = "-d" ]; then
  # Delete chart
  if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    usage
    exit 1
  fi
  chart_name=$2
  namespace=$3

  delete_chart
  exit 0
else
  usage
  exit 1
fi
