import datetime
import time

from src.output.BOutput import OutputBase
from os.path import exists, join


class OutputCSV(OutputBase):
    def __init__(self, params: dict):
        """
        Initialize the output CSV class.
        """
        super().__init__(params)

        time_now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')

        self.nodes_file = join(self.output_dir, "nodes_output.csv")
        if exists(self.nodes_file):
            self.nodes_file = join(self.output_dir, "nodes_output_{}.csv".format(time_now))

        self.entities_file = join(self.output_dir, "entities_output.csv")
        if exists(self.entities_file):
            self.entities_file = join(self.output_dir, "entities_output_{}.csv".format(time_now))

        self._write_headers_to_csv()

    def _write_headers_to_csv(self):
        """
        Write the headers to the output CSV files.
        """
        with open(self.nodes_file, 'w') as f:
            f.write("time,node_id,data_collected\n")

        with open(self.entities_file, 'w') as f:
            f.write("time,entity_id,data_collected\n")

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
        nodes : dict[dict[list]]
            Dictionary of nodes in the simulation.
        """
        with open(self.nodes_file, 'a') as f:
            for ts, node_data_ts in nodes.items():
                for node_id, data_collected in node_data_ts.items():
                    f.write("{},{},{}\n".format(ts, node_id, data_collected))

    def _write_entities_output(self, entities: dict):
        """
        Write the output to the CSV file.

        Parameters
        ----------
        entities : dict
            Dictionary of entities in the simulation.
        """
        with open(self.entities_file, 'a') as f:
            for ts, entity_data_ts in entities.items():
                for entity_id, data_collected in entity_data_ts.items():
                    f.write("{},{},{}\n".format(ts, entity_id, data_collected))
