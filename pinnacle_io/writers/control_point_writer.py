"""
Writer for Pinnacle ControlPoint files.
"""

from pinnacle_io.models import ControlPoint

class ControlPointWriter:
    """
    Writer for Pinnacle ControlPoint files.
    """
    @staticmethod
    def write(control_point: ControlPoint, path: str) -> None:
        """
        Write a Pinnacle ControlPoint model to files.

        Args:
            control_point: ControlPoint model
            path: Path to write the ControlPoint files
        """
        raise NotImplementedError("ControlPointWriter.write is not implemented")
