import subprocess
import os

import asyncio


from core.src.razer.airbyte_base.airbyte_base import AirByteBase
from core.src.razer.Enums.airbyte_connector_types import ConnectionType


obj = AirByteBase()


os.chdir("./source-pokeapi")


YOUR_REPOSITORY_NAME = "<>"

# Build the Docker image
subprocess.run(["docker", "build", "-t", "source-pokeapi:latest", "."])
# Add a tag to the Docker image
subprocess.run(
    [
        "docker",
        "tag",
        "source-pokeapi:latest",
        f"{YOUR_REPOSITORY_NAME}/source-pokeapi:latest",
    ]
)
subprocess.run(["docker", "push", f"{YOUR_REPOSITORY_NAME}/source-pokeapi:latest"])

ws_id = asyncio.run(
    obj.get_or_create_workspace(workspace_name="Test Workspace", email="test@fake.org")
)
print(f"using ws id {ws_id}")

res = asyncio.run(
    obj.sync_custom_connector(
        workspace_id=ws_id,
        image_tag="latest",
        repository_url=f"{YOUR_REPOSITORY_NAME}/source-pokeapi",
        connection_name="example-pokeapi-source",
        connector_type=ConnectionType.SOURCE,
    )
)

print(res)
