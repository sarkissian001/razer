#!/bin/bash


kubectl --namespace dev-local port-forward $(kubectl get pods --namespace dev-local \
  -l "app.kubernetes.io/name=dagster,app.kubernetes.io/instance=dagster,component=dagit" \
    -o jsonpath="{.items[0].metadata.name}") 8080:80
