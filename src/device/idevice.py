from typing import Protocol


class IDevice(Protocol):
    """
    This is an interface for all the devices in the simulation to mimic. The interface is used to ensure that
    all the devices have the uplink and downlink stages. This is required for the scheduler to work as expected.
    """

    def uplink_stage(self) -> None:
        ...

    def downlink_stage(self) -> None:
        ...
