"""
Writer for Pinnacle Beam files.
"""

from pinnacle_io.models import Beam

class BeamWriter:
    """
    Writer for Pinnacle Beam files.
    """
    @staticmethod
    def write(beam: Beam, path: str) -> None:
        """
        Write a Pinnacle Beam model to files.

        Args:
            beam: Beam model
            path: Path to write the Beam files
        """
        raise NotImplementedError("BeamWriter.write is not implemented")
