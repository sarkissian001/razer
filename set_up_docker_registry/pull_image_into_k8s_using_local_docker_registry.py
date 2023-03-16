import subprocess
import os

import asyncio
from core.src.razer.airbyte_base.airbyte_base import AirByteBase
from core.src.razer.Enums.airbyte_connector_types import ConnectionType

os.chdir("../../../razer_airbyte/custom_connectors/sources/source-pokeapi")


def docker_build_tag_push():
    # Build the Docker image
    subprocess.run(["docker", "build", "-t", f"{IMAGE_NAME}:{TAG}", "."])
    # Add a tag to the Docker image
    subprocess.run(
        [
            "docker",
            "tag",
            "source-pokeapi:latest",
            f"{YOUR_REPOSITORY_NAME}/{IMAGE_NAME}:{TAG}",
        ]
    )
    subprocess.run(["docker", "push", f"{YOUR_REPOSITORY_NAME}/{IMAGE_NAME}:{TAG}"])

    # Build the Docker image
    # Log in to the registry
    subprocess.run(
        [
            "docker",
            "login",
            "-u",
            USERNAME,
            "-p",
            PASSWORD,
            f"https://{YOUR_REPOSITORY_NAME}",
        ]
    )

    # Push the Docker image
    subprocess.run(["docker", "push", f"{YOUR_REPOSITORY_NAME}/{IMAGE_NAME}:{TAG}"])
def sync() -> None:
    print("kkkkk")
    ws_id = asyncio.run(obj.get_workspaces())["workspaces"][0]["workspaceId"]

    print(f"using ws id {ws_id}")

    res = asyncio.run(
        obj.sync_custom_connector(
            workspace_id=ws_id,
            image_tag=TAG,
            repository_url=f"{INTERNAL_HOST}/{IMAGE_NAME}",
            connection_name=CUSTOM_CONNECTOR_NAME,
            connector_type=ConnectionType.SOURCE,
        )
    )

    print(res)


if __name__ == "__main__":
    obj = AirByteBase()

    # Set your Docker login credentials
    USERNAME = "airbyte"
    PASSWORD = "airbyte1234"
    YOUR_REPOSITORY_NAME = "localhost:5005"
    INTERNAL_HOST = "https://dockerhost:5005/source-pokeapi"

    TAG = "latest"
    IMAGE_NAME = "source-pokeapi"
    CUSTOM_CONNECTOR_NAME = "example-pokeapi-source"

    # docker_build_tag_push()
    sync()
