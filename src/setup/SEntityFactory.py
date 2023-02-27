from src.device.DVehicleEntity import VehicleEntity
from src.device.DRSUEntity import RSUEntity


class EntityFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_entity(params: dict, sensors: dict):
        """
        Create an entity from the given parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the entity.
        sensors : dict
            Dictionary containing all the sensors for the entity.
        """
        entity_type = params.get('type', None)
        if entity_type == 'vehicle':
            return VehicleEntity(params, sensors)
        elif entity_type == 'rsu':
            return RSUEntity(params, sensors)
        else:
            raise ValueError("Entity type not supported.")
