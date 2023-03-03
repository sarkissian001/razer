import subprocess

# Define the Docker registry URL where the connector images are stored
DOCKER_REGISTRY_URL = 'http://localhost:5005'

# Define the Airbyte Helm chart release name
AIRBYTE_RELEASE_NAME = 'airbyte'

# Define the Airbyte connector names and Docker image tags
CONNECTOR_IMAGES = {
    'source_yahoo_example': 'latest',
}

# Update the values.yaml file with the connector image URLs
with open('values.yaml', 'r') as f:
    values = f.read()

for name, tag in CONNECTOR_IMAGES.items():
    image_url = f'{DOCKER_REGISTRY_URL}/{name}:{tag}'
    values = values.replace(f'{name}:latest', image_url)

with open('values.yaml', 'w') as f:
    f.write(values)

# # Deploy or upgrade Airbyte using Helm
# upgrade_command = f'helm upgrade {AIRBYTE_RELEASE_NAME} airbyte/airbyte -f values.yaml'
# subprocess.check_call(upgrade_command, shell=True)
