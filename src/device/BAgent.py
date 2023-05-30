from abc import abstractmethod

from mesa import Agent
from collections import deque


class AgentBase(Agent):
    def __init__(self, params: dict, sensor_params: dict, sim_model=None):
        """
        Initialize the agent.
        """
        super().__init__(params['id'], sim_model)
        self.sim_model = sim_model

        # Get the positions
        self.positions = params['positions']

        # Get the start and end time of the agent
        self.start_time = params['start_time']
        self.end_time = params['end_time']

        self.total_data = 0

        self.sensor_params = sensor_params
        self.active = False

        self.data_cache = deque(maxlen=3)
        self.data_cache.append(0)

    @abstractmethod
    def step(self):
        """
        Step function for the agent.
        """
        pass

    def toggle_status(self, model):
        """
        Toggle the active status of the agent.
        """
        # Toggle the status
        self.active = not self.active

        if self.active:
            # Assign the model to the agent and add the agent to the scheduler of the model
            self.sim_model = model
            self.sim_model.schedule.add(self)

            # Initiate the models
            self._initiate_models()
        else:
            # Remove the agent from the scheduler of the model
            self.sim_model.schedule.remove(self)

            # Deactivate the models
            self._deactivate_models()

    @abstractmethod
    def _initiate_models(self):
        """
        Initiate the models related to this agent.
        """
        pass

    @abstractmethod
    def _deactivate_models(self):
        """
        Deactivate the models related to this agent.
        """
        pass

    def get_start_and_end_time(self) -> tuple[int, int]:
        """
        Get the start and end time of the agent.
        """
        return self.start_time, self.end_time

    def get_cached_data(self):
        """
        Get the data cached by the agent.
        """
        return self.data_cache.pop()
