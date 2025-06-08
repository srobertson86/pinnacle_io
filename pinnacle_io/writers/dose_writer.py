"""
Writer for Pinnacle Dose files.
"""

from pinnacle_io.models import Dose

class DoseWriter:
    """
    Writer for Pinnacle Dose files.
    """
    @staticmethod
    def write(dose: Dose, path: str) -> None:
        """
        Write a Pinnacle Dose model to a file.

        Args:
            dose: Dose model
            path: Path to write the Dose file
        """
        raise NotImplementedError("DoseWriter.write is not implemented")
