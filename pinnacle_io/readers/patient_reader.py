"""
Reader for Pinnacle Patient files.
"""

from pathlib import Path
from pinnacle_io.models import Patient
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader


class PatientReader:
    """
    Reader for Pinnacle Patient files.
    """
    @staticmethod
    def read(patient_path: str) -> Patient:
        """
        Read a Pinnacle Patient file and create a Patient model.

        Args:
            patient_path: Path to the Patient file

        Returns:
            Patient model populated with data from the file
        """
        path = Path(patient_path)
        if not str(path).lower().endswith("Patient"):
            path = path / 'Patient'

        if not path.exists():
            raise FileNotFoundError(f"Patient file not found: {path}")
        
        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            return PatientReader.parse_patient_content(f.readlines())

    @staticmethod
    def parse_patient_content(content_lines: list[str]) -> Patient:
        """
        Parse a Pinnacle Patient content string and create a Patient model.

        Args:
            content_lines: Pinnacle Patient content lines

        Returns:
            Patient model populated with data from the content
        """
        data = PinnacleFileReader.parse_key_value_content_lines(content_lines)
        patient = Patient(**data)
        return patient
