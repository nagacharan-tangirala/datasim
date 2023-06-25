from abc import abstractmethod

from mesa import Agent
from pandas import DataFrame

from src.core.CustomExceptions import WrongActivationTimeError, WrongDeactivationTimeError


class BaseUE(Agent):
    def __init__(self, ue_id: int):
        """
        Initialize the ue.
        """
        super().__init__(ue_id, None)

        self.sim_model = None

        self.current_position: list[float] = []

        self.start_time: int = 0
        self.end_time: int = 0

        self.active: bool = False
        self.data_sent: bool = False

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

    def get_id(self) -> int:
        """
        Get the ue id.

        Returns
        -------
        int
            The ue id.
        """
        return self.unique_id

    def get_position(self) -> list[float]:
        """
        Get the current position of the ue.

        Returns
        -------
        list[float]
            The current position of the ue.
        """
        return self.current_position

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

    def get_start_and_end_time(self) -> tuple[int, int]:
        """
        Get the start and end time of the ue.

        Returns
        -------
        tuple[int, int]
            The start and end time of the ue.
        """
        return self.start_time, self.end_time
