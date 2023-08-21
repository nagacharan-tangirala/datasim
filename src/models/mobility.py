import logging

from mesa import Agent

from src.core.common_constants import Column, CoordSpace, TraceTimes
from src.core.constants import ModelType

logger = logging.getLogger(__name__)


class StaticMobilityModel(Agent):
    def __init__(self):
        """
        Initialize the static mobility model.

        Parameters
        ----------
        position : list[float]
            The position of the vehicle.
        """
        super().__init__(0, None)
        self._type = ModelType.STATIC
        self._current_location: list[float] = []

    @property
    def type(self) -> str:
        """Get the type of the mobility model."""
        return self._type

    @property
    def current_location(self) -> list[float]:
        """Get the current location."""
        return self._current_location

    def step(self) -> None:
        """
        Step through the model.
        """
        pass

    def update_position(self, new_position: list[float]) -> None:
        """
        Update the position.

        Parameters
        ----------
        new_position : list[float]
            The new position.
        """
        self._current_location = new_position


class TraceMobilityModel(Agent):
    def __init__(self):
        """
        Initialize the trace mobility model.
        """
        super().__init__(0, None)
        self._type: str = ModelType.TRACE

        self.current_time: int = 0
        self._current_velocity: float = 0.0
        self._current_location: list[float] = []

        self._positions: dict = {}
        self._velocities: dict = {}

    @property
    def type(self) -> str:
        """Get the type of the mobility model."""
        return self._type

    @property
    def current_location(self) -> list[float]:
        """Get the current location."""
        return self._current_location

    @property
    def current_velocity(self) -> float:
        """Get the current velocity."""
        return self._current_velocity

    def update_mobility_data(self, new_positions_data: dict) -> None:
        """
        Update the positions.

        Parameters
        ----------
        new_positions_data : dict
            The new positions.
        """
        positions_data = dict(
            zip(
                new_positions_data[TraceTimes.TIME_STEP],
                zip(new_positions_data[CoordSpace.X], new_positions_data[CoordSpace.Y]),
            )
        )
        velocity_data = dict(
            zip(
                new_positions_data[TraceTimes.TIME_STEP],
                new_positions_data[Column.VELOCITY],
            )
        )

        self._positions.update(positions_data)
        self._velocities.update(velocity_data)

    def step(self) -> None:
        """
        Step through the model.
        """
        # Check if the current time is in the positions dataframe
        if self.current_time in self._positions:
            self._current_location = self._positions[self.current_time]
            self._current_velocity = self._velocities[self.current_time]
        elif not self._current_location:
            logger.error(f"Missing position for time step {self.current_time}")
            exit(1)
