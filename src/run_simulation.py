import argparse

from os.path import exists
from src.Simulation import Simulation


def create_simulation(config_file: str) -> Simulation:
    # Create the simulation setup object if the config file exists
    if not exists(config_file):
        raise FileNotFoundError('Config file not found: %s' % config_file)
    simulation = Simulation(config_file)

    # Setup the simulation.
    simulation.setup_simulation()

    # Return the simulation object
    return simulation


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Run the simulation.')
    parser.add_argument('--config', type=str, help='The path to the config file.')

    # Parse the arguments
    args = parser.parse_args()

    # Create the simulation and run it
    net_simulation = create_simulation(args.config)
    net_simulation.run()

