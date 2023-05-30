from mesa import Model
from mesa.time import BaseScheduler
from src.device.BAgent import AgentBase


class AgentModel(Model):
    def __init__(self, sim_params: dict, agents: dict[int, AgentBase]):
        """
        Initialize the ABM model.
        """
        super().__init__()

        # Get the simulation parameters
        self.start_time = sim_params['start'] * 3600 * 1000
        self.end_time = sim_params['end'] * 3600 * 1000
        self.time_step = sim_params['step']

        self.seed = sim_params['seed']
        self.update_step = sim_params['update_step']
        self.output_dir = sim_params['output_dir']
        self.output_step = sim_params['output_step']

        self.current_time = self.start_time

        # Override the default scheduler
        self.schedule = BaseScheduler(self)

        self.agents: dict[int, AgentBase] = agents
        self.agent_activation_times: dict[int, list[int]] = {}

        self._prepare_active_agents_dict()

    def _prepare_active_agents_dict(self):
        """
        Prepare a dictionary with time step as the key and the respective agents to activate in that time step.
        """
        for agent_id, agent in self.agents.items():
            start_time, end_time = agent.get_start_and_end_time()
            # Add the agent to the dictionary with the start time as the key
            if start_time not in self.agent_activation_times:
                self.agent_activation_times[start_time] = [agent_id]
            else:
                self.agent_activation_times[start_time].append(agent_id)

            # Add the agent to the dictionary with the end time as the key
            if end_time not in self.agent_activation_times:
                self.agent_activation_times[end_time] = [agent_id]
            else:
                self.agent_activation_times[end_time].append(agent_id)

    def _refresh_active_agents(self, time_step: int):
        """
        If the start or end time of an agent is equal to the current time step, activate or deactivate the agent.

        Parameters
        ----------
        time_step : int
            The time step of the simulation.
        """
        agents_to_update = self.agent_activation_times[time_step]
        for agent_id in agents_to_update:
            agent = self.agents[agent_id]
            agent.toggle_status(self)

    def step(self):
        """
        Step function for the model.
        """
        # Refresh the active agents
        if self.current_time in self.agent_activation_times:
            self._refresh_active_agents(self.current_time)

        # Step through the schedule object
        self.schedule.step()
        self.current_time += self.time_step

    def run(self):
        """
        Run the model until the end time.
        """
        while self.current_time <= self.end_time:
            print(f"Current time: {self.current_time}")
            self.step()
