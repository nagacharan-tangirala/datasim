from abc import abstractmethod
from collections import namedtuple

from mesa import Agent
from pandas import DataFrame

from src.core.CustomExceptions import WrongActivationTimeError, WrongDeactivationTimeError


class UEBase(Agent):
    def __init__(self, ue_id: int):
        """
        Initialize the ue.
        """
        super().__init__(ue_id, None)

        self.sim_model = None

        self.position: list[float] = []

        self._start_time: int = 0
        self._end_time: int = 0

        self.active: bool = False

    @property
    def start_time(self) -> int:
        """ Get the start time. """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: int) -> None:
        """ Set the start time. """
        if start_time < 0:
            raise ValueError("Start time must be positive.")
        self._start_time = start_time

    @property
    def end_time(self) -> int:
        """ Get the end time. """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: int) -> None:
        """ Set the end time. """
        if end_time < 0:
            raise ValueError("End time must be positive.")
        self._end_time = end_time

    @abstractmethod
    def step(self, *args, **kwargs) -> None:
        """
        Step function for the ue.
        """
        pass

    @abstractmethod
    def _activate_models(self) -> None:
        """
        Initiate the models related to this ue.
        """
        pass

    @abstractmethod
    def _deactivate_models(self) -> None:
        """
        Deactivate the models related to this ue.
        """
        pass

    @abstractmethod
    def update_mobility_data(self, mobility_data: DataFrame) -> None:
        """
        Update the mobility model data.
        """
        pass

    @abstractmethod
    def get_generated_data(self) -> namedtuple:
        """
        Get the generated data.
        """
        pass

    def activate_ue(self, time_step: int) -> None:
        """
        Activate the ue.
        """
        if time_step != self.start_time:
            raise WrongActivationTimeError(time_step, self.start_time)
        self._activate_models()

    def deactivate_ue(self, time_step: int) -> None:
        """
        Deactivate the ue.
        """
        if time_step != self.end_time:
            raise WrongDeactivationTimeError(time_step, self.end_time)
        self._deactivate_models()
