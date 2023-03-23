import abc
from typing import List

from dagster_airbyte import AirbyteConnection, AirbyteSource, AirbyteDestination


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
    def source(self) -> AirbyteSource:
        pass

    @abc.abstractmethod
    def destination(self) -> AirbyteDestination:
        pass

    @abc.abstractmethod
    def connection(self, conn_name: str) -> AirbyteConnection:
        pass


class AirbyteConnectionManager:
    """
    A class that manages Airbyte connections.
    """

    @classmethod
    def init_connections(cls, connection_classes) -> List:
        """
        Initializes a list of Airbyte connections based on the given connection classes.

        :param connection_classes: A list of Airbyte connection classes to use for creating connections.
        :type connection_classes: List[type]
        :return: A list of Airbyte connections.
        :rtype: List[AirbyteConnection]
        """
        connections = []
        for connection_class in connection_classes:
            connection_instance = connection_class()
            connection = connection_instance.connection()
            connections.append(connection)
        return connections
