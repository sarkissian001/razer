import asyncio

from razer_dagster_manager import ConnectionType
from razer_dagster_manager import AirByteBase


obj = AirByteBase()


ws_id: list = asyncio.run(obj.get_workspace_ids())

print("ws-ids: ", ws_id)

print(f"using workspace {ws_id[0]}")

res = asyncio.run(obj.sync_custom_connector(
    workspace_id=ws_id[0],
    image_tag="latest",
    repository_url="airbyte/destination-sqlite",
    connection_name="Destination Test1",
    connector_type=ConnectionType.DESTINATION

)
)

print(res)
