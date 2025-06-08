"""
Reader for Pinnacle plan.Trial files.
"""

from pathlib import Path
from typing import List
from pinnacle_io.models import Trial
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader
from pinnacle_io.readers.patient_setup_reader import PatientSetupReader

class TrialReader:
    """
    Reader for Pinnacle plan.Trial files.
    """
    @staticmethod
    def read(plan_path: str) -> List[Trial]:
        """
        Read a Pinnacle plan.Trial file and return the Trial models.
        The patient setup information is also processed and attached to the Trial models.

        Args:
            plan_path: Path to the Pinnacle plan.Trial file

        Returns:
            List of Trial models populated with data from the file
        """
        path = Path(plan_path)
        if not str(path).lower().endswith("plan.Trial"):
            path = path / 'plan.Trial'

        if not path.exists():
            raise FileNotFoundError(f"plan.Trial file not found: {path}")
        
        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            trials = TrialReader.parse_trial_content(f.readlines())
        
        patient_position = PatientSetupReader.read(str(path.parent))
        for trial in trials:
            trial._patient_position = patient_position
        return trials

    @staticmethod
    def parse_trial_content(content_lines: list[str]) -> List[Trial]:
        """
        Parse a Pinnacle plan.Trial content string and create a Trial model.
        The patient setup information is NOT processed by this method.

        Args:
            content_lines: Pinnacle plan.Trial content lines

        Returns:
            List of Trial models populated with data from the content
        """
        data = PinnacleFileReader.parse_key_value_content_lines(content_lines)
        trials = [Trial(**trial, trial_id=i) for i, trial in enumerate(data.get("TrialList", []))]
        return trials
