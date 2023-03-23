import opcode
import os
from dagster import define_asset_job, ScheduleDefinition, AssetSelection, Definitions, job, AssetKey, repository, op
from dagster_airbyte import airbyte_resource
from dagster_airbyte import load_assets_from_airbyte_instance
from dagster_airbyte import AirbyteResource

import dagster
from dagster import AssetKey
from dagster_airbyte import (
    AirbyteManagedElementReconciler,
    load_assets_from_connections, load_assets_from_airbyte_instance,
)
from dagster_airbyte.managed.generated.sources import FileSource
from dagster_airbyte.managed.generated.destinations import LocalJsonDestination, BigqueryDestination
from dagster_airbyte import AirbyteConnection, AirbyteSyncMode
from dagster_airbyte import airbyte_resource


airbyte_instance = airbyte_resource.configured(
    {
        "host": "localhost",
        "port": "8000",
        # "username": "airbyte",
        # "password": "password"
     }
)


address_source = FileSource(
    name="file-source-addresses",
    dataset_name="addresses",
    format="csv",
    url="https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv",
    provider=FileSource.HTTPSPublicWeb()

)

bq_destination = BigqueryDestination(
    name="address_destination",
    project_id="arcane-optics-380121",
    dataset_id="arcane-optics-380121.sample_dataset",
    dataset_location="europe-west2",
    loading_method=BigqueryDestination.StandardInserts(),
    credentials_json=os.environ.get("BQ_CREDENTIALS")
)

address_connection = AirbyteConnection(
    name="fetch_addresses",
    source=address_source,
    destination=bq_destination,
    stream_config={"addresses": AirbyteSyncMode.incremental_append_dedup()},
    normalize_data=False

)

reconciler = AirbyteManagedElementReconciler(
    airbyte=airbyte_instance,
    connections=[address_connection],
    delete_unmentioned_resources=False

)

# import pdb; pdb.set_trace()
if not reconciler.check().is_empty():
    print("Found changes, applying ")
    reconciler.apply()


airbyte_assets = load_assets_from_airbyte_instance(
        airbyte_instance, connection_to_asset_key_fn=lambda c, n: AssetKey([c.name, n])
    )





# def get_all_assets() -> load_assets_from_airbyte_instance:
#
#     return load_assets_from_airbyte_instance(
#         airbyte_instance, connection_to_asset_key_fn=lambda c, n: AssetKey([c.name, n])
#     )


# def check_if_asset_exists(connection_name= "fetch_addresses"):
#     conns = get_all_assets()._get_connections()
#     exists = False
#
#
#     for c in conns:
#         if isinstance(c, tuple):
#             if c[1].name == connection_name:
#                 exists = True
#
#     return exists
#
# if check_if_asset_exists():
#     print("fetch_addresses exists ")



# if not check_if_asset_exists():


