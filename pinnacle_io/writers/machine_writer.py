"""
Writer for Pinnacle plan.Pinnacle.Machines files.
"""

from pinnacle_io.models import Machine

class MachineWriter:
    """
    Writer for Pinnacle plan.Pinnacle.Machines files.
    """
    @staticmethod
    def write(machine: Machine, path: str) -> None:
        """
        Write a Pinnacle Machine model to files.

        Args:
            machine: Machine model
            path: Path to write the Machine files
        """
        raise NotImplementedError("MachineWriter.write is not implemented")
