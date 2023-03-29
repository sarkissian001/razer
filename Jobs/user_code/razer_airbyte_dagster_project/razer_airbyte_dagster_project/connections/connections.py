import os
from typing import List

from dagster_airbyte.managed.generated.sources import FileSource
from dagster_airbyte.managed.generated.destinations import BigqueryDestination
from dagster_airbyte import AirbyteConnection, AirbyteSyncMode

from razer_dagster_manager import AirbyteConnectionsBase


class AirbyteAddresses(AirbyteConnectionsBase):
    def source(self, source_name="file-source-addresses"):
        return FileSource(
            name=source_name,
            dataset_name="addresses",
            format="csv",
            url="https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv",
            provider=FileSource.HTTPSPublicWeb(),
        )

    def destination(self, destination_name="bq-destination-address"):
        return BigqueryDestination(
            name=destination_name,
            project_id=os.environ.get("BQ_PROJECT_ID"),
            dataset_id=os.environ.get("BQ_DATASET_ID"),
            dataset_location="europe-west2",
            loading_method=BigqueryDestination.StandardInserts(),
            credentials_json=os.environ.get("BQ_CREDENTIALS"),
        )

    def connection(self, connection_name: str = "fetch_addresses"):
        return AirbyteConnection(
            name=connection_name,
            source=self.source(),
            destination=self.destination(),
            stream_config={"addresses": AirbyteSyncMode.incremental_append_dedup()},
            normalize_data=False,
        )


class AirbyteCities(AirbyteConnectionsBase):
    def source(self, source_name="file-source-cities"):
        return FileSource(
            name="file-source-cities",
            dataset_name="cities",
            format="csv",
            url="https://people.sc.fsu.edu/~jburkardt/data/csv/cities.csv",
            provider=FileSource.HTTPSPublicWeb(),
        )

    def destination(self, destination_name="cities_destination"):
        return BigqueryDestination(
            name=destination_name,
            project_id="arcane-optics-380121",
            dataset_id="arcane-optics-380121.sample_dataset",
            dataset_location="europe-west2",
            loading_method=BigqueryDestination.StandardInserts(),
            credentials_json=os.environ.get("BQ_CREDENTIALS"),
        )

    def connection(self, connection_name: str = "fetch_cities"):
        return AirbyteConnection(
            name=connection_name,
            source=self.source(),
            destination=self.destination(),
            stream_config={"cities": AirbyteSyncMode.incremental_append_dedup()},
            normalize_data=False,
        )


class UserDefinedConnections:
    # Add UDC here
    CONNECTIONS = [
        AirbyteAddresses,
        AirbyteCities,
    ]

    def get_user_defined_connections(self) -> List:

        return self.CONNECTIONS



