from typing import Dict, List, Optional, Union

import aiohttp
import requests

from ..Enums.airbyte_connector_types import ConnectionType
from ..common.logger import Logger


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

    async def create_workspace(self, **kwargs) -> Dict:
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

    async def get_or_create_workspace(self, workspace_name: str, **kwargs) -> str:
        """
        if workspace already exists returns ws id otherwise creates a new ws and returns id

        @param workspace_name: workspace_name
        @param workspace_name: other details, such as name, customerId etc
        @return: string workspace id

        """

        workspaces: Dict = await self.get_workspaces()

        for w in workspaces["workspaces"]:
            if w["name"] == workspace_name:
                self.logger.info(
                    f"`{workspace_name}` already exists , getting workspace_id"
                )
                return w["workspaceId"]

        self.logger.info(f"`{workspace_name}` doesn't exists , creating workspace")
        w: Dict = await self.create_workspace(name=workspace_name, **kwargs)

        return w["workspaceId"]

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

        Returns all connections that have been created in the workspace; that is source <> destination pairs

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

    async def get_configured_connectors(
        self, workspace_id: str, connector_type: ConnectionType
    ) -> List[Dict]:
        """
        Returns list of sources/destinations that have been configured in the workspace.
        Note: This is not the same as available connectors which can be used but rather source connections which have been configured

        @param workspace_id: str
        @param connector_type: Enum
        @return: List
        """

        connector_type_name: str = connector_type.name.lower()

        url = f"{self.base_url}/{connector_type_name}" + "s" + "/list"
        headers = {"Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            self.logger.info(
                f"getting list of {connector_type_name} configured in ws {workspace_id}"
            )
            async with session.post(
                url=url, headers=headers, json={"workspaceId": workspace_id}
            ) as response:
                if not response.ok:
                    self.logger.error(
                        f"failed to fetch list of {connector_type_name} configured in ws {workspace_id}"
                    )
                    raise requests.HTTPError(response.status, await response.text())
                res: Dict = await response.json()
                return res[f"{connector_type_name}s"]

    async def get_all_connector_definitions(
        self, workspace_id: str, connector_type: ConnectionType
    ) -> List[Dict]:
        """
        Returns the source/destination connector definitions
        @param workspace_id:
        @param connector_type: Enum,
        @return:
        """

        connector_type_name: str = connector_type.name.lower()

        url = f"{self.base_url}/{connector_type_name}_definitions/list_for_workspace"
        headers = {"Content-Type": "application/json"}

        self.logger.info(
            f"getting all `{connector_type_name}` connector definitions for ws {workspace_id}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=headers, json={"workspaceId": workspace_id}
            ) as response:
                if not response.ok:
                    self.logger.info(
                        f"failed to get `{connector_type_name}` definitions for ws {workspace_id}"
                    )
                    raise requests.HTTPError(response.status, await response.text())

                res: Dict = await response.json()

                return res[f"{connector_type_name}Definitions"]

    async def get_all_connector_names(
        self, workspace_id: str, connector_type: ConnectionType
    ) -> List[str]:
        """
        Returns the names of source/destination connectors available in Airbyte
        @param workspace_id:
        @param connector_type: Enum,
        @return: List
        """

        self.logger.info(
            f"getting {connector_type.name} connectors' names for ws {workspace_id}"
        )

        connectors = await self.get_all_connector_definitions(
            workspace_id, connector_type
        )

        return [name["name"] for name in connectors]

    async def get_connector_definition_id_by_name(
        self, workspace_id: str, connector_name: str, connector_type: ConnectionType
    ) -> Union[str, None]:
        """

        Returns the source/destination definition id for a given connector

        @param workspace_id: workspace id
        @param connector_name: name of the connector
        @param connector_type: Enum,
        @return: connector definition id if connector exists else None
        """

        # TODO: consider caching
        connector_definitions: List = await self.get_all_connector_definitions(
            workspace_id=workspace_id, connector_type=connector_type
        )

        connector_type_name: str = connector_type.name.lower()

        self.logger.info(
            f"trying to get {connector_type_name} definition id for `{connector_name}` connector"
        )

        for connector in connector_definitions:
            if connector["name"] == connector_name:
                return connector[f"{connector_type_name}DefinitionId"]

        self.logger.info(
            f"couldn't find {connector_type_name}DefinitionId for specified "
            f"{connector_type_name} {connector_name}. "
            f"Make sure such {connector_type_name} is available/configured"
        )

        return None

    async def configure_connector(
        self,
        workspace_id: str,
        name: str,
        connector_name: str,
        connector_type: ConnectionType,
        connection_configs: Dict,
        ignore_duplicates: bool = False,
    ) -> Union[Dict, None]:
        """

        Sets up source/destination connector in ws (not to confuse with custom connectors, this is just to create
         a source or a destination)

        @param ignore_duplicates: If set to False it can create sources with duplicated names
        @param workspace_id: ws id
        @param name: source/destination connection name (ex: MyMongodbSource, my-big-query-destination etc..)
        @param connector_name: connector name (ex. File, Mongodb, some-custom-connector, etc...)
        @param connector_type: Enum
        @param connection_configs: connection configs ( an example of a source config for a file may look something like
         this:

            ```
                    {
                        "dataset_name": "addresses",
                        "provider": {
                          "storage": "HTTPS",
                          "user_agent": false
                        },
                        "format": "csv",
                        "url": "https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv"
              }

        ```
        @return: Dict
        """

        connector_type_name: str = connector_type.name.lower()

        url = f"{self.base_url}/{connector_type_name}" + "s" + "/create"
        headers = {"Content-Type": "application/json"}

        if not ignore_duplicates:
            cons = await self.get_configured_connectors(
                workspace_id=workspace_id, connector_type=connector_type
            )

            for c in cons:
                if c["name"] == name:
                    self.logger.warning(
                        f"{connector_name} connector with the name {name} is already configured in ws {workspace_id}"
                    )
                    return None

        definition_id: str = await self.get_connector_definition_id_by_name(
            workspace_id, connector_name, connector_type
        )

        if not definition_id:
            raise ValueError(f"Unknown source {connector_name}")

        payload = {
            "connectionConfiguration": connection_configs,
            "name": name,
            f"{connector_type_name}DefinitionId": definition_id,
            "workspaceId": workspace_id,
        }

        async with aiohttp.ClientSession() as session:
            self.logger.info(
                f"configuring a {connector_name} connection with name `{name}` in ws {workspace_id}"
            )
            async with session.post(url, headers=headers, json=payload) as response:
                if not response.ok:
                    self.logger.error(
                        f"failed to configure {connector_name} connection with the name `{name}` in ws {workspace_id}"
                    )
                    raise requests.HTTPError(response.status, await response.text())
                self.logger.info(
                    f"successfully configured a new {connector_name} {connector_type_name} "
                    f"connector with name {name} in ws {workspace_id}"
                )
                return await response.json()

    async def sync_custom_connector(
        self,
        workspace_id: str,
        connection_name: str,
        repository_url: str,
        image_tag: str,
        connector_type: ConnectionType,
        documentation_url: Optional[str] = "",
        timeout: int = 300,
        ignore_if_exits: bool = False,
    ) -> Union[None, Dict]:
        """
        This method takes Airbyte public/private docker custom connector repository details and pushes them into the
        running Airbyte instance.

        Note that K8s requires secrets to authenticate into any private image repository in order to
        pull images.
        For more information checkout the following documentation: https://docs.airbyte.com/operator-guides/using-custom-connectors/#for-kubernetes-airbyte-deployments


        @param ignore_if_exits: False, If the custom connector already exists do not recreate it
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

        if not ignore_if_exits:
            connectors: List = await self.get_all_connector_names(
                workspace_id, connector_type
            )
            for c in connectors:
                if c == connection_name:
                    self.logger.warning(
                        f"custom connector with the name {connection_name} already exists in ws {workspace_id}"
                    )
                    return None

        async with aiohttp.ClientSession() as session:
            self.logger.info(
                f"trying to pull {connector_type.name.lower()} connector image with name `{connection_name}` from repo "
                f"`{repository_url}:{image_tag}` into ws {workspace_id}"
            )
            async with session.post(
                url, headers=headers, json=payload, timeout=timeout
            ) as response:
                if not response.ok:
                    self.logger.error(
                        f"failed to pull image {repository_url}:{image_tag} into ws {workspace_id}"
                    )
                    raise requests.HTTPError(response.status, await response.text())

                self.logger.info(f"successfully pulled image {repository_url}:{image_tag} into ws {workspace_id}")
                return await response.json()
