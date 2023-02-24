#!/bin/bash

# Set default cluster name and namespace name
DEFAULT_CLUSTER_NAME="airbyte-cluster"
DEFAULT_NAMESPACE="airbyte"

# Parse command line arguments
if [ $# -ge 1 ]; then
  CLUSTER_NAME=$1
else
  CLUSTER_NAME=$DEFAULT_CLUSTER_NAME
fi

if [ $# -ge 2 ]; then
  NAMESPACE_NAME=$2
else
  NAMESPACE_NAME=$DEFAULT_NAMESPACE
fi

# Check if kind cluster already exists
if kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  echo "$CLUSTER_NAME cluster already exists, skipping creation."
else
  # Create kind cluster
  kind create cluster --name $CLUSTER_NAME
fi

# Set current context to use new cluster
kubectl config use-context kind-$CLUSTER_NAME
# Get current context name
CONTEXT_NAME=$(kubectl config current-context)
echo "Current context is set to: $CONTEXT_NAME"

# Verify that namespace was created
NAMESPACE_EXISTS=$(kubectl get namespace | grep -c "$NAMESPACE_NAME")
if [ $NAMESPACE_EXISTS -eq 1 ]; then
  echo "Namespace '$NAMESPACE_NAME' already exists."
else
  kubectl create namespace "$NAMESPACE_NAME"
  echo "Namespace '$NAMESPACE_NAME' was created successfully."
fi
