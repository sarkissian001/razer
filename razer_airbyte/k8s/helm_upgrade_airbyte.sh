#!/bin/bash

NAMESPACE=${1:-dev-local}
RELEASE=${2:-airbyte}
CHART=${3:-airbyte/airbyte}
VERSION=${4:-"0.43.33"}

helm upgrade $RELEASE $CHART --version $VERSION --install --force --values ./helm/values.yaml -n $NAMESPACE
