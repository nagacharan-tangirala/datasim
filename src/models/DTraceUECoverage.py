from pandas import DataFrame

from src.models.BUECoverage import UECoverage


class TraceUECoverage(UECoverage):
    def __init__(self, coverage_data: DataFrame):
        """
        Initialize the trace coverage model.
        """
        super().__init__()
        self.coverage_data = coverage_data

    def step(self):
        """
        Step through the model.
        """
        # Check if the coverage data is empty
        if self.coverage_data is None or len(self.coverage_data) == 0:
            self.coverage_data = []

        # Get the ues in the coverage
        self.ues_in_coverage = self.coverage_data[self.coverage_data["time"] == self.current_time]['neighbours'].tolist()
