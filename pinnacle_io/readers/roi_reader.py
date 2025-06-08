"""
Reader for Pinnacle plan.roi files.
"""

import numpy as np
from pathlib import Path
from pinnacle_io.models import ROI, Curve
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader
from typing import List

class ROIReader:
    """
    Reader for Pinnacle plan.roi files.
    """
    @staticmethod
    def read(plan_path: str) -> List[ROI]:
        """
        Read a Pinnacle plan.roi file and create a list of ROI models.

        Args:
            plan_path: Path to the patient's plan directory

        Returns:
            List of ROI models populated with data from the file
        """
        path = Path(plan_path)
        if not str(path).lower().endswith("plan.roi"):
            path = path / 'plan.roi'

        if not path.exists():
            raise FileNotFoundError(f"plan.roi file not found: {path}")
        
        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            return ROIReader._parse_roi_lines(f.readlines())

    @staticmethod
    def parse_roi_content(content_lines: list[str]) -> List[ROI]:
        """
        Parse a Pinnacle plan.roi content string and create a list of ROI models.

        Args:
            content_lines: Pinnacle plan.roi content lines

        Returns:
            List of ROI models populated with data from the content
        """
        return ROIReader._parse_roi_lines(content_lines)

    @staticmethod
    def _parse_roi_lines(lines: list[str]) -> List[ROI]:
            """
            Parse ROI lines into a list of ROI models.

            Args:
                lines: List of lines from the ROI file.

            Returns:
                List of ROI models populated with data from the content.
            """
            lines = [line.strip() for line in lines]
            beginning_of_rois = [i for i in range(len(lines)) if lines[i] == "roi={"]
            beginning_of_curves = [i for i in range(len(lines)) if lines[i] == "curve={"]

            rois = []
            i_roi = 0
            i_curve = 0
            while i_roi < len(beginning_of_rois) and i_curve < len(beginning_of_curves):
                beginning_of_roi = beginning_of_rois[i_roi]
                beginning_of_curve = beginning_of_curves[i_curve]
                roi_lines = lines[beginning_of_roi + 1 : beginning_of_curve]
                roi_data = PinnacleFileReader.parse_key_value_content_lines(roi_lines)
                roi_data["roi_number"] = i_roi + 1
                roi = ROI(**roi_data)

                curve_number = 0
                while curve_number < roi_data["num_curve"]:
                    beginning_of_curve = beginning_of_curves[i_curve]
                    curve_lines = lines[beginning_of_curve + 1 : beginning_of_curve + 4]
                    curve_data = PinnacleFileReader.parse_key_value_content_lines(curve_lines)
                    curve_data["curve_number"] = curve_number

                    beginning_of_points = beginning_of_curve + 5
                    point_lines = lines[
                        beginning_of_points : beginning_of_points + curve_data["num_points"]
                    ]
                    curve_data["points"] = np.array(
                        [list(map(float, line.split())) for line in point_lines]
                    )
                    roi.curve_list.append(Curve(**curve_data))

                    curve_number += 1
                    i_curve += 1

                rois.append(roi)
                i_roi += 1

            return rois