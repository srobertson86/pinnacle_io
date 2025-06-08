"""
Reader for Pinnacle plan.PatientSetup files.
"""

from pathlib import Path
from pinnacle_io.models import PatientSetup
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader

class PatientSetupReader:
    """
    Reader for Pinnacle plan.PatientSetup files.
    """
    @staticmethod
    def read(plan_path: str) -> PatientSetup:
        """
        Read a Pinnacle plan.PatientSetup file and return the PatientSetup models.

        Args:
            path: Path to the Pinnacle plan.PatientSetup file

        Returns:
            PatientSetup model populated with data from the file
        """
        path = Path(plan_path)
        if not str(path).lower().endswith("plan.PatientSetup"):
            path = path / 'plan.PatientSetup'

        if not path.exists():
            raise FileNotFoundError(f"plan.PatientSetup file not found: {path}")
        
        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            return PatientSetupReader.parse_patient_setup_content(f.readlines())

    @staticmethod
    def parse_patient_setup_content(content_lines: list[str]) -> PatientSetup:
        """
        Parse a Pinnacle plan.PatientSetup content string and create a PatientSetup model.

        Args:
            content_lines: Pinnacle plan.PatientSetup content lines

        Returns:
            PatientSetup model populated with data from the content
        """
        data = PinnacleFileReader.parse_key_value_content_lines(content_lines)
        patient_setup = PatientSetup(**data)
        return patient_setup
