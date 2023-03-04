#!/bin/bash

DEPLOYMENT=${1:-airbyte}
NAMESPACE=${1:-dev-local}

kubectl get deployments -n $NAMESPACE | grep $DEPLOYMENT | awk '{print $1}' | xargs kubectl rollout restart deployment -n  $NAMESPACE
