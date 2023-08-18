from dataclasses import dataclass

from mesa import Agent, Model
from mesa.time import BaseScheduler


@dataclass
class TypeStage:
    type: type[Agent]
    stage: str


class OrderedMultiStageScheduler(BaseScheduler):
    def __init__(
        self,
        model: Model,
        type_stage_list: list[TypeStage] | None = None,
        shuffle: bool = False,
    ) -> None:
        """
        Create an ordered multi-stage scheduler.

        Parameters
        ----------
        model : Model
            Model object associated with the schedule.
        type_stage_list : list[str] | None, optional
            List of types and their respective stages to run, in the order to run them in, by default None
        shuffle : bool, optional
            If True, shuffle the order of agents within each step, by default False. This does not shuffle the order of
            the stages and the types.
        """
        super().__init__(model)
        self.types_with_stages: list[TypeStage] = (
            type_stage_list if type_stage_list else []
        )
        self.shuffle = shuffle
        self.stage_time = 1 / len(self.types_with_stages)
        self.agents_by_type: dict[type[Agent], dict[int, Agent]] = {}
        for type_stage in self.types_with_stages:
            self.agents_by_type[type_stage.type] = {}

    def add(self, agent: Agent) -> None:
        """
        Adds an agent to the schedule.

        Parameters
        ----------
        agent : Agent
            An Agent to be added to the schedule.
        """
        super().add(agent)
        agent_class: type[Agent] = type(agent)
        self.agents_by_type[agent_class][agent.unique_id] = agent

    def remove(self, agent: Agent) -> None:
        """
        Removes all instances of a given agent from the schedule.

        Parameters
        ----------
        agent : Agent
            The agent to remove.
        """
        super().remove(agent)
        agent_class: type[Agent] = type(agent)
        self.agents_by_type[agent_class].pop(agent.unique_id)

    def step(self) -> None:
        """
        Executes all the stages for all agents. This method is called by the model.
        """
        for type_stage in self.types_with_stages:
            # Get the agents of the type
            agent_keys = list(self.agents_by_type[type_stage.type].keys())

            if self.shuffle:
                self.model.random.shuffle(agent_keys)

            # Get the stage and run this stage for the agents
            stage = type_stage.stage
            for agent_key in agent_keys:
                if agent_key in self.agents_by_type[type_stage.type]:
                    getattr(self.agents_by_type[type_stage.type][agent_key], stage)()

            self.time += self.stage_time

        self.steps += 1
