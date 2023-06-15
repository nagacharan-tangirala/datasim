from abc import ABCMeta, abstractmethod


class OutputBase(metaclass=ABCMeta):
    def __init__(self, params: dict):
        """
        Initialize the output base class.
        """
        self.output_dir = params.get("output_dir")
        self.output_step = params.get("output_step")

        self.last_output_time = 0

    def get_output_dir(self) -> str:
        """
        Get the output directory.

        Returns
        ----------
        str
            The output directory.
        """
        return self.output_dir

    def get_output_step(self) -> int:
        """
        Get the output step.

        Returns
        ----------
        int
            The output step.
        """
        return self.output_step

    def write_output(self, sim_time: int, agents: dict, nodes: dict):
        """
        Write the output to the CSV file.

        Parameters
        ----------
        sim_time : int
            The current time.
        agents : dict
            Dictionary of agents in the simulation.
        nodes : dict
            Dictionary of nodes in the simulation.
        """
        # Check if it is time to write the output. If not, return.
        if sim_time > self.last_output_time:
            self._write_data(agents, nodes)

        # Update the last update time.
        self.last_output_time = sim_time

    @abstractmethod
    def _write_data(self, agents: dict, nodes: dict):
        """
        Write the output to the requested format.

        Parameters
        ----------
        agents : dict
            Dictionary of agents in the simulation.
        nodes : dict
            Dictionary of nodes in the simulation.
        """
        pass
