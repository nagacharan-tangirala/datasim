from mesa import Agent

from src.device.ComputingHardware import ComputingHardware
from src.device.NetworkHardware import NetworkHardware


class RoadSideUnitUE(Agent):
    def __init__(self,
                 rsu_id: int,
                 hardware_settings: ComputingHardware,
                 network_settings: NetworkHardware):
        """
        Initialize the rsu.
        """
        super().__init__(rsu_id, None)

        self._hardware_settings: ComputingHardware = hardware_settings
        self._network_settings: NetworkHardware = network_settings
