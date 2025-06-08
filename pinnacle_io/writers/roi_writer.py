"""
Writer for Pinnacle ROI files.
"""

from pinnacle_io.models import ROI

class ROIWriter:
    """
    Writer for Pinnacle ROI files.
    """
    @staticmethod
    def write(roi: ROI, path: str) -> None:
        """
        Write a Pinnacle ROI model to files.

        Args:
            roi: ROI model
            path: Path to write the ROI files
        """
        raise NotImplementedError("ROIWriter.write is not implemented")
