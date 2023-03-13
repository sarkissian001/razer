from typing import Union
from dagster_airbyte import airbyte_resource
from dagster_airbyte import load_assets_from_airbyte_instance

from ..common.logger import Logger


class DagsterBase:

    def __init__(
        self,
        host: str = "localhost",
        port: str = "8000",
        log_level: Union[str, None] = None,
    ):
        self.host = host
        self.port = port

        self.logger = Logger(__name__, log_level)

    def get_airbyte_instance(self):

        airbyte_instance = airbyte_resource.configured(
            {
                "host": self.host,
                "port": self.port,
            }
        )

        return load_assets_from_airbyte_instance(airbyte_instance)
