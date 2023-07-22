from mesa import Model
from mesa.time import BaseScheduler

from src.core.CustomExceptions import DuplicateDeviceFoundError
from src.device.VehicleUE import VehicleUE
from src.orchestrator.EdgeOrchestrator import EdgeOrchestrator


class VehicleModel(Model):
    def __init__(self, vehicles: dict[int, VehicleUE]):
        """
        Initialize the model for the vehicles.
        """
        # Override the default scheduler
        super().__init__()
        self.schedule: BaseScheduler = BaseScheduler(self)

        self._vehicles: dict[int, VehicleUE] = vehicles

        self._vehicle_activation_times: dict[int, list[int]] = {}
        self._vehicle_deactivation_times: dict[int, list[int]] = {}

        self.edge_orchestrator: EdgeOrchestrator | None = None

        self._current_time: int = -1

    @property
    def current_time(self) -> int:
        """Get the current time."""
        return self._current_time

    def _prepare_active_vehicle_times(self) -> None:
        """
        Prepare a dictionary with time step as the key and the respective vehicles to activate in that time step.
        """
        for vehicle_id, vehicle in self._vehicles.items():
            start_time, end_time = vehicle.start_time, vehicle.end_time
            self._save_activation_time(start_time, vehicle_id)
            self._save_deactivation_time(end_time, vehicle_id)

    def update_vehicles(self, vehicles: dict[int, VehicleUE]) -> None:
        """
        Update the vehicles in the model.

        Parameters
        ----------
        vehicles : dict[int, VehicleUE]
            The vehicles to update.
        """
        for vehicle_id, vehicle in vehicles.items():
            if vehicle_id in self._vehicles:
                raise DuplicateDeviceFoundError(vehicle_id, 'vehicle')
            self._vehicles[vehicle_id] = vehicle

    def _save_activation_time(self, time: int, vehicle_id: int):
        """
        Update the activation time of the vehicle.
        """
        if time not in self._vehicle_activation_times:
            self._vehicle_activation_times[time] = [vehicle_id]
        else:
            self._vehicle_activation_times[time].append(vehicle_id)

    def _save_deactivation_time(self, time: int, vehicle_id: int):
        """
        Update the deactivation time of the vehicle.
        """
        if time not in self._vehicle_deactivation_times:
            self._vehicle_deactivation_times[time] = [vehicle_id]
        else:
            self._vehicle_deactivation_times[time].append(vehicle_id)

    def _refresh_active_vehicles(self, time_step: int) -> None:
        """
        If the start or end time of an vehicle is equal to the current time step, activate or deactivate the vehicle.

        Parameters
        ----------
        time_step : int
            The time step of the simulation.
        """
        self._activate_vehicles(time_step)
        self._deactivate_vehicles(time_step)

    def _activate_vehicles(self, time_step: int) -> None:
        """
        Activate the vehicles in the current time step.
        """
        vehicles_to_activate = self._vehicle_activation_times[time_step]
        for vehicle_id in vehicles_to_activate:
            vehicle = self._vehicles[vehicle_id]
            vehicle.activate_vehicle(time_step)

            # Add to the schedule and orchestrator and set the mesa model to this
            self.schedule.add(vehicle)
            self.edge_orchestrator.add_vehicle(vehicle)
            vehicle.sim_model = self

    def _deactivate_vehicles(self, time_step: int) -> None:
        """
        Deactivate the vehicles in the current time step.
        """
        vehicles_to_deactivate = self._vehicle_deactivation_times[time_step]
        for vehicle_id in vehicles_to_deactivate:
            vehicle = self._vehicles[vehicle_id]
            vehicle.deactivate_vehicle(time_step)

            # Remove from the schedule and orchestrator and set the mesa model to None
            self.schedule.remove(vehicle)
            self.edge_orchestrator.remove_vehicle(vehicle_id)
            vehicle.sim_model = None

    def step(self, *args, **kwargs):
        """
        Step function for the model.
        """
        # Refresh the active vehicles
        current_time = int(args[0])
        if current_time in self._vehicle_activation_times:
            self._refresh_active_vehicles(current_time)

        # Step through the schedule object
        self.schedule.step()
