#!/bin/bash

function delete_registry_if_exists {
    local container_name=$1
    # Check if a container with the name "my-registry" already exists
    if docker container inspect $container_name &>/dev/null; then
        # If the container exists, stop and remove it
        docker stop $container_name
        docker rm $container_name
        echo "deleted container $container_name."
    else
        # If the container does not exist, do nothing
        echo "container $container_name does not exist."
    fi
}

function create_registry_with_auth {
    local username=$1
    local password=$2
    local container_name=$3
    local port=$4

    # Create the auth directory
    mkdir -p auth

    # Create a Docker volume to store the auth data
    docker volume create ${container_name}-auth

    # Create the certs directory
    mkdir -p certs

    # Generate a self-signed SSL certificate
    openssl req -newkey rsa:4096 -nodes -sha256 \
    -keyout certs/domain.key \
    -x509 -days 365 \
    -out certs/domain.crt \
    -subj "/CN=myregistry.com"

    # Create the config file
    cat << EOF > ./confs/config.yml
      version: 0.1
      storage:
        filesystem:
          rootdirectory: /var/lib/registry
      auth:
        htpasswd:
          realm: basic-realm
          path: /auth/htpasswd
      http:
        addr: :5000
        tls:
          certificate: /certs/domain.crt
          key: /certs/domain.key
EOF

    # Start the Docker registry container, mounting the auth and config volumes, exposing port 5000 and using the SSL certificate
    docker run -d -p $port:5000 \
    --name $container_name \
    -v ${container_name}-auth:/auth \
    -v $(pwd)/certs:/certs \
    -v $(pwd)/confs/config.yml:/etc/docker/registry/config.yml \
    registry:2

    # Create a new user in the auth directory of the volume
    htpasswd -Bbn $username $password > auth/htpasswd

    # Copy the htpasswd file from the host to the auth directory in the volume
    if [ -e auth/htpasswd ]; then
        docker cp auth/htpasswd ${container_name}:/auth/htpasswd
        docker exec $container_name chown root:root /auth/htpasswd
        docker exec $container_name chmod 644 /auth/htpasswd
    else
        echo "htpasswd file not found"
    fi

    # Restart the registry container to apply the changes
    docker restart $container_name
}

function create_kubernetes_secret {
    local registry_url=$1
    local username=$2
    local password=$3
    local secret_name=$4
    local namespace=$5
    local ssl_cert_file=$6
    local ssl_key_file=$7

    # Delete the Kubernetes secret using subprocess
    if kubectl delete secret $secret_name --namespace=$namespace &>/dev/null; then
        echo "Deleted secret $secret_name in namespace $namespace"
    else
        echo "Secret $secret_name doesn't exist in namespace $namespace. Will create it"
    fi

    # Create a .dockerconfigjson file with registry authentication details
    local auth=$(echo -n "$username:$password" | base64)

    cat <<EOF > dockerconfigjson.txt
      {
          "auths": {
              "$registry_url": {
                  "username": "$username",
                  "password": "$password",
                  "auth": "$auth"
              }
          }
      }
EOF


    # Create the Kubernetes secret using kubectl
    kubectl create secret docker-registry $secret_name \
    --docker-server=$registry_url \
    --docker-username=$username \
    --docker-password=$password \
    --namespace=$namespace \
    --from-file=certs=$ssl_cert_file \
    --from-file=key=$ssl_key_file \
    --from-file=.dockerconfigjson=./dockerconfigjson.txt

    # Clean up the .dockerconfigjson file
    rm dockerconfigjson.txt
}

function apply_dockerhost_service() {
    local namespace=$1
    echo "applying dockerhost-service.yaml to namespace $namespace; which will make localhost:5005 running in host available in k8s"

    kubectl apply -f ./confs/dockerhost-service.yaml --namespace="$namespace"
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    REGISTRY_NAME="my-registry"
    PORT="5005"
    PASSWORD="airbyte1234"
    USERNAME="airbyte"
    NAMESPACE="dev-local"
    REGISTRY_URL="https://dockerhost:5005"
    SECRET_NAME="regcred"
    SSL_CERT_FILE="./certs/domain.crt"
    SSL_KEY_FILE="./certs/domain.key"

    delete_registry_if_exists $REGISTRY_NAME
    create_registry_with_auth $USERNAME $PASSWORD $REGISTRY_NAME $PORT
    apply_dockerhost_service $NAMESPACE
    create_kubernetes_secret $REGISTRY_URL $USERNAME $PASSWORD $SECRET_NAME $NAMESPACE $SSL_CERT_FILE $SSL_KEY_FILE
fi
