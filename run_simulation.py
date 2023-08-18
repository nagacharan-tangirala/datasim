import argparse
from pathlib import Path

from src.core.simulation import Simulation


def create_simulation(config_file: str) -> Simulation:
    """
    Creates a simulation object.

    Parameters
    ----------
    config_file : str
        The path to the config file.
    """
    config_file = Path(config_file).resolve()
    if not Path.exists(config_file):
        raise FileNotFoundError("Config file not found: %s" % config_file)

    # Create the simulation object.
    simulation = Simulation(config_file)

    # Set up the simulation.
    simulation.setup_simulation()

    # Return the simulation object
    return simulation


def run_simulation(simulation: Simulation):
    """
    Runs the simulation.

    Parameters
    ----------
    simulation : Simulation
        The simulation object to run.
    """
    simulation.run()
    simulation.save_simulation_results()


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Run the simulation.")
    parser.add_argument("--config", type=str, help="The path to the config file.")

    # Parse the arguments
    args = parser.parse_args()

    # Create the simulation object
    net_simulation = create_simulation(args.config)

    # Run the simulation
    run_simulation(net_simulation)
