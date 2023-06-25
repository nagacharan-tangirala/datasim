from random import choices

from pandas import DataFrame, Series

from src.core.CustomExceptions import NotSupportedCellTowerError
from src.device.BUE import BaseUE
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
        self.cell_towers: dict[int, BasicCellTower] = {}
        self.ues: dict[int, BaseUE] = {}
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

    def create_cell_towers(self, cell_tower_data: DataFrame, cell_tower_models_data: dict) -> None:
        """
        Create the cell towers in the simulation.
        """
        # Get the list of cell towers in the simulation.
        cell_tower_list = cell_tower_data['cell_tower_id'].unique()

        for cell_tower_id in cell_tower_list:
            # Get the cell tower data.
            cell_tower_data: Series = cell_tower_data[cell_tower_data['cell_tower_id'] == cell_tower_id].iloc[0]

            # Create the cell tower.
            self.cell_towers[cell_tower_id] = self._create_cell_tower(cell_tower_id, cell_tower_data, cell_tower_models_data)

    @staticmethod
    def _create_cell_tower(cell_tower_id: int, cell_tower_data: Series, cell_tower_models_data: dict):
        """
        Create a cell tower from the given parameters.
        """
        cell_tower_type = cell_tower_data['type']
        if cell_tower_type == 'bs':
            return BasicCellTower(cell_tower_id, cell_tower_data, cell_tower_models_data)
        elif cell_tower_type == 'intermediate':
            return IntermediateCellTower(cell_tower_id, cell_tower_data, cell_tower_models_data)
        else:
            raise NotSupportedCellTowerError(cell_tower_type)

    def create_controllers(self, controller_data: DataFrame, controller_models_data: dict) -> None:
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
            self.controllers[controller_id] = self._create_controller(controller_id, controller_position, controller_models_data)

    @staticmethod
    def _create_controller(controller_id, position, controller_models_data) -> CentralController:
        """
        Create a controller from the given parameters.

        Parameters
        ----------
        controller_id : int
            The ID of the controller.
        position : list[float]
            The position of the controller.
        """
        return CentralController(controller_id, position, controller_models_data)

    def create_ues(self, ue_trace_data: DataFrame, ue_models: dict) -> None:
        """
        Create the ues in the simulation.
        """
        # Get the list of ues in the simulation.
        ue_list = ue_trace_data['vehicle_id'].unique()

        # Get the weights of the ue types.
        ue_weights = [float(ue_data['weight']) for ue_data in ue_models.values()]
        ue_types = list(ue_models.keys())

        # Create the ues.
        for ue_id in ue_list:
            # Randomly select the type of the ue and get the respective model set.
            ue_type_choice = choices(ue_types, weights=ue_weights, k=1)[0]
            selected_ue_model_set = ue_models[ue_type_choice].copy()

            # Create the ue.
            self.ues[ue_id] = self._create_ue(ue_id, selected_ue_model_set)

            # Update the ue trace data.
            this_ue_trace: DataFrame = ue_trace_data[ue_trace_data['vehicle_id'] == ue_id]
            self.ues[ue_id].update_mobility_data(this_ue_trace)

    @staticmethod
    def _create_ue(ue_id: int, ue_models: dict) -> VehicleUE:
        """
        Create an ue from the given parameters.

        Parameters
        ----------
        ue_id : int
            The ID of the ue.
        """
        return VehicleUE(ue_id, ue_models)

    def update_ues(self, ue_trace_data: DataFrame, ue_models: dict) -> None:
        """
        Update the ues based on the new trace data.
        """
        ue_list = ue_trace_data['vehicle_id'].unique()

        # Get the weights of the ue types.
        ue_weights = [float(ue_data['weight']) for ue_data in ue_models.values()]
        ue_types = list(ue_models.keys())

        for ue_id in ue_list:
            this_ue_trace: DataFrame = ue_trace_data[ue_trace_data['vehicle_id'] == ue_id]
            if ue_id in self.ues:
                # Already exists, update the trace data.
                self.ues[ue_id].update_mobility_data(this_ue_trace)
                continue

            # Randomly select the type of the ue and get the respective model set.
            ue_type_choice = choices(ue_types, weights=ue_weights, k=1)[0]
            selected_ue_model_set = ue_models[ue_type_choice].copy()

            # Create the ue and update the trace data.
            self.ues[ue_id] = self._create_ue(ue_id, selected_ue_model_set)
            self.ues[ue_id].update_mobility_data(this_ue_trace)

    def update_cell_towers(self, cell_tower_data: DataFrame, cell_tower_models_data: dict) -> None:
        """
        Update the cell towers based on the new trace data.
        """
        # Get the list of cell towers in the simulation.
        cell_tower_list = cell_tower_data['cell_tower_id'].unique()

        for cell_tower_id in cell_tower_list:
            if cell_tower_id in self.cell_towers:
                # TODO: Update the cell tower if there is any requirement to do so. Currently, there is no requirement. All the cell tower data is static in the simulation.
                continue

            # Get the cell tower data.
            cell_tower_data: Series = cell_tower_data[cell_tower_data['cell_tower_id'] == cell_tower_id].iloc[0]

            # Create the cell tower.
            self.cell_towers[cell_tower_id] = self._create_cell_tower(cell_tower_id, cell_tower_data, cell_tower_models_data)

    def update_controllers(self, controller_data: DataFrame, controller_models_data: dict) -> None:
        """
        Update the controllers based on the new trace data.
        """
        # Get the list of controllers in the simulation.
        controller_list = controller_data['controller_id'].unique()

        for controller_id in controller_list:
            if controller_id in self.controllers:
                # TODO: Update the controller if there is any requirement to do so. Currently, there is no requirement. All the controller data is static in the simulation.
                continue

            # Get the controller position.
            controller_position: list[float, float] = controller_data[controller_data['controller_id'] == controller_id][['x', 'y']].values.tolist()

            # Create the controller.
            self.controllers[controller_id] = self._create_controller(controller_id, controller_position, controller_models_data)
