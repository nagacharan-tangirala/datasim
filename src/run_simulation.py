from os.path import exists
from src.setup.SSimulationSetup import SimulationSetup
import argparse


class Simulation:
    def __init__(self, config_file: str):
        # Create the simulation setup object if the config file exists
        if not exists(config_file):
            raise FileNotFoundError('Config file not found: %s' % config_file)
        self.sim_setup = SimulationSetup(config_file)

        # Read the config file
        self.sim_setup.setup_simulation()

    def run(self):
        pass


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Run the simulation.')
    parser.add_argument('--config', type=str, help='The path to the config file.')

    # Parse the arguments
    args = parser.parse_args()

    # Create the simulation object and run it
    simulation = Simulation(args.config)
    simulation.run()
