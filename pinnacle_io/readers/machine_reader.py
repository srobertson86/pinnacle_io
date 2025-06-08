"""
Reader for Pinnacle plan.Pinnacle.Machines files.
"""
from pathlib import Path
from pinnacle_io.models import Machine
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader
from typing import List

class MachineReader:
    """
    Reader for Pinnacle plan.Pinnacle.Machines files.
    """
    @staticmethod
    def read(plan_path: str) -> List[Machine]:
        """
        Read a Pinnacle plan.Pinnacle.Machines directory and create a list of Machine models.
        
        Args:
            plan_path: Path to the plan directory or plan.Pinnacle.Machines file
            
        Returns:
            List of Machine models populated with data from the files
        """
        path = Path(plan_path)
        if not str(path).lower().endswith('plan.Pinnacle.Machines'):
            path = path / 'plan.Pinnacle.Machines'
        
        if not path.exists():
            raise FileNotFoundError(f"Machine file not found: {path}")
        
        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            return MachineReader.parse_machine_content(f.readlines())
    
    @staticmethod
    def parse_machine_content(content_lines: list[str]) -> List[Machine]:
        """
        Parse a Pinnacle Machine content string and create a list of Machine models.
        
        Args:
            content_lines: Pinnacle Machine content lines
            
        Returns:
            List of Machine models populated with data from the content
        """
        data = PinnacleFileReader.parse_key_value_content_lines(content_lines)
        machines = []
        for machine_data in data.values():
            machines.append(Machine(**machine_data))
        return machines