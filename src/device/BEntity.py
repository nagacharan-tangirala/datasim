from enum import Enum
from abc import ABCMeta, abstractmethod

from src.sensor.BSensor import SensorBase
from src.device.SEntityModelFactory import EntityModelFactory


class EntityStatus(Enum):
    """Enum for entity status."""

    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    OFFLINE = 'OFFLINE'


class EntityType(Enum):
    """Enum for entity types."""

    RSU = 'RSU'
    VEHICLE = 'VEHICLE'
    INFRA = 'INFRA'
    IOT = 'IOT'
    

class EntityBase(metaclass=ABCMeta):
    """Base class for all entity classes."""

    def __init__(self, params: dict, sensors: dict):
        """
        Initialize the entity.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the entity.
        sensors : dict
            Dictionary containing all the sensors for the entity.
        """
        self.entity_id = int(params.get('id', 0))
        self.positions: dict = params.get('positions', None)

        self.start_time = int(params.get('start_time', 0))
        self.end_time = int(params.get('end_time', 0))

        self.type: EntityType = EntityType.VEHICLE
        self.status: EntityStatus = EntityStatus.INACTIVE

        self.total_sensor_data_size = 0
        self.location = [0.0, 0.0]
        self.neighbours = []

        self.sensors: dict[int, SensorBase] = sensors

        self._initiate_models()

    def _initiate_models(self):
        """
        Initiate the models related to this entity.
        """
        # Create the entity model factory
        self.model_creator = EntityModelFactory()

        # Create the mobility model
        self.mobility_model = self.model_creator.create_mobility_model(self.positions, self.start_time)

    def get_status(self) -> str:
        """
        Get the status of the entity.

        Returns
        ----------
        str
            The current status of the entity as a string.
        """
        return self.status.value

    def get_id(self) -> int:
        """
        Get the ID of the entity.

        Returns
        ----------
        int
            The ID of the entity.
        """
        return self.entity_id

    def get_type(self) -> str:
        """
        Get the type of the entity.

        Returns
        ----------
        str
            The type of the entity as a string.
        """
        return self.type.value

    def get_collected_data_size(self):
        """
        Get the total sensor data size.

        Returns
        ----------
        int
            The total sensor data size collected since the previous update.
        """
        return self.total_sensor_data_size

    def is_entity_active(self) -> bool:
        """
        Check if the entity is active.

        Returns
        ----------
        bool
            True if the entity is active, False otherwise.
        """
        return self.status == EntityStatus.ACTIVE

    def get_start_and_end_time(self) -> tuple[int, int]:
        """
        Get the start and end time of the entity.

        Returns
        ----------
        tuple
            The start and end time of the entity as a tuple.
        """
        return self.start_time, self.end_time

    def set_neighbours(self, neighbours: list):
        """
        Set the neighbours of the entity.

        Parameters
        ----------
        neighbours : list
            List of neighbours of the entity.
        """
        self.neighbours = neighbours

    @abstractmethod
    def toggle_entity_status(self):
        """
        Toggle the status of the entity.
        """
        pass

    @abstractmethod
    def get_location(self) -> list[float]:
        """Get the location of the entity."""
        pass

    @abstractmethod
    def update_entity(self, time: int):
        """
        Update the location and collect data from the sensors associated with this entity.
        Parameters
        ----------
        time : int
            The current time in the simulation.
        """
        pass
