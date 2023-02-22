from enum import Enum
from abc import ABCMeta, abstractmethod

from src.sensor.BSensor import SensorBase
from src.device.DStaticMobilityModel import StaticMobilityModel
from src.device.DTraceMobilityModel import TraceMobilityModel


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
        self.entity_id = params.get('id', None)
        self.positions: dict = params.get('positions', None)

        self.type: EntityType = EntityType.VEHICLE
        self.status: EntityStatus = EntityStatus.INACTIVE

        self.collected_data = 0
        self.location = [0.0, 0.0]

        self.sensors: dict[int, SensorBase] = sensors

        self._initiate_models()

    def _initiate_models(self):
        """
        Initiate the models related to this entity.
        """
        # Create the mobility model
        self._create_mobility_model(self.positions)

    def _create_mobility_model(self, positions: dict):
        """
        Create a mobility model for the entity.

        Parameters
        ----------
        positions : list
            List of positions for the entity.
        """
        if len(positions) == 1:
            # Static entity, create a static mobility model
            self.mobility_model = StaticMobilityModel(positions)
        else:
            # Mobile entity, create a trace mobility model
            self.mobility_model = TraceMobilityModel(positions)

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

    @abstractmethod
    def get_location(self) -> list[float]:
        """Get the location of the entity."""
        pass

    def update(self, time: int):
        """
        Update the entity.
        """
        # Update the location of the entity
        self.mobility_model.update_location(time)
        self.location = self.mobility_model.get_current_location()

        # Get the data collected by the sensors

        for sensor in self.sensors.values():
            sensor.get_collected_data_size(time)
