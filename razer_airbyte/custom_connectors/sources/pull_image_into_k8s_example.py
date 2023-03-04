import asyncio

from src.razer.airbyte_base.airbyte_base import AirByteBase
from src.razer.Enums.airbyte_connector_types import ConnectionType

obj = AirByteBase()


ws_id: list = asyncio.run(obj.get_workspace_ids())

print("ws-ids: ", ws_id)

print(f"using workspace {ws_id[0]}")

res = asyncio.run(obj.sync_custom_connector(
    workspace_id=ws_id[0],
    image_tag="0.1.5",
    repository_url="airbyte/source-pokeapi",
    connection_name="Source Test1",
    connector_type=ConnectionType.SOURCE

)
)

print(res)
