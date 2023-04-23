from typing import List
from dagster_airbyte import (
    load_assets_from_connections
)

from dagster_airbyte import airbyte_resource

from razer_airbyte_dagster_project.connections.connections import UserDefinedConnections


from razer_dagster_manager import AirbyteConnectionManager

airbyte_instance = airbyte_resource.configured(
    {
        "host": "localhost",
        "port": "8000",
        # "username": "airbyte",
        # "password": "password"
    }
)


connection_classes: List = UserDefinedConnections().get_user_defined_connections()
manager = AirbyteConnectionManager.init_connections(connection_classes=connection_classes)
manager.reconcile_connections(airbyte_instance)


# loads only specified connections
airbyte_assets = load_assets_from_connections(
    airbyte=airbyte_instance,
    connections=manager.connections,
    key_prefix="airbyte_integrations",
)