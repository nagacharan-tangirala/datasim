from abc import abstractmethod

from mesa import Agent

from src.device.BUE import BaseUE
from src.device.BCellTower import BaseCellTower


class BaseUEChannel(Agent):
    def __init__(self):
        super().__init__(0, None)
        self.agents: dict[int, BaseUE] = {}
        self.nodes: dict[int, BaseCellTower] = {}

        self.node_agents: dict[int, list[int]] = {}
        self.data_from_agents: dict[int, float] = {}

        self.current_time: int = 0

    def set_current_time(self, current_time: int) -> None:
        """
        Set the current time.
        """
        self.current_time = current_time

    def step(self, *args, **kwargs) -> None:
        """
        Step through the agent channel.
        """
        # Assert that nodes are assigned to the channel
        assert len(self.nodes) > 0, "No nodes assigned to the channel."

        if len(self.agents) is 0:
            return

        # Send data to neighboring agents
        self._send_data_to_neighbours()

        # Collect data from each agent
        self._collect_data_from_agents()

        # Send data to the respective nodes
        self._send_data_to_nodes()

    def _find_nearest_node(self, agent_id: int) -> int:
        """
        Find the nearest node to each agent.
        """
        # Get the agent's position
        agent_position = self.agents[agent_id].get_position()

        # Find the nearest node
        nearest_node_id = None
        nearest_node_distance = None
        for node_id, node in self.nodes.items():
            # Get the node's position
            node_position = node.get_position()

            # Calculate distance between the agent and the node
            distance = self._get_distance(agent_position, node_position)

            # Update the nearest node
            if nearest_node_id is None or distance < nearest_node_distance:
                nearest_node_id = node_id
                nearest_node_distance = distance

        return nearest_node_id

    def _collect_data_from_agents(self):
        """
        Collect data from each agent.
        """
        for agent_id, agent in self.agents.items():
            # Get the nearest node to the agent
            nearest_node_id = self._find_nearest_node(agent_id)

            # Store the node ID
            if nearest_node_id not in self.node_agents:
                self.node_agents[nearest_node_id] = []
            self.node_agents[nearest_node_id].append(agent_id)

            # Get the data from the agent
            self.data_from_agents[agent_id] = agent.get_data()

    @staticmethod
    def _get_distance(position1: list[float], position2: list[float]):
        """
        Get the distance between two positions.
        """
        # Calculate distance between the agent and the node
        distance = 0
        for i in range(len(position1)):
            distance += (position1[i] - position2[i]) ** 2
        distance = distance ** 0.5

        return distance

    @abstractmethod
    def _send_data_to_nodes(self):
        """
        Send data to the respective nodes.
        """
        pass

    @abstractmethod
    def _send_data_to_neighbours(self):
        """
        Send data to neighboring agents.
        """
        pass

    def assign_nodes(self, nodes: dict[int, BaseCellTower]) -> None:
        """
        Add a node to the channel.
        """
        self.nodes = nodes

    def add_agent(self, agent: BaseUE) -> None:
        """
        Add an agent to the channel.
        """
        self.agents[agent.get_id()] = agent

    def remove_agent(self, agent: BaseUE) -> None:
        """
        Remove an agent from the channel.
        """
        self.agents.pop(agent.get_id())
