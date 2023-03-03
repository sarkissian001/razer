from typing import Dict, List, Optional, Union

import aiohttp
import requests

from src.razer.Enums.airbyte_connector_types import ConnectionType
from src.razer.common.logger import Logger


class AirByteBase:
    """
    Defines all Airbyte basic functionalities
    Documentation: https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html#post-/v1/connections/list

    """

    # TODO: we need to configure airbyte in such way that it requires user login details
    # TODO: All headers should include auth token

    def __init__(
        self,
        host: str = "localhost",
        port: str = "8000",
        username: Union[str, None] = None,
        password_env: Union[str, None] = None,
        log_level: Union[str, None] = None,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password_env = password_env

        self.base_url: str = f"http://{self.host}:{self.port}/api/v1"

        self.logger = Logger(__name__, log_level)

    async def get_workspaces(self) -> Dict:
        """
        List all available workspaces
        @return: Dictionary
        """

        ws_url: str = f"{self.base_url}/workspaces/list"

        headers = {"Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.post(ws_url, headers=headers) as response:
                if not response.ok:
                    raise requests.HTTPError(response.status, await response.text())
                return await response.json()

    async def get_workspace_ids(self) -> List[str]:
        """
        Gets all available workspace ids
        @return: List
        """
        self.logger.info("retrieving ws ids")

        workspaces = await self.get_workspaces()

        return [ws["workspaceId"] for ws in workspaces["workspaces"]]

    async def create_workspace(self, **kwargs) -> str:
        """

        @param kwargs: name, email etc.
        @return: string workspace id
        """
        ws_url = f"{self.base_url}/workspaces/create"
        headers = {"Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.post(ws_url, headers=headers, json=kwargs) as response:
                if not response.ok:
                    raise requests.HTTPError(response.status, await response.text())
                return await response.json()

    async def get_customer_id(self, workspace_id: str) -> Union[str, None]:
        """
        Gets customerId for a given workspace
        @param workspace_id: str ws id
        @return: str or None
        """
        self.logger.info(f"retrieving customer id for ws {workspace_id}")
        wss = await self.get_workspaces()

        for ws in wss["workspaces"]:
            if ws["workspaceId"] == workspace_id:
                return ws["customerId"]

        self.logger.warning(f"Invalid ws id {workspace_id}. \n ")

        return None

    async def get_workspace_connections(self, workspace_id: str) -> List[str]:
        """

        @param workspace_id: str
        @return: List of connection ids that belong to the given workspace
        """
        url = f"{self.base_url}/connections/list"
        headers = {"Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            self.logger.info(f"getting all connections for ws {workspace_id}")
            async with session.post(
                url=url, headers=headers, json={"workspaceId": workspace_id}
            ) as response:
                if not response.ok:
                    self.logger.error(
                        f"failed to fetch connection ids for ws {workspace_id}"
                    )
                    raise requests.HTTPError(response.status, await response.text())

                res: Dict = await response.json()

                return [c["connectionId"] for c in res["connections"]]

    async def sync_custom_connector(
        self,
        workspace_id: str,
        connection_name: str,
        repository_url: str,
        image_tag: str,
        connector_type: ConnectionType,
        documentation_url: Optional[str] = "",
        timeout: int = 300,
    ) -> Dict:
        """
        This method takes Airbyte public/private docker custom connector repository details and pushes them into the
        running Airbyte instance.

        Note that K8s requires secrets to authenticate into any private image repository in order to
        pull images.
        For more information checkout the following documentation: https://docs.airbyte.com/operator-guides/using-custom-connectors/#for-kubernetes-airbyte-deployments


        @param workspace_id: Airbyte workspace id
        @param connection_name: The name of connection (ex. source-google-docs | destination-google-docs)
        @param repository_url: Private repository name (ex airbyte/source-pokeapi)
        @param image_tag: Image version (ex: latest)
        @param connector_type: Type of the connector that needs to be synced (ex: SOURCE | DESTINATION)
        @param documentation_url: Optional
        @param timeout: Timeout (in seconds) if server fails to create resource
        @return:
        """
        url = f"{self.base_url}/{connector_type.name.lower()}_definitions/create_custom"
        headers = {"Content-Type": "application/json"}

        payload = {
            "workspaceId": workspace_id,
            f"{connector_type.name.lower()}Definition": {
                "name": connection_name,
                "documentationUrl": documentation_url,
                "dockerRepository": repository_url,
                "dockerImageTag": image_tag,
            },
        }

        async with aiohttp.ClientSession() as session:
            self.logger.info(
                f"trying to pull {connector_type.name.lower()} connector image "
                f"{repository_url}:{image_tag} into ws {workspace_id}"
            )
            async with session.post(
                url, headers=headers, json=payload, timeout=timeout
            ) as response:
                if not response.ok:
                    self.logger.error(
                        f"failed to pull image {repository_url}:{image_tag} into ws {workspace_id}"
                    )
                    raise requests.HTTPError(response.status, await response.text())
                return await response.json()
