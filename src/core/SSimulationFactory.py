from src.core.DSimulationSimple import SimulationSimple
from src.core.DSimulationABM import SimulationABM


class SimulationFactory:
    """
    This class is a factory for creating simulation objects.
    """

    def __init__(self):
        """
        Initialize the simulation factory.
        """
        pass

    @staticmethod
    def create_simulation(sim_type: str, config_file: str):
        """
        This function creates a simulation object.

        Parameters
        ----------
        sim_type : str
            The type of simulation to create.
        config_file : str
            The path to the config file.
        """
        if sim_type == 'simple':
            return SimulationSimple(config_file)
        elif sim_type == 'abm':
            return SimulationABM(config_file)
        else:
            raise ValueError('Invalid simulation type: %s' % sim_type)
