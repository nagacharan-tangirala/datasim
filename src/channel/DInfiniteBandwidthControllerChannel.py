from src.channel.BControllerChannel import BaseControllerChannel


class InfiniteBandwidthControllerChannel(BaseControllerChannel):
    def __init__(self, controller_links):
        """
        Initialize the infinite bandwidth controller channel.
        """
        super().__init__(controller_links)

    def _collect_from_cell_towers(self):
        """
        Collect data from the cell towers.
        """
        # Collect data from the cell towers
        for cell_tower_id, cell_tower in self.cell_towers.items():
            self.incoming_data[cell_tower_id] = cell_tower.get_incoming_data()

    def _send_to_controller(self):
        """
        Send data to the controller.
        """
        # Send data to the controller
