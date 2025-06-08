"""
Writer for Pinnacle Trial files.
"""

from pinnacle_io.models import Trial

class TrialWriter:
    """
    Writer for Pinnacle Trial files.
    """
    @staticmethod
    def write(trial: Trial, path: str) -> None:
        """
        Write a Pinnacle Trial model to files.

        Args:
            trial: Trial model
            path: Path to write the Trial files
        """
        raise NotImplementedError("TrialWriter.write is not implemented")
