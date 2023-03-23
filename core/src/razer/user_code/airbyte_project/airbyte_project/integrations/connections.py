import os
import sys
from dagster_airbyte.managed.generated.sources import FileSource
from dagster_airbyte.managed.generated.destinations import BigqueryDestination
from dagster_airbyte import AirbyteConnection, AirbyteSyncMode


# TODO: Need to create package
# Add the parent directory of the `core` module to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# Import the `AirByteBase` module
from core.src.razer.dagster_base.dagster_base import AirbyteConnectionsBase, AirbyteConnectionManager


class AirbyteAddresses(AirbyteConnectionsBase):

    def source(self):
        return FileSource(
            name="file-source-addresses",
            dataset_name="addresses",
            format="csv",
            url="https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv",
            provider=FileSource.HTTPSPublicWeb()
        )

    def destination(self):
        return BigqueryDestination(
            name="address_destination",
            project_id="arcane-optics-380121",
            dataset_id="arcane-optics-380121.sample_dataset",
            dataset_location="europe-west2",
            loading_method=BigqueryDestination.StandardInserts(),
            credentials_json=os.environ.get("BQ_CREDENTIALS")
        )

    def connection(self, conn_name: str):
        return AirbyteConnection(
            name=conn_name,
            source=self.source(),
            destination=self.destination(),
            stream_config={"addresses": AirbyteSyncMode.incremental_append_dedup()},
            normalize_data=False
        )


class AirbyteCities(AirbyteConnectionsBase):

    def source(self):
        return FileSource(
            name="file-source-addresses",
            dataset_name="addresses",
            format="csv",
            url="https://people.sc.fsu.edu/~jburkardt/data/csv/cities.csv",
            provider=FileSource.HTTPSPublicWeb()
        )

    def destination(self):
        return BigqueryDestination(
            name="address_destination",
            project_id="arcane-optics-380121",
            dataset_id="arcane-optics-380121.sample_dataset",
            dataset_location="europe-west2",
            loading_method=BigqueryDestination.StandardInserts(),
            credentials_json=os.environ.get("BQ_CREDENTIALS")
        )

    def connection(self, conn_name: str):
        return AirbyteConnection(
            name=conn_name,
            source=self.source(),
            destination=self.destination(),
            stream_config={"cities": AirbyteSyncMode.incremental_append_dedup()},
            normalize_data=False
        )