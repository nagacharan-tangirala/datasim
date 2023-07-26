from mesa import Agent
from pandas import DataFrame

from src.application.Payload import VehiclePayload, VehicleResponse
from src.device.BaseStation import BaseStation
from src.device.VehicleUE import VehicleUE
from src.models.ModelFactory import ModelFactory
from src.models.finder.BaseStationFinder import BaseStationFinder


class EdgeOrchestrator(Agent):
    def __init__(self,
                 base_stations: dict,
                 vehicle_links_df: DataFrame,
                 base_station_links_df: DataFrame,
                 model_data: dict):
        """
        Initialize the edge orchestrator.

        Parameters
        ----------
        base_stations : dict[int, BaseStation]
            The base stations in the network.
        vehicle_links_df : DataFrame
            The links between the vehicles and the base stations.
        base_station_links_df : DataFrame
            The links between the base stations.
        model_data : dict
            The model data.
        """
        super().__init__(0, None)

        self._vehicles: dict[int, VehicleUE] = {}
        self._base_stations: dict[int, BaseStation] = base_stations

        self._vehicle_links: DataFrame = vehicle_links_df
        self._base_station_links: DataFrame = base_station_links_df

        self._base_station_finder: BaseStationFinder | None = None

        # Uplink data generated at the vehicles
        self.data_at_vehicles: dict[int, VehiclePayload] = {}

        # Uplink vehicle data along with the target base stations
        self.uplink_vehicle_data: dict[int, dict[int, VehiclePayload]] = {}

        # Downlink data arrived at the base stations from the controllers
        self.downlink_response_at_basestations: dict[int, dict[int, VehicleResponse]] = {}

        self._current_time: int = -1

        # Create the models
        self._create_models(model_data)

    @property
    def current_time(self) -> int:
        """Get the time stamp."""
        return self._current_time

    @current_time.setter
    def current_time(self, value: int) -> None:
        """ Set the current time."""
        self._current_time = value

    def add_vehicle(self, vehicle: VehicleUE) -> None:
        """
        Add a new vehicle.
        """
        self._vehicles[vehicle.unique_id] = vehicle

    def remove_vehicle(self, vehicle_id: int) -> None:
        """
        Remove the vehicle.
        """
        self._vehicles.pop(vehicle_id)

    def add_base_station(self, base_station: BaseStation) -> None:
        """
        Add a new base station.
        """
        self._base_stations[base_station.unique_id] = base_station

    def remove_base_station(self, base_station_id: int) -> None:
        """
        Remove the base station.
        """
        self._base_stations.pop(base_station_id)

    def update_v2v_links(self, v2v_links: DataFrame) -> None:
        """
        Update the V2V links.
        """
        self._vehicle_links = v2v_links

    def update_v2b_links(self, v2b_links: DataFrame) -> None:
        """
        Update the V2B links.
        """
        self._base_station_links = v2b_links

    def _create_models(self, model_data: dict):
        """
        Create the models
        """
        model_factory = ModelFactory()
        self._base_station_finder = model_factory.create_basestation_finder(self._base_stations,
                                                                            self._base_station_links,
                                                                            model_data['base_station_finder'])

    def uplink_stage(self) -> None:
        """
        Step through the orchestration process for the uplink stage.
        This is the second step in the overall simulation.
        """
        # Step through the models.
        self._base_station_finder.current_time = self.current_time

        # Collect data from each vehicle
        self._collect_data_from_vehicles()

        # Find target base stations
        self._assign_target_basestations()

        # Send data to base stations
        self._send_data_to_basestations()

    def _collect_data_from_vehicles(self):
        """
        Send data from the vehicles to the base stations.
        """
        self.data_at_vehicles.clear()
        for vehicle_id, vehicle in self._vehicles.items():
            self.data_at_vehicles[vehicle_id] = vehicle.uplink_payload
            # Consume the network bandwidth in the vehicle.
            vehicle.use_network_for_uplink()

    def _assign_target_basestations(self) -> None:
        """
        Find the base stations for the vehicles.
        """
        # Prepare a dictionary with the payloads to send.
        self.uplink_vehicle_data.clear()
        for vehicle_id, vehicle_data in self.data_at_vehicles.items():
            # Find the base station for the vehicle
            base_station_ids = self._base_station_finder.select_n_base_stations_for_vehicle(vehicle_id, 1)
            base_station_id = base_station_ids[0]

            if base_station_id not in self.uplink_vehicle_data:
                self.uplink_vehicle_data[base_station_id] = {}
            self.uplink_vehicle_data[base_station_id][vehicle_id] = vehicle_data

    def _send_data_to_basestations(self) -> None:
        """
        Send data to the base stations.
        """
        for base_station_id, vehicle_data in self.uplink_vehicle_data.items():
            self._base_stations[base_station_id].set_uplink_vehicle_data(vehicle_data)
            # Consume the wireless network bandwidth in the base station.
            self._base_stations[base_station_id].use_wireless_for_uplink()

    def downlink_stage(self) -> None:
        """
        Step through the orchestration process for the downlink stage.
        """
        # Collect data from each base station
        self._collect_data_from_basestations()

        # Send data to vehicles
        self._send_data_to_vehicles()

    def _collect_data_from_basestations(self):
        """
        Collect data from the base stations.
        """
        self.downlink_response_at_basestations.clear()
        for base_station_id, base_station in self._base_stations.items():
            self.downlink_response_at_basestations[base_station_id] = base_station.downlink_vehicle_data
            # Consume the wireless network bandwidth in the base station.
            base_station.use_wireless_for_downlink()

    def _send_data_to_vehicles(self):
        """
        Send data to the vehicles.
        """
        for base_station_id, base_station_data in self.downlink_response_at_basestations.items():
            for vehicle_id, veh_data in base_station_data:
                self._vehicles[vehicle_id].downlink_response = veh_data
                # Consume the network bandwidth in the vehicle.
                self._vehicles[vehicle_id].use_network_for_downlink()
