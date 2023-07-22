from mesa import Agent
from pandas import DataFrame

from src.application.Payload import BaseStationPayload, BaseStationResponse
from src.device.BaseStation import BaseStation
from src.device.CentralController import CentralController
from src.models.ModelFactory import ModelFactory


class CloudOrchestrator(Agent):
    def __init__(self,
                 controllers: dict,
                 base_stations: dict[int, BaseStation],
                 controller_links_df: DataFrame):
        """
        Initialize the cloud orchestrator.

        Parameters
        ----------
        controllers : dict
            The controllers in the network.
        base_stations : dict[int, BaseStation]
            The base stations in the network.
        controller_links_df : DataFrame
            The links between the controllers.
        """
        super().__init__(0, None)

        self._controllers: dict[int, CentralController] = controllers
        self._base_stations: dict[int, BaseStation] = base_stations
        self._controller_links_df: DataFrame = controller_links_df

        # Uplink data generated at the basestations
        self.data_at_basestations: dict[int, BaseStationPayload] = {}

        # Uplink base station data along with the target controllers
        self.uplink_basestations_data: dict[int, dict[int, BaseStationPayload]] = {}

        # Downlink response created at the controllers
        self.downlink_response_at_controllers: dict[int, dict[int, BaseStationResponse]] = {}

        self._base_station_controller_dict = {}
        self._current_time: int = -1

    @property
    def current_time(self) -> int:
        """Get the time stamp."""
        return self._current_time

    @current_time.setter
    def current_time(self, value: int) -> None:
        """ Set the current time."""
        self._current_time = value

    def _prepare_network_mappings(self) -> None:
        """
        Prepare the base station controller mapping.
        """
        # Prepare the dict with second column as the key and the third column as the value
        self._base_station_controller_dict = {row[1]: row[2] for row in self._controller_links_df.values}

    def _create_models(self, model_data: dict):
        """
        Create the models
        """
        model_factory = ModelFactory()

    def uplink_stage(self) -> None:
        """
        Step through the orchestration process for the uplink stage.
        This is the second step in the overall simulation.
        """
        # Step through the models.

        # Collect data from each base station
        self._collect_data_from_basestations()

        # Find target controllers
        self._assign_target_controllers()

        # Send data to controllers
        self._send_data_to_controllers()

    def _collect_data_from_basestations(self) -> None:
        """
        Collect data from each base station.
        """
        self.data_at_basestations.clear()
        for station_id, base_station in self._base_stations.items():
            self.data_at_basestations[station_id] = base_station.uplink_payload
            # Consume the wired bandwidth in the base station.
            base_station.use_wired_for_uplink()

    def _assign_target_controllers(self) -> None:
        """
        Assign target controllers for each base station.
        """
        # Clear the previous data
        self.uplink_basestations_data.clear()

        for base_station_id, base_station_data in self.data_at_basestations.items():
            # Find the controller for the base station
            controller_id = self._base_station_controller_dict[base_station_id]

            if controller_id not in self.uplink_basestations_data:
                self.uplink_basestations_data[controller_id] = {}
            self.uplink_basestations_data[controller_id][base_station_id] = base_station_data

    def _send_data_to_controllers(self) -> None:
        """
        Send data to controllers.
        """
        for controller_id, base_station_data in self.uplink_basestations_data.items():
            self._controllers[controller_id].received_data = base_station_data
            # Consume the wired network bandwidth in the base station.
            self._base_stations[controller_id].use_wired_for_uplink()

    def downlink_stage(self) -> None:
        """
        Step through the orchestration process for the downlink stage.
        """
        # Collect data from each controller
        self._collect_data_from_controllers()

        # Send data to base stations
        self._send_data_to_basestations()

    def _collect_data_from_controllers(self) -> None:
        """
        Collect data from each controller.
        """
        self.downlink_response_at_controllers.clear()
        for controller_id, controller in self._controllers.items():
            self.downlink_response_at_controllers[controller_id] = controller.downlink_response
            # Controller has to consume the wired bandwidth
            controller.use_network_for_downlink()

    def _send_data_to_basestations(self) -> None:
        """
        Send data to base stations.
        """
        for controller_id, controller_data in self.downlink_response_at_controllers.items():
            for station_id, station_data in controller_data:
                self._base_stations[station_id].downlink_response = station_data
                # Consume the network bandwidth in the base station.
                self._base_stations[station_id].use_wired_for_downlink()
