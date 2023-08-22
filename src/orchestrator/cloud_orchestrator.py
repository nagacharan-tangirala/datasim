import logging

from mesa import Agent
from pandas import DataFrame

from src.core.constants import MainKey
from src.device.base_station import BaseStation
from src.device.controller import CentralController
from src.device.payload import BaseStationPayload, BaseStationResponse

logger = logging.getLogger(__name__)


class CloudOrchestrator(Agent):
    def __init__(self, controller_links_df: DataFrame, model_data: dict):
        """
        Initialize the cloud orchestrator.

        Parameters
        ----------
        controller_links_df : DataFrame
            The links between the controllers.
        model_data : dict
            The model data.
        """
        super().__init__(990001, None)
        self.type: str = MainKey.CLOUD_ORCHESTRATOR
        self.model = None

        self._controllers: dict[int, CentralController] = {}
        self._base_stations: dict[int, BaseStation] = {}
        self._controller_links_df: DataFrame = controller_links_df

        # Uplink data generated at the basestations
        self.data_at_basestations: dict[int, BaseStationPayload] = {}

        # Uplink base station data along with the target controllers
        self.uplink_basestations_data: dict[int, dict[int, BaseStationPayload]] = {}

        # Downlink response created at the controllers
        self.downlink_response_at_controllers: dict[
            int, dict[int, BaseStationResponse]
        ] = {}

        # Prepare the dict with second column as the key and the third column as the value

        self._create_models(model_data)

    @property
    def data_generated_at_device(self) -> float:
        """Get the data generated at the device."""
        return -1.0

    @property
    def vehicles_in_range(self) -> int:
        """Get the number of vehicles in range."""
        return -1

    def active_controller_count(self) -> int:
        """
        Get the active controller count in the cloud orchestrator.

        Returns
        -------
        int
            The active controller count.
        """
        return len(self._controllers)

    def add_controller(self, controller: CentralController) -> None:
        """
        Add a new controller to the cloud orchestrator.

        Parameters
        ----------
        controller : CentralController
            The controller to add.
        """
        self._controllers[controller.unique_id] = controller

    def remove_controller(self, controller_id: int) -> None:
        """
        Remove the controller from the cloud orchestrator.

        Parameters
        ----------
        controller_id : int
            The id of the controller to remove.
        """
        self._controllers.pop(controller_id)

    def add_base_station(self, base_station: BaseStation) -> None:
        """
        Add a new base station to the cloud orchestrator.

        Parameters
        ----------
        base_station : BaseStation
            The base station to add to the cloud orchestrator.
        """
        self._base_stations[base_station.unique_id] = base_station

    def remove_base_station(self, base_station_id: int) -> None:
        """
        Remove the base station from the cloud orchestrator.

        Parameters
        ----------
        base_station_id : int
            The id of the base station to remove.
        """
        self._base_stations.pop(base_station_id)

    def update_b2c_links(self, b2c_links: DataFrame) -> None:
        """
        Update the B2B links.

        Parameters
        ----------
        b2c_links : DataFrame
            The new B2C links.

        Returns
        -------
        None
        """
        self._controller_links_df = b2c_links

    def _prepare_network_mappings(self) -> None:
        """
        Prepare the base station controller mapping.
        """
        pass

    def get_total_data_at_controllers(self) -> float:
        """
        Get the total data at the controllers.

        Returns
        -------
        float
            The total data at the controllers.
        """
        total_data: float = 0.0
        for controller in self._controllers.values():
            total_data += controller.total_data_received
        return total_data

    def get_visible_vehicles_at_controllers(self) -> int:
        """
        Get the total number of vehicles visible to the controllers.

        Returns
        -------
        int
            The total number of vehicles.
        """
        total_vehicles: int = 0
        for controller in self._controllers.values():
            total_vehicles += controller.vehicles_in_range
        return total_vehicles

    def get_data_sizes_by_type(self) -> dict[str, float]:
        """
        Get the data sizes of each type at the controllers.

        Returns
        -------
        dict[str, float]
            The data types and sizes.
        """
        data_types_sizes: dict = {}
        for controller in self._controllers.values():
            type_sizes = controller.data_sizes_by_type
            for data_type, size in type_sizes.items():
                if data_type not in data_types_sizes:
                    data_types_sizes[data_type] = 0.0
                data_types_sizes[data_type] += size

        return data_types_sizes

    def get_data_counts_by_type(self) -> dict[str, int]:
        """
        Get the data counts by type at the controllers.

        Returns
        -------
        dict[str, int]
            The data counts by type.
        """
        data_types_counts: dict = {}
        for controller in self._controllers.values():
            type_counts = controller.data_counts_by_type
            for data_type, count in type_counts.items():
                if data_type not in data_types_counts:
                    data_types_counts[data_type] = 0
                data_types_counts[data_type] += count

        return data_types_counts

    def _create_models(self, model_data: dict):
        """
        Create the models.
        """
        pass

    def uplink_stage(self) -> None:
        """
        Step through the orchestration process for the uplink stage.

        This is the second step in the overall simulation.
        """
        logger.debug(f"Uplink stage at time {self.model.current_time}.")
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
        logger.debug("Collecting data from base stations.")
        self.data_at_basestations.clear()
        for station_id, base_station in self._base_stations.items():
            self.data_at_basestations[station_id] = base_station.uplink_payload
            # Consume the wired bandwidth in the base station.
            base_station.use_wired_for_uplink()

    def _assign_target_controllers(self) -> None:
        """
        Assign target controllers for each base station.
        """
        logger.debug("Assigning target controllers.")
        # Clear the previous data
        self.uplink_basestations_data.clear()

        for base_station_id, base_station_data in self.data_at_basestations.items():
            # Find the controller for the base station
            controller_id = self._base_station_controller_dict[base_station_id]

            if controller_id not in self.uplink_basestations_data:
                self.uplink_basestations_data[controller_id] = {}
            self.uplink_basestations_data[controller_id][
                base_station_id
            ] = base_station_data

    def _send_data_to_controllers(self) -> None:
        """
        Send data to controllers.
        """
        logger.debug("Sending data to controllers.")
        for controller_id, base_station_data in self.uplink_basestations_data.items():
            self._controllers[controller_id].received_data = base_station_data
            # Consume the wired network bandwidth in the base station.
            self._controllers[controller_id].use_network_for_uplink()

    def downlink_stage(self) -> None:
        """
        Step through the orchestration process for the downlink stage.
        """
        logger.debug(f"Downlink stage at time {self.model.current_time}.")
        # Collect data from each controller
        self._collect_data_from_controllers()

        # Send data to base stations
        self._send_data_to_basestations()

    def _collect_data_from_controllers(self) -> None:
        """
        Collect data from each controller.
        """
        logger.debug("Collecting data from controllers.")
        self.downlink_response_at_controllers.clear()
        for controller_id, controller in self._controllers.items():
            self.downlink_response_at_controllers[
                controller_id
            ] = controller.downlink_response
            # Controller has to consume the wired bandwidth
            controller.use_network_for_downlink()

    def _send_data_to_basestations(self) -> None:
        """
        Send data to base stations.
        """
        logger.debug("Sending data to base stations.")
        for controller_data in self.downlink_response_at_controllers.values():
            for station_id, station_data in controller_data.items():
                self._base_stations[station_id].downlink_response = station_data
                # Consume the network bandwidth in the base station.
                self._base_stations[station_id].use_wired_for_downlink()
