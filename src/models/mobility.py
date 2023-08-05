from mesa import Agent
from pandas import DataFrame, concat

import src.core.common_constants as cc

__all__ = ["StaticMobilityModel", "TraceMobilityModel"]


class StaticMobilityModel(Agent):
    def __init__(self, position: list[float]):
        """
        Initialize the static mobility model.

        Parameters
        ----------
        position : DataFrame
            DataFrame of positions.
        """
        super().__init__(0, None)
        self._type = "static"
        self._current_location = position

    @property
    def type(self) -> str:
        """Get the type of the mobility model."""
        return self._type

    @property
    def current_location(self) -> list[float]:
        """Get the current location."""
        return self._current_location

    def step(self) -> None:
        pass

    def update_position(self, new_position: list[float]) -> None:
        """
        Update the position.

        Parameters
        ----------
        new_position : DataFrame
            The new positions.
        """
        self._current_location = new_position


class TraceMobilityModel(Agent):
    def __init__(self):
        """
        Initialize the trace mobility model.
        """
        super().__init__(0, None)
        self._type: str = "trace"

        self._current_time: int = 0
        self._current_location: list[float] = []
        self._positions: DataFrame = DataFrame()

    @property
    def type(self) -> str:
        """Get the type of the mobility model."""
        return self._type

    @property
    def current_location(self) -> list[float]:
        """Get the current location."""
        return self._current_location

    @property
    def current_time(self) -> int:
        """Get the current time."""
        return self._current_time

    @current_time.setter
    def current_time(self, value: int) -> None:
        """Set the current time."""
        self._current_time = value

    def update_positions(self, positions: DataFrame) -> None:
        """
        Update the positions.

        Parameters
        ----------
        positions : DataFrame
            The new positions.
        """
        self._positions = concat([self._positions, positions], ignore_index=True)

    def step(self) -> None:
        """
        Step through the model.
        """
        # Check if the current time is in the positions dataframe
        if self._current_time in self._positions[cc.TIME_STEP].values:
            self._current_location = (
                self._positions[self._positions[cc.TIME_STEP] == self._current_time]
                .iloc[0]
                .values[2:]
            )
        else:
            # If not, then the vehicle is not moving
            self._current_location = self._current_location
