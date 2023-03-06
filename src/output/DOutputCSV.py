import time

from src.output.BOutput import OutputBase
from os.path import exists, join


class OutputCSV(OutputBase):
    def __init__(self, params: dict):
        """
        Initialize the output CSV class.
        """
        super().__init__(params)

        time_now = time.time()

        self.nodes_file = join(self.output_dir, "output.csv")
        if exists(self.nodes_file):
            self.nodes_file = join(self.output_dir, "nodes_output_{}.csv".format(time_now))

        self.entities_file = join(self.output_dir, "entities_output.csv")
        if exists(self.entities_file):
            self.entities_file = join(self.output_dir, "entities_output_{}.csv".format(time_now))

    def _write_data(self, entities: dict, nodes: dict):
        """
        Write the output to the CSV file.

        Parameters
        ----------
        entities : dict
            Dictionary of entities in the simulation.
        nodes : dict
            Dictionary of nodes in the simulation.
        """
        self._write_nodes_output(nodes)
        self._write_entities_output(entities)

    def _write_nodes_output(self, nodes: dict):
        """
        Write the output to the CSV file.

        Parameters
        ----------
        nodes : dict
            Dictionary of nodes in the simulation.
        """
        with open(self.nodes_file, 'w') as f:
            f.write("node_id, data_collected")

    def _write_entities_output(self, entities: dict):
        """
        Write the output to the CSV file.

        Parameters
        ----------
        entities : dict
            Dictionary of entities in the simulation.
        """
        with open(self.entities_output, 'w') as f:
            f.write("entity_id, data_collected")
