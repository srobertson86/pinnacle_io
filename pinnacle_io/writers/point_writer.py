"""
Writer for Pinnacle Point files.
"""

from pinnacle_io.models import Point

class PointWriter:
    """
    Writer for Pinnacle Point files.
    """
    @staticmethod
    def write(point: Point, path: str) -> None:
        """
        Write a Pinnacle Point model to files.

        Args:
            point: Point model
            path: Path to write the Point files
        """
        raise NotImplementedError("PointWriter.write is not implemented")
