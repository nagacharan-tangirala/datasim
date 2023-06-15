from src.channel.BUEChannel import BaseUEChannel


class InfiniteBandwidthUEChannel(BaseUEChannel):
    def __init__(self):
        super().__init__()

    def _send_data_to_nodes(self):
        """
        Send data to the respective nodes.
        """
        # Send as much data as the bandwidth allows.
        for node_id, agents in self.node_agents.items():
            for agent_id in agents:
                # Get the data from the agent
                data = self.data_from_agents[agent_id]

                # TODO: Add bandwidth, losses, quantization, etc. to the channel.

                # Send the data to the node
                self.nodes[node_id].receive_data(agent_id, data)

                # Tell the agent that the data has been sent
                self.agents[agent_id].set_data_transmit_status(True)

    def _send_data_to_neighbours(self):
        """
        Send data to neighbouring agents.
        """
        # TODO: Complete this function.
        # Whoever failed to send data in the previous time step, send it now.
        for agent_id, agent in self.agents.items():
            # Get the neighbouring agents data
            data = agent.get_neighbour_data()

            if len(data) is 0:
                continue

            # Send the data to the neighbouring agents
            for neighbour_id, neighbour_data in data.items():
                # Get the data from the agent
                data = self.data_from_agents[agent_id]
