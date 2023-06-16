from src.channel.BUEChannel import BaseUEChannel


class InfiniteBandwidthUEChannel(BaseUEChannel):
    def __init__(self):
        super().__init__()

    def _send_data_to_cell_towers(self):
        """
        Send data to the respective cell_towers.
        """
        # Send as much data as the bandwidth allows.
        for cell_tower_id, ues in self.cell_tower_coverage_ues.items():
            for ue_id in ues:
                # Get the data from the ue
                data = self.data_from_ues[ue_id]

                # TODO: Add bandwidth, losses, quantization, etc. to the channel.

                # Send the data to the cell_tower
                self.cell_towers[cell_tower_id].receive_data(ue_id, data)

                # Tell the ue that the data has been sent
                self.ues[ue_id].set_data_transmit_status(True)

    def _send_data_to_neighbours(self):
        """
        Send data to neighbouring ues.
        """
        # TODO: Complete this function.
        # Whoever failed to send data in the previous time step, send it now.
        for ue_id, ue in self.ues.items():
            # Get the neighbouring ues data
            data = ue.get_neighbour_data()

            if len(data) is 0:
                continue

            # Send the data to the neighbouring ues
            for neighbour_id, neighbour_data in data.items():
                # Get the data from the ue
                data = self.data_from_ues[ue_id]

    def _receive_data_from_cell_towers(self):
        pass

    def _send_data_to_ues(self):
        pass
