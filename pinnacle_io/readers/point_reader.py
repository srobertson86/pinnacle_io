"""
Reader for Pinnacle plan.Points files.
"""

from pathlib import Path
from typing import List
from pinnacle_io.models import Point
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader


class PointReader:
    """
    Reader for Pinnacle plan.Points files.
    """
    @staticmethod
    def read(plan_path: str) -> List[Point]:
        """
        Read a Pinnacle plan.Points file and create a list of Point models.

        Args:
            plan_path: Path to the patient's plan directory

        Returns:
            List of Point models populated with data from the file
        """
        path = Path(plan_path)
        if not str(path).lower().endswith("plan.Points"):
            path = path / 'plan.Points'

        if not path.exists():
            raise FileNotFoundError(f"plan.Points file not found: {path}")
        
        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            return PointReader.parse_point_content(f.readlines())

    @staticmethod
    def parse_point_content(content_lines: list[str]) -> List[Point]:
        """
        Parse a Pinnacle plan.Points content string and create a list of Point models.

        Args:
            content_lines: Pinnacle plan.Points content lines

        Returns:
            List of Point models populated with data from the content
        """
        data = PinnacleFileReader.parse_key_value_content_lines(content_lines)
        return [Point(**point) for point in data['PoiList']]
