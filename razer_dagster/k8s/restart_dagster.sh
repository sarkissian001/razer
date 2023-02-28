#!/bin/bash

NAMESPACE=${1:-dev-local}
RELEASE=${2:-dagster}
CHART=${3:-dagster/dagster}
CHART_VERSION=${4:-1.1.20}

helm upgrade --install $RELEASE $CHART --version $CHART_VERSION -f ./helm/values.yaml -n $NAMESPACE