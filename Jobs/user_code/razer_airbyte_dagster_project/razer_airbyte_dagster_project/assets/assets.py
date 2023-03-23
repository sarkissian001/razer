from typing import List
import hashlib

import dagster
from dagster import AssetKey
from dagster_airbyte import (
    AirbyteManagedElementReconciler,
    load_assets_from_connections, load_assets_from_airbyte_instance,
)
from dagster_airbyte.asset_defs import AirbyteInstanceCacheableAssetsDefinition
from dagster_airbyte.managed.generated.sources import FileSource
from dagster_airbyte.managed.generated.destinations import LocalJsonDestination, BigqueryDestination
from dagster_airbyte import AirbyteConnection, AirbyteSyncMode
from dagster_airbyte import airbyte_resource

from razer_airbyte_dagster_project.connections.connections import UserDefinedConnections
# from razer_airbyte_dagster_project.connections.connections import AirbyteAddresses


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


# airbyte_assets = load_assets_from_airbyte_instance(
#     airbyte_instance,
#     key_prefix="airbyte_integrations",
#     connections=manager.connections,
#
# )