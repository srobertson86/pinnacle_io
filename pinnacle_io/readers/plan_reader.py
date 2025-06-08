"""
Reader for Pinnacle Plan files.
"""

from pathlib import Path
from typing import List
from pinnacle_io.models import Plan, Patient
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader
from pinnacle_io.readers.patient_setup_reader import PatientSetupReader

class PlanReader:
    """
    Reader for Pinnacle Plan files.
    """
    @staticmethod
    def read(patient_path: str) -> List[Plan]:
        """
        Read a Pinnacle Patient file and return the Plan models.
        The patient setup information is also processed and attached to the Plan models.

        Args:
            patient_path: Path to the Pinnacle Patient file

        Returns:
            List of Plan models populated with data from the file
        """
        path = Path(patient_path)
        if not str(path).lower().endswith("Patient"):
            path = path / 'Patient'

        if not path.exists():
            raise FileNotFoundError(f"Patient file not found: {path}")
        
        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            plans = PlanReader.parse_patient_content(f.readlines())
        
        for i, plan in enumerate(plans):
            try:
                plan._patient_position = PatientSetupReader.read(str(path.parent / f"Plan_{i}"))
            except FileNotFoundError:
                pass

        return plans

    @staticmethod
    def parse_patient_content(content_lines: list[str]) -> List[Plan]:
        """
        Parse a Pinnacle Patient content string and create a Patient model.
        The patient setup information is NOT processed by this method.

        Args:
            content_lines: Pinnacle Patient content lines

        Returns:
            List of Plan models populated with data from the content
        """
        data = PinnacleFileReader.parse_key_value_content_lines(content_lines)
        patient = Patient(**data)
        return patient.plan_list
