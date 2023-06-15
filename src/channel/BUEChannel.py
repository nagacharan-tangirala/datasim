from abc import abstractmethod

from mesa import Agent

from src.device.BUE import BaseUE
from src.device.BCellTower import BaseCellTower


class BaseUEChannel(Agent):
    def __init__(self):
        super().__init__(0, None)
        self.ues: dict[int, BaseUE] = {}
        self.cell_towers: dict[int, BaseCellTower] = {}

        self.cell_tower_coverage_ues: dict[int, list[int]] = {}
        self.data_from_ues: dict[int, float] = {}

        self.current_time: int = 0

    def set_current_time(self, current_time: int) -> None:
        """
        Set the current time.
        """
        self.current_time = current_time

    def step(self, *args, **kwargs) -> None:
        """
        Step through the ue channel.
        """
        # Assert that cell towers are assigned to the channel
        assert len(self.cell_towers) > 0, "No cell_towers assigned to the channel."

        if len(self.ues) is 0:
            return

        # Send data to neighboring ues
        self._send_data_to_neighbours()

        # Collect data from each ue
        self._collect_data_from_ues()

        # Send data to the respective cell towers
        self._send_data_to_cell_towers()

        # Receive data from the respective cell towers
        self._receive_data_from_cell_towers()

        # Send data to the respective ues
        self._send_data_to_ues()

    def _find_nearest_cell_tower(self, ue_id: int) -> int:
        """
        Find the nearest cell_tower to each ue.
        """
        # Get the ue's position
        ue_position = self.ues[ue_id].get_position()

        # Find the nearest cell_tower
        nearest_cell_tower_id = None
        nearest_cell_tower_distance = None
        for cell_tower_id, cell_tower in self.cell_towers.items():
            # Get the cell_tower's position
            cell_tower_position = cell_tower.get_position()

            # Calculate distance between the ue and the cell tower
            distance = self._get_distance(ue_position, cell_tower_position)

            # Update the nearest cell_tower
            if nearest_cell_tower_id is None or distance < nearest_cell_tower_distance:
                nearest_cell_tower_id = cell_tower_id
                nearest_cell_tower_distance = distance

        return nearest_cell_tower_id

    def _collect_data_from_ues(self):
        """
        Collect data from each ue.
        """
        for ue_id, ue in self.ues.items():
            # Get the nearest cell_tower to the ue
            nearest_cell_tower_id = self._find_nearest_cell_tower(ue_id)

            # Store the cell_tower ID
            if nearest_cell_tower_id not in self.cell_tower_coverage_ues:
                self.cell_tower_coverage_ues[nearest_cell_tower_id] = []
            self.cell_tower_coverage_ues[nearest_cell_tower_id].append(ue_id)

            # Get the data from the ue
            self.data_from_ues[ue_id] = ue.get_data()

    @staticmethod
    def _get_distance(position1: list[float], position2: list[float]):
        """
        Get the distance between two positions.
        """
        # Calculate distance between the ue and the cell tower
        distance = 0
        for i in range(len(position1)):
            distance += (position1[i] - position2[i]) ** 2
        distance = distance ** 0.5

        return distance

    @abstractmethod
    def _send_data_to_cell_towers(self):
        """
        Send data to the respective cell towers.
        """
        pass

    @abstractmethod
    def _send_data_to_neighbours(self):
        """
        Send data to neighboring ues.
        """
        pass

    @abstractmethod
    def _receive_data_from_cell_towers(self):
        """
        Receive data from the respective cell towers.
        """
        pass

    @abstractmethod
    def _send_data_to_ues(self):
        """
        Send data to the respective ues.
        """
        pass

    def assign_cell_towers(self, cell_towers: dict[int, BaseCellTower]) -> None:
        """
        Add a cell tower to the channel.
        """
        self.cell_towers = cell_towers

    def add_ue(self, ue: BaseUE) -> None:
        """
        Add an ue to the channel.
        """
        self.ues[ue.get_id()] = ue

    def remove_ue(self, ue: BaseUE) -> None:
        """
        Remove an ue from the channel.
        """
        self.ues.pop(ue.get_id())
