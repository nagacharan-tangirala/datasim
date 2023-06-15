from src.output.BOutput import OutputBase


class OutputParquet(OutputBase):
    def __init__(self, params: dict):
        """
        Initialize the output CSV class.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the output CSV class.
        """
        super().__init__(params)

    def _write_data(self, agents: dict, nodes: dict):
        """
        Write the output to the CSV file.

        Parameters
        ----------
        agents : dict
            Dictionary of agents in the simulation.
        nodes : dict
            Dictionary of nodes in the simulation.
        """
        pass
