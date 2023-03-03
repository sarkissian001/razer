#!/bin/bash

# Check that required environment variables are set
if [[ -z $DOCKER_USERNAME ]]; then
    echo "Error: DOCKER_USERNAME environment variable is not set."
    exit 1
fi

if [[ -z $DOCKER_PASSWORD ]]; then
    echo "Error: DOCKER_PASSWORD environment variable is not set."
    exit 1
fi

if [[ -z $DOCKER_EMAIL ]]; then
    echo "Error: DOCKER_EMAIL environment variable is not set."
    exit 1
fi

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Check that required arguments are set
if [[ -z $NAMESPACE ]]; then
    echo "Usage: $0 -n <namespace>"
    exit 1
fi

# Create secret using environment variables
kubectl create secret docker-registry regcred \
    --docker-server=https://index.docker.io/v1/ \
    --docker-username=$DOCKER_USERNAME \
    --docker-password=$DOCKER_PASSWORD \
    --docker-email=$DOCKER_EMAIL \
    --namespace=$NAMESPACE
