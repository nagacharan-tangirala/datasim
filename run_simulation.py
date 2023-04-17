import argparse

from os.path import exists
from src.core.BSimulation import SimulationBase
from src.core.SSimulationFactory import SimulationFactory


def create_simulation(config_file: str, sim_type: str) -> SimulationBase:
    """
    This function creates the simulation object.

    Parameters
    ----------
    config_file : str
        The path to the config file.
    """
    if not exists(config_file):
        raise FileNotFoundError('Config file not found: %s' % config_file)

    # Create simulation factory object
    simulation_factory = SimulationFactory()

    # Create the simulation object
    simulation = simulation_factory.create_simulation(sim_type, config_file)

    # Set up the simulation.
    simulation.setup_simulation()

    # Return the simulation object
    return simulation


def run_simulation(simulation: SimulationBase):
    """
    This function initiates the simulation.

    Parameters
    ----------
    simulation : Simulation
        The simulation object to run.
    """
    simulation.run()


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Run the simulation.')
    parser.add_argument('--config', type=str, help='The path to the config file.')
    parser.add_argument('--simtype', type=str, help='The type of simulation to run. (default: "simple")', default="simple")

    # Parse the arguments
    args = parser.parse_args()

    # Create the simulation object
    net_simulation = create_simulation(args.config, args.simtype)

    # Run the simulation
    run_simulation(net_simulation)
