from mesa import Agent


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
