import pandas as pd

from src.device.DBasicCellTower import BaseStation
from src.device.DCentralController import CentralController
from src.device.DIntermediateCellTower import IntermediateCellTower
from src.device.DVehicleUE import VehicleUE


class DeviceFactory:
    def __init__(self):
        """
        Initialize the device factory object.
        """
        # Create the dictionaries to store the devices in the simulation
        self.nodes = {}
        self.agents = {}
        self.controllers = {}

    def get_cell_towers(self) -> dict:
        """
        Get the nodes in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the nodes.
        """
        return self.nodes

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
        Get the agents in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the agents.
        """
        return self.agents

    def create_cell_towers(self, all_nodes_data: pd.DataFrame):
        """
        Create the nodes in the simulation.
        """
        # Get the list of nodes in the simulation.
        node_list = all_nodes_data['node_id'].unique()

        # Create the nodes.
        for node_id in node_list:
            # Get the node data.
            node_data: pd.Series = all_nodes_data[all_nodes_data['node_id'] == node_id].iloc[0]

            # Create the node.
            self.nodes[node_id] = self._create_node(node_id, node_data)

    @staticmethod
    def _create_node(node_id: int, node_data: pd.Series):
        """
        Create a node from the given parameters.
        """
        node_type = node_data['type']
        if node_type == 'bs':
            return BaseStation(node_id, node_data)
        elif node_type == 'intermediate':
            return IntermediateCellTower(node_id, node_data)
        else:
            raise ValueError("Node {} type not supported.".format(node_type))

    def create_controllers(self, controller_data: pd.DataFrame):
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

    def create_ues(self, agent_data: pd.DataFrame, coverage_data: pd.DataFrame):
        """
        Create the agents in the simulation.
        """
        # Get the list of agents in the simulation.
        agent_list = agent_data['agent_id'].unique()

        # Create the agents.
        for agent_id in agent_list:
            # Get the agent positions.
            agent_trace = agent_data[agent_data['agent_id'] == agent_id][['time', 'x', 'y']].reset_index(drop=True)

            # Create the agent.
            self.agents[agent_id] = self._create_agent(agent_id)

            # Set the agent trace.
            self.agents[agent_id].set_mobility_data(agent_trace)

            # Get the agent coverage.
            agent_coverage = coverage_data[coverage_data['vehicle_id'] == agent_id][['neighbours', 'time']]

            # Set the agent coverage.
            self.agents[agent_id].set_coverage_data(agent_coverage)

    @staticmethod
    def _create_agent(agent_id: int) -> VehicleUE:
        """
        Create an agent from the given parameters.

        Parameters
        ----------
        agent_id : int
            The ID of the agent.
        """
        return VehicleUE(agent_id)
