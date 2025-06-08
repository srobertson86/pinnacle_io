"""
Writer for Pinnacle Patient files.
"""

from pinnacle_io.models import Patient

class PatientWriter:
    """
    Writer for Pinnacle Patient files.
    """
    @staticmethod
    def write(patient: Patient, path: str) -> None:
        """
        Write a Pinnacle Patient model to files.

        Args:
            patient: Patient model
            path: Path to write the Patient files
        """
        raise NotImplementedError("PatientWriter.write is not implemented")
