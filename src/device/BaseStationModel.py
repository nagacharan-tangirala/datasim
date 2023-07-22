from mesa import Model
from mesa.time import BaseScheduler

from src.core.CustomExceptions import DuplicateDeviceFoundError
from src.device.BaseStation import BaseStation


class BaseStationModel(Model):
    def __init__(self, base_stations: dict[int, BaseStation]):
        """
        Initialize the base station model.
        """
        super().__init__()

        self.base_stations: dict[int, BaseStation] = base_stations

        self.schedule: BaseScheduler = BaseScheduler(self)
        self._add_base_stations_to_scheduler()

    def _add_base_stations_to_scheduler(self) -> None:
        """
        Add the base_stations to the scheduler.
        """
        for base_station in self.base_stations.values():
            self.schedule.add(base_station)

    def step(self) -> None:
        """
        Step function for the model. This function is called every time step.
        """
        # Step the scheduler
        self.schedule.step()

    def update_base_stations(self, new_base_stations: dict[int, BaseStation]) -> None:
        """
        Update the base stations.
        """
        for base_station_id, base_station in new_base_stations:
            if base_station_id in self.base_stations:
                raise DuplicateDeviceFoundError(base_station_id, 'base station')
            self.base_stations[base_station_id] = base_station
