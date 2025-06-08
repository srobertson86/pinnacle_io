"""
Writer for Pinnacle PatientSetup files.
"""

from pinnacle_io.models import PatientSetup

class PatientSetupWriter:
    """
    Writer for Pinnacle PatientSetup files.
    """
    @staticmethod
    def write(patient_setup: PatientSetup, path: str) -> None:
        """
        Write a Pinnacle PatientSetup model to files.

        Args:
            patient_setup: PatientSetup model
            path: Path to write the PatientSetup files
        """
        raise NotImplementedError("PatientSetupWriter.write is not implemented")
