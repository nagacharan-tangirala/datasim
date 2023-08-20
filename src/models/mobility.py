import logging

from mesa import Agent
from pandas import DataFrame, concat

from src.core.common_constants import CoordSpace, TraceTimes
from src.core.constants import ModelType

logger = logging.getLogger(__name__)


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
        self._type = ModelType.STATIC
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
        """
        Step through the model.
        """
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
        self._type: str = ModelType.TRACE

        self.current_time: int = 0
        self._current_location: list[float] = []
        self._positions_df: DataFrame = DataFrame()
        self._positions: dict = {}

    def _prepare_positions(self) -> None:
        """
        Prepare the positions.
        """
        self._positions_df[TraceTimes.TIME_STEP] = self._positions_df[
            TraceTimes.TIME_STEP
        ].astype(int)

        # Convert the positions to a dictionary
        self._positions = dict(
            zip(
                self._positions_df[TraceTimes.TIME_STEP],
                list(
                    zip(
                        self._positions_df[CoordSpace.X],
                        self._positions_df[CoordSpace.Y],
                    )
                ),
            )
        )

    @property
    def type(self) -> str:
        """Get the type of the mobility model."""
        return self._type

    @property
    def current_location(self) -> list[float]:
        """Get the current location."""
        return self._current_location

    def update_positions(self, new_positions_df: DataFrame) -> None:
        """
        Update the positions.

        Parameters
        ----------
        new_positions_df : DataFrame
            The new positions.
        """
        self._positions_df = concat(
            [self._positions_df, new_positions_df], ignore_index=True
        )
        self._prepare_positions()

    def step(self) -> None:
        """
        Step through the model.
        """
        # Check if the current time is in the positions dataframe
        if self.current_time in self._positions:
            self._current_location = self._positions[self.current_time]
        elif not self._current_location:
            logger.error(f"Missing position for time step {self.current_time}")
            exit(1)
