import abc
from typing import List, Union, Iterable

from dagster_airbyte import (
    AirbyteConnection,
    AirbyteSource,
    AirbyteDestination,
    AirbyteManagedElementReconciler,
)
from dagster._core.definitions.resource_definition import ResourceDefinition
from dagster_managed_elements import ManagedElementDiff, ManagedElementError

from ..common.logger import Logger


class AirbyteConnectionsBase(abc.ABC):
    """
    Base abstract class for Airbyte connections.

    Defines the interface for defining sources, destinations, and connections.

    Subclasses must implement the `source`, `destination`, and `connection` methods.

    Attributes:
        None

    Methods:
        source() -> object: bstract method for defining Airbyte source connection (can be found here `dagster_airbyte.managed.generated.sources`)
        destination() -> object: Abstract method for defining Airbyte destination connection (can be found here `dagster_airbyte.managed.generated.destinations`)
        connection(conn_name: str) -> AirbyteConnection: Abstract method for creating an `AirbyteConnection`.

    Returns:
        None
    """

    @abc.abstractmethod
    def source(self, source_name: str) -> AirbyteSource:
        pass

    @abc.abstractmethod
    def destination(self, destination_name: str) -> AirbyteDestination:
        pass

    @abc.abstractmethod
    def connection(self, connection_name: str) -> AirbyteConnection:
        pass


class AirbyteConnectionManager:
    """
    A class that manages Airbyte connections.
    """

    LOGGER = Logger(__name__)

    def __init__(self, connections: Iterable[AirbyteConnection]) -> None:
        self.connections = connections

    def reconcile_connections(
        self,
        airbyte_instance: ResourceDefinition,
        delete_unmanaged_resources: bool = False,
    ) -> None:
        """
        Reconciles the Airbyte connections.

        :param airbyte_instance: An instance of the Airbyte resource definition.
        :type airbyte_instance: dagster._core.definitions.resource_definition.ResourceDefinition

        :param delete_unmanaged_resources: delete_unmentioned_resources (bool): Whether to delete resources that are not mentioned in
                the set of connections provided. When True, all Airbyte instance contents are effectively
                managed by the reconciler. Defaults to False.
        :type connections: List[AirbyteConnection]

        """
        reconciler = AirbyteManagedElementReconciler(
            airbyte=airbyte_instance,
            connections=self.connections,
            delete_unmentioned_resources=delete_unmanaged_resources,
        )

        changes: Union[ManagedElementDiff, ManagedElementError] = reconciler.check()

        if not changes.is_empty():
            self.LOGGER.debug(
                f"found changes in connections {self.connections} \n applying changes"
            )
            if changes.modifications:
                self.LOGGER.debug(f"modified changes are {changes.modifications} ")

            if changes.deletions:
                self.LOGGER.debug(f"deleted changes are {changes.modifications} ")

            reconciler.apply()

            return None

        self.LOGGER.debug(f"No connections changes were found.")

    @classmethod
    def init_connections(
        cls, connection_classes: List[abc.ABCMeta]
    ) -> "AirbyteConnectionManager":
        """
        Initializes a list of Airbyte connections based on the given connection classes.

        :param connection_classes: A list of Airbyte connection classes to use for creating connections.
        :type connection_classes: List[type]
        :return: A list of Airbyte connections.
        :rtype: List[AirbyteConnection]
        """
        connections: List = []
        for connection_class in connection_classes:
            connection_instance = connection_class()
            connection = connection_instance.connection()
            connections.append(connection)

        return cls(connections)
