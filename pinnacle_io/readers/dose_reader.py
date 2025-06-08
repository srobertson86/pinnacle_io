"""
Reader for Pinnacle plan.Trail.binary.### files.
"""

from pinnacle_io.models import Dose, DoseGrid, Trial, Beam
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader
import numpy as np
import os

class DoseReader:
    """
    Reader for Pinnacle plan.Trail.binary.### files.
    """
    @staticmethod 
    def read(plan_path: str, trial: Trial) -> Dose:
        """
        Read Pinnacle plan.Trail.binary.### files and create a Dose model for the given trial.
        This method saves the dose for each beam as well.

        Args:
            plan_path: Path to the patient's plan directory
            trial: Trial model to use for the dose

        Returns:
            Dose model populated with data from the file
        """
        for beam in trial.beam_list:
            beam.dose = DoseReader.read_beam_dose(plan_path, beam, trial.dose_grid)
        
        # TODO: Create a new dose for the trial that sums all beam doses
        trial_dose = Dose(dose_summation_type="PLAN")
        return trial_dose


    @staticmethod
    def read_beam_dose(plan_path, beam: Beam, dose_grid: DoseGrid) -> Dose:
        """
        Read a beam dose from a Pinnacle binary dose file.

        Args:
            plan_path: Path to the patient's plan directory
            beam: Beam model to use for the dose
            dose_grid: DoseGrid model to use for the dose

        Returns:
            Dose model populated with data from the file
        """

        # Get the unscaled binary dose data as a numpy array
        beam_dose_path = os.path.join(plan_path, beam.dose_volume_file)
        dose_data = DoseReader.read_binary_dose(beam_dose_path, dose_grid)

        # TODO: Scale the dose data based on monitor unit info and the machine PDD
        
        beam_dose = Dose(
            dose_type="PHYSICAL",
            dose_unit="CGY",
            dose_summation_type="BEAM",
            # Set both the relationship and the foreign key
            dose_grid=dose_grid,
            dose_grid_id=dose_grid.id if dose_grid else None,
            # Set dimensions
            x_dim=dose_grid.dimension.x if dose_grid else 0,
            y_dim=dose_grid.dimension.y if dose_grid else 0,
            z_dim=dose_grid.dimension.z if dose_grid else 0,
            x_pixdim=dose_grid.voxel_size.x,
            y_pixdim=dose_grid.voxel_size.y,
            z_pixdim=dose_grid.voxel_size.z,
            x_start=dose_grid.origin.x,
            y_start=dose_grid.origin.y,
            z_start=dose_grid.origin.z,
            dose_comment=beam.name,
            pixel_data=dose_data,
            beam = beam,
        )

        return beam_dose

    @staticmethod
    def read_binary_dose(file_path: str, dose_grid: DoseGrid = None) -> np.ndarray:
        """
        Read and parse a Pinnacle binary dose file.

        Args:
            file_path: Path to the binary dose file.
            dose_grid: A DoseGrid model object containing the dimensions of the dose volume.

        Returns:
            Numpy array of unscaled dose data (i.e., dose per monitor unit per fraction).
        """
        # Read the binary data directly from the file
        with open(file_path, 'rb') as f:
            binary_data = f.read()

        # The createdcm.py script loads the binary dose volume using:
        #     value = struct.unpack(">f", data_element)[0]
        # where ">f" indicates a 32-bit float in big-endian format
        data_type = ">f4"

        # Reshape binary data into 3D array
        dose_volume = np.frombuffer(binary_data, dtype=data_type)
        if dose_grid:
            # Convert dimensions to integers for reshaping
            z_dim = int(dose_grid.dimension.z)
            y_dim = int(dose_grid.dimension.y)
            x_dim = int(dose_grid.dimension.x)
            dose_volume = dose_volume.reshape((z_dim, y_dim, x_dim))
        return dose_volume