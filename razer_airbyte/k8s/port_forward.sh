#!/bin/bash


kubectl --namespace dev-local port-forward service/airbyte-airbyte-webapp-svc 8000:80
