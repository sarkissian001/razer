from dagster import ResourceDefinition
from dagster_airbyte import airbyte_resource


class AirByteBase:
    """Defines all Airbyte basic functionalities"""

    def __init__(
            self,
            host: str = "localhost",
            port: str = "8000",
            username: str = "airbyte",
            password_env: str = "AIRBYTE_PASSWORD"
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password_env = password_env

        self._init = None

    def init(self) -> ResourceDefinition:

        if not self._init:
            self._init = airbyte_resource.configured(
                {
                    "host": self.host,
                    "port": self.port,
                    "username": self.username,
                    "password": {"env": self.password_env},
                }
            )

        return self._init
    