#!/bin/bash

NAMESPACE=${1:-dev-local}
RELEASE=${2:-airbyte}
CHART=${3:-airbyte/airbyte}

helm upgrade $RELEASE $CHART --install --force --values ./helm/values.yaml -n $NAMESPACE
