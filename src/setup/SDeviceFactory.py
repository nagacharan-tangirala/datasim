import pandas as pd

from src.setup.SAgentFactory import AgentFactory
from src.setup.SControllerFactory import ControllerFactory
from src.setup.SNodeFactory import NodeFactory


class DeviceFactory:
    def __init__(self):
        """
        Initialize the device factory object.
        """
        # Create the factories needed to create the devices.
        self._node_factory = NodeFactory()
        self._device_factory = AgentFactory()
        self._controller_factory = ControllerFactory()

        # Create the dictionaries to store the devices in the simulation
        self.nodes = {}
        self.agents = {}
        self.controllers = {}

    def get_nodes(self) -> dict:
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

    def get_agents(self) -> dict:
        """
        Get the agents in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the agents.
        """
        return self.agents

    def create_nodes(self, node_data: pd.DataFrame):
        """
        Create the nodes in the simulation.
        """
        for node_id, node_params in node_data.iterrows():
            self.nodes[node_id] = self._node_factory.create_node(node_id, node_params)

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
            self.controllers[controller_id] = self._controller_factory.create_controller(controller_id, controller_position)

    def create_agents(self, agent_data: pd.DataFrame, coverage_data: pd.DataFrame):
        """
        Create the agents in the simulation.
        """
        # Get the list of agents in the simulation.
        agent_list = agent_data['agent_id'].unique()

        # Create the agents.
        for agent_id in agent_list:
            # Get the agent positions.
            agent_trace = agent_data[agent_data['agent_id'] == agent_id][['time', 'x', 'y']].values.tolist()

            # Create the agent.
            self.agents[agent_id] = self._device_factory.create_agent(agent_id)

            # Set the agent trace.
            self.agents[agent_id].set_mobility_data(agent_trace)

            # Get the agent coverage.
            agent_coverage = coverage_data[coverage_data['agent_id'] == agent_id][['coverage', 'time_step']]

            # Set the agent coverage.
            self.agents[agent_id].set_coverage_data(agent_coverage)
