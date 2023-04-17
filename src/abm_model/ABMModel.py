from mesa import Model
from mesa.time import BaseScheduler
from src.device.BAgent import BAgent


class ABMModel(Model):
    def __init__(self, sim_params: dict, agents: dict[int, BAgent]):
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
        self.schedule = BaseScheduler(self)

        self.agents: dict[int, BAgent] = agents

        # Schedule the agents
        self.schedule_agent_activation()
        self.schedule_agent_deactivation()

    def schedule_agent_activation(self):
        """
        Schedule the agents for activation.
        """
        for agent in self.agents.values():
            agent.model = self
            agent.schedule_activation(agent.get_start_time())

    def schedule_agent_deactivation(self):
        """
        Schedule the agents for deactivation.
        """
        for agent in self.agents.values():
            agent.model = self
            agent.schedule_deactivation(agent.get_end_time())

    def step(self):
        """
        Step function for the model.
        """
        self.schedule.step()
        self.current_time += self.time_step

    def run(self):
        """
        Run the model until the end time.
        """
        while self.current_time <= self.end_time:
            print(f"Current time: {self.current_time}")
            self.step()
