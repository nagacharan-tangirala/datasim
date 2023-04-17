from mesa import Agent, Model


class BAgent(Agent):
    def __init__(self, params: dict, sensors: dict, model: Model = None):
        """
        Initialize the entity agent.
        """
        super().__init__(params['id'], model)

        # Get the start and end time of the agent
        self.start_time = params['start_time']
        self.end_time = params['end_time']

        self.sensors = sensors
        self.active = False

    def step(self):
        """
        Step function for the agent.
        """
        # Check if the agent is active
        if not self.active:
            return

    def get_start_time(self) -> int:
        """
        Get the start time of the agent.
        """
        return self.start_time

    def get_end_time(self) -> int:
        """
        Get the end time of the agent.
        """
        return self.end_time

    def schedule_activation(self, start_time: int):
        """
        Activate the agent at a start time.
        """
        self.model.schedule.add(self)
        self.active = True

    def schedule_deactivation(self, end_time: int):
        """
        Deactivate the agent at end time.
        """
        self.model.schedule.remove(self)
        self.active = False
