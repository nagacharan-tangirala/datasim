from mesa import Model, Agent

from src.core.BSimulation import SimulationBase
from src.setup.SParticipantFactory import ParticipantFactory
from src.abm_model.ABMModel import ABMModel


class SimulationABM(SimulationBase):
    def __init__(self, config_file: str):
        """
        Initialize the simulation object.
        """
        super().__init__(config_file)

    def setup_simulation(self):
        """
        Set up the simulation.
        """
        # Call the base class setup function
        super().setup_simulation()

        self._create_participants()
        self._create_model()

    def _create_participants(self):
        """
        Create the participants in the simulation. These are the non-mesa agents.
        """
        # Create a participant factory object and create the participants
        participant_factory = ParticipantFactory(self.config_dict)
        participant_factory.create_participants_of_type('sensor')
        participant_factory.create_participants_of_type('node')
        participant_factory.create_participants_of_type('agent')
        participant_factory.create_participants_of_type('controller')

        # Get the nodes and agents
        self.nodes = participant_factory.get_nodes()
        self.agents = participant_factory.get_devices()

    def _create_model(self):
        """
        Create the ABM model.
        """
        self.model = ABMModel(self.config_dict.simulation_params, self.agents)

    def run(self):
        """
        Run the simulation.
        """
        self.model.run()
