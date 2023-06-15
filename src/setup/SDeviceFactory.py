from pandas import DataFrame, Series

from src.device.DBasicCellTower import BasicCellTower
from src.device.DCentralController import CentralController
from src.device.DIntermediateCellTower import IntermediateCellTower
from src.device.DVehicleUE import VehicleUE


class DeviceFactory:
    def __init__(self):
        """
        Initialize the device factory object.
        """
        # Create the dictionaries to store the devices in the simulation
        self.cell_towers = {}
        self.ues = {}
        self.controllers = {}

    def get_cell_towers(self) -> dict:
        """
        Get the cell towers in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the cell_tower.
        """
        return self.cell_towers

    def get_controllers(self) -> dict:
        """
        Get the controllers in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the controllers.
        """
        return self.controllers

    def get_ues(self) -> dict:
        """
        Get the ues in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the ues.
        """
        return self.ues

    def create_cell_towers(self, all_cell_tower_data: DataFrame):
        """
        Create the cell towers in the simulation.
        """
        # Get the list of cell towers in the simulation.
        cell_tower_list = all_cell_tower_data['cell_tower_id'].unique()

        for cell_tower_id in cell_tower_list:
            # Get the cell tower data.
            cell_tower_data: Series = all_cell_tower_data[all_cell_tower_data['cell_tower_id'] == cell_tower_id].iloc[0]

            # Create the cell tower.
            self.cell_tower[cell_tower_id] = self._create_cell_tower(cell_tower_id, cell_tower_data)

    @staticmethod
    def _create_cell_tower(cell_tower_id: int, cell_tower_data: Series):
        """
        Create a cell tower from the given parameters.
        """
        cell_tower_type = cell_tower_data['type']
        if cell_tower_type == 'bs':
            return BasicCellTower(cell_tower_id, cell_tower_data)
        elif cell_tower_type == 'intermediate':
            return IntermediateCellTower(cell_tower_id, cell_tower_data)
        else:
            raise ValueError("cell_tower {} type not supported.".format(cell_tower_type))

    def create_controllers(self, controller_data: DataFrame):
        """
        Create the controllers in the simulation.
        """
        # Get the list of controllers in the simulation.
        controller_list = controller_data['controller_id'].unique()

        # Create the controllers.
        for controller_id in controller_list:
            # Get the controller position.
            controller_position: list[float, float] = controller_data[controller_data['controller_id'] == controller_id][['x', 'y']].values.tolist()

            # Create the controller.
            self.controllers[controller_id] = self._create_controller(controller_id, controller_position)

    @staticmethod
    def _create_controller(controller_id, position) -> CentralController:
        """
        Create a controller from the given parameters.

        Parameters
        ----------
        controller_id : int
            The ID of the controller.
        position : list[float]
            The position of the controller.
        """
        return CentralController(controller_id, position)

    def create_ues(self, ue_data: DataFrame, coverage_data: DataFrame):
        """
        Create the ues in the simulation.
        """
        # Get the list of ues in the simulation.
        ue_list = ue_data['ue_id'].unique()

        # Create the ues.
        for ue_id in ue_list:
            # Get the ue positions.
            ue_trace = ue_data[ue_data['ue_id'] == ue_id][['time', 'x', 'y']].reset_index(drop=True)

            # Create the ue.
            self.ues[ue_id] = self._create_ue(ue_id)

            # Set the ue trace.
            self.ues[ue_id].set_mobility_data(ue_trace)

            # Get the ue coverage.
            ue_coverage = coverage_data[coverage_data['vehicle_id'] == ue_id][['neighbours', 'time']]

            # Set the ue coverage.
            self.ues[ue_id].set_coverage_data(ue_coverage)

    @staticmethod
    def _create_ue(ue_id: int) -> VehicleUE:
        """
        Create an ue from the given parameters.

        Parameters
        ----------
        ue_id : int
            The ID of the ue.
        """
        return VehicleUE(ue_id)
