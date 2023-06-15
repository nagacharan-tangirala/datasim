from abc import abstractmethod

from mesa import Agent
from pandas import DataFrame

from src.device.BCellTower import BaseCellTower


class BaseControllerChannel(Agent):
    def __init__(self, controller_links: DataFrame):
        super().__init__(0, None)

        self.controller_links = controller_links
        self.cell_tower_to_controller = {}
        self.cell_towers: dict = {}

        self.incoming_data: dict = {}

    def assign_cell_towers(self, cell_towers: dict[int, BaseCellTower]) -> None:
        """
        Add a cell tower to the channel.
        """
        # Add the cell towers to the channel
        self.cell_towers = cell_towers

        # Read the controller links
        self._read_controller_links()

    def _read_controller_links(self) -> None:
        """
        Read the controller links.
        """
        # Based on the controller links, assign cell towers to the controller
        for _, row in self.controller_links.iterrows():
            # Get the cell tower ID
            cell_tower_id = row['cell_tower']

            # Add the cell tower to the controller
            self.cell_tower_to_controller[cell_tower_id] = row['controller']

    @abstractmethod
    def _collect_from_cell_towers(self):
        """
        Collect data from the cell towers.
        """
        pass

    @abstractmethod
    def _send_to_controller(self):
        """
        Send data to the controller.
        """
        pass

    def step(self) -> None:
        """
        Step through the controller channel.
        """
        # Collect data from the cell towers
        self._collect_from_cell_towers()

        # Send data to the controller
        self._send_to_controller()
