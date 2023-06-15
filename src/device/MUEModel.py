from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BUEChannel import BaseUEChannel
from src.device.BUE import BaseUE
from src.setup.SDeviceModelFactory import DeviceModelFactory


class UEModel(Model):
    def __init__(self, agents: dict[int, BaseUE], agent_model_data: dict):
        """
        Initialize the model for the agents.
        """
        # Override the default scheduler
        super().__init__()
        self.schedule: BaseScheduler = BaseScheduler(self)

        self.agents: dict[int, BaseUE] = agents
        self.agent_activation_times: dict[int, list[int]] = {}

        self.current_time: int = 0

        # All models are defined here
        self.agent_channel: BaseUEChannel = None

        self._prepare_active_agents_dict()
        self._create_models(agent_model_data)

    def _prepare_active_agents_dict(self) -> None:
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

    def _create_models(self, agent_model_data: dict) -> None:
        """
        Create all the models for the agents.
        """
        # Iterate through the model data and create the models
        model_factory = DeviceModelFactory()
        for model_id, model_data in agent_model_data.items():
            if model_data['type'] == 'channel':
                self.agent_channel = model_factory.create_agent_channel(model_data)
            else:
                raise ValueError(f"Unknown model type {model_data['type']}")

    def get_agent_channel(self) -> BaseUEChannel | None:
        """
        Get the channel for the agent model.
        """
        return self.agent_channel

    def _refresh_active_agents(self, time_step: int) -> None:
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
            agent.toggle_status()

            # If the agent is active, add it to the scheduler and channel. Otherwise, remove from them.
            if agent.is_active():
                self.schedule.add(agent)
                self.agent_channel.add_agent(agent)
                agent.sim_model = self
            else:
                self.schedule.remove(agent)
                self.agent_channel.remove_agent(agent)
                agent.sim_model = None

    def step(self, *args, **kwargs):
        """
        Step function for the model.
        """
        # Refresh the active agents
        current_time = int(args[0])
        if current_time in self.agent_activation_times:
            self._refresh_active_agents(current_time)

        # Step through the schedule object
        self.schedule.step()
