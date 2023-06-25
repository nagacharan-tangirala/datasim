# This script will test if the config file can be parsed by the simulator.
# It will not start the simulation, only loads the information from the config file.
# test_config.xml should be provided as an input argument. Make sure it is updated.

import argparse

from src.setup.SSimulationSetup import SimulationSetup

# Get the arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--config', type=str, required=True)
args = arg_parser.parse_args()

# Create simulation setup object.
simulation_setup = SimulationSetup(args.config)

# Test 1 - Read the config file.
simulation_setup.read_input_file()

print('Test passed - Able to read the simulation input data.')
