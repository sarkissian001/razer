#!/bin/bash

NAMESPACE=${1:-dev-local}
RELEASE=${2:-airbyte}
CHART=${3:-airbyte/airbyte}

helm upgrade --install $RELEASE $CHART --recreate-pods -f ./helm/values.yaml -n $NAMESPACE
