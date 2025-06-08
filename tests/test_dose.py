"""
Tests for the Dose model, reader, and writer.
"""
from pathlib import Path
import pytest
import numpy as np

from pinnacle_io.models import Dose, DoseGrid, Trial, Beam
from pinnacle_io.readers.dose_reader import DoseReader
from pinnacle_io.writers.dose_writer import DoseWriter


def test_dose_initialization():
    """Test creating a Dose directly with kwargs."""
    # Create a test trial first
    trial = Trial(
        trial_id=1,
        trial_name="Test Trial"
    )
    
    # Create a dose grid for testing and associate it with the trial
    dose_grid = DoseGrid(
        dimension_x=100,
        dimension_y=100,
        dimension_z=50,
        voxel_size_x=2.0,
        voxel_size_y=2.0,
        voxel_size_z=3.0,
        origin_x=-100.0,
        origin_y=-100.0,
        origin_z=0.0,
        trial=trial  # Associate with trial
    )
    
    # Create a test beam and associate it with the trial
    beam = Beam(
        beam_number=1,
        name="Beam 1",
        description="Test beam",
        dose_volume_file="plan.Trial.binary.1",
        trial=trial  # Associate with trial
    )
    
    # Create sample pixel data
    pixel_data = np.random.rand(100, 100, 50).astype(np.float32)
    
    # Test with all parameters
    dose = Dose(
        dose_id="1",
        dose_type="PHYSICAL",
        dose_unit="GY",
        datatype=1,
        bitpix=32,
        bytes_pix=4,
        vol_max=10.5,
        vol_min=0.0,
        dose_comment="Test dose",
        dose_grid_scaling=1.0,
        dose_summation_type="PLAN",
        referenced_plan_id="Plan1",
        referenced_beam_numbers=[1, 2, 3],
        dose_grid=dose_grid,
        dose_grid_id=dose_grid.id,  # Set the foreign key
        beam=beam,
        pixel_data=pixel_data,
        non_existent_field="This should be ignored"
    )
    
    # Test properties
    assert dose.dose_id == "1"
    assert dose.dose_type == "PHYSICAL"
    assert dose.dose_unit == "GY"
    assert dose.datatype == 1
    assert dose.bitpix == 32
    assert dose.bytes_pix == 4
    assert dose.vol_max == 10.5
    assert dose.vol_min == 0.0
    assert dose.dose_comment == "Test dose"
    assert dose.dose_grid_scaling == 1.0
    assert dose.dose_summation_type == "PLAN"
    assert dose.referenced_plan_id == "Plan1"
    assert dose.referenced_beam_numbers == [1, 2, 3]
    assert dose.dose_grid == dose_grid
    assert dose.beam == beam
    assert np.array_equal(dose.pixel_data, pixel_data)
    assert not hasattr(dose, "non_existent_field")
    
    # Test getter methods
    assert dose.get_dose_dimensions() == (100, 100, 50)
    assert dose.get_dose_grid_resolution() == (2.0, 2.0, 3.0)
    assert dose.get_dose_grid_origin() == (-100.0, -100.0, 0.0)
    
    # Test slice operations
    # Create a test slice with known values
    slice_data = np.zeros((100, 100), dtype=np.float32)
    # Set some non-zero values
    slice_data[0, 0] = 1.0
    slice_data[50, 50] = 2.0
    slice_data[99, 99] = 3.0
    
    slice_index = 25
    dose.set_slice_data(slice_index, slice_data)
    
    # Get the slice back and verify the values
    retrieved_slice = dose.get_slice_data(slice_index)
    assert retrieved_slice is not None
    assert retrieved_slice[0, 0] == 1.0
    assert retrieved_slice[50, 50] == 2.0
    assert retrieved_slice[99, 99] == 3.0
    
    # Test point access
    x, y, z = 50, 50, 25
    expected_value = float(pixel_data[x, y, z] * dose.dose_grid_scaling)
    assert np.allclose(dose.get_dose_value(x, y, z), expected_value, rtol=1e-6, atol=1e-6)


def test_dose_beam_relationship():
    """Test the relationship between Dose and Beam."""
    # Create a test trial first
    trial = Trial(trial_id=1, trial_name="Test Trial")
    
    # Create a dose grid for testing and associate it with the trial
    dose_grid = DoseGrid(
        dimension_x=100,
        dimension_y=100,
        dimension_z=50,
        voxel_size_x=2.0,
        voxel_size_y=2.0,
        voxel_size_z=3.0,
        origin_x=-100.0,
        origin_y=-100.0,
        origin_z=0.0,
        trial=trial  # Associate with trial
    )
    
    # Create a beam and associate it with the trial
    beam = Beam(
        beam_number=1,
        name="Test Beam",
        description="Test beam description",
        dose_volume_file="plan.Trial.binary.1",
        trial=trial
    )
    
    # Create a dose and set up relationships
    dose = Dose(dose_id="1", dose_grid=dose_grid, beam=beam)

    # Test the relationship
    assert dose.beam == beam
    assert beam.dose == dose


def test_dose_grid_relationship():
    """Test the relationship between Dose and DoseGrid."""
    # Create a test trial first
    trial = Trial(trial_id=1, trial_name="Test Trial")
    
    # Create a dose grid and associate it with the trial
    dose_grid = DoseGrid(
        dimension_x=100,
        dimension_y=100,
        dimension_z=50,
        voxel_size_x=2.0,
        voxel_size_y=2.0,
        voxel_size_z=3.0,
        origin_x=-100.0,
        origin_y=-100.0,
        origin_z=0.0,
        trial=trial  # Associate with trial
    )
    
    # Create a test beam and associate it with the trial
    beam = Beam(
        beam_number=1,
        name="Test Beam",
        description="Test beam description",
        dose_volume_file="plan.Trial.binary.1",
        trial=trial
    )

    # Create a dose and set up relationships
    dose = Dose(dose_id="1", dose_grid=dose_grid, beam=beam)

    # Test the relationship
    assert dose.dose_grid == dose_grid
    # The dose should be in the doses list, and there should be at least one dose
    assert len(dose_grid.dose_list) >= 1
    assert dose in dose_grid.dose_list


def test_read_beam_dose():
    """Test reading a beam dose from a binary file."""
    # Create a test trial first
    trial = Trial(trial_id=1, trial_name="Test Trial")
    
    # Create a test dose grid and associate it with the trial
    dose_grid = DoseGrid(
        dimension_x=20,
        dimension_y=20,
        dimension_z=10,
        voxel_size_x=2.0,
        voxel_size_y=2.0,
        voxel_size_z=3.0,
        origin_x=-20.0,
        origin_y=-20.0,
        origin_z=0.0,
        trial=trial
    )
    
    # Create a test beam with required attributes
    beam = Beam(
        beam_number=1,
        name="Test Beam",
        description="Test beam description",
        dose_volume="test:1",  # This will be used to generate dose_volume_file
        trial=trial
    )
    
    # Create a test binary dose file
    test_data_dir = Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/Plan_0'
    test_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a test binary file with the expected name
    dose_file = test_data_dir / f"plan.Trial.binary.{beam.beam_number:03d}"
    with open(dose_file, 'wb') as f:
        # Write some test data (20*20*10 floats = 16000 bytes)
        f.write(np.zeros((20*20*10), dtype=np.float32).tobytes())
    
    # Read the beam dose
    test_data_dir = Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/Plan_0'
    dose = DoseReader.read_beam_dose(test_data_dir, beam, dose_grid)
    
    # Verify the dose properties
    assert dose is not None
    assert isinstance(dose, Dose)
    assert dose.dose_type == "PHYSICAL"
    assert dose.dose_unit == "CGY"
    assert dose.dose_grid == dose_grid
    assert dose.beam == beam
    assert dose.pixel_data is not None
    assert dose.pixel_data.shape == (10, 20, 20)  # z, y, x order from reader


def test_read_trial_dose():
    """Test reading a trial dose (sum of beam doses)."""
    # Create a test trial
    trial = Trial(trial_id=1, trial_name="Test Trial")
    
    # Set up a test dose grid and associate it with the trial
    trial.dose_grid = DoseGrid(
        dimension_x=20,
        dimension_y=20,
        dimension_z=10,
        voxel_size_x=2.0,
        voxel_size_y=2.0,
        voxel_size_z=3.0,
        origin_x=-20.0,
        origin_y=-20.0,
        origin_z=0.0,
        trial=trial
    )
    
    # Create test beams with required attributes
    beam1 = Beam(
        beam_number=1, 
        name="Beam 1", 
        dose_volume="test:1",
        trial=trial
    )
    beam2 = Beam(
        beam_number=2, 
        name="Beam 2", 
        dose_volume="test:2",
        trial=trial
    )
    trial.beam_list = [beam1, beam2]
    
    # Create test binary dose files
    test_data_dir = Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/Plan_0'
    test_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create test binary files with the expected names
    for beam in [beam1, beam2]:
        dose_file = test_data_dir / f"plan.Trial.binary.{beam.beam_number:03d}"
        with open(dose_file, 'wb') as f:
            # Write some test data (20*20*10 floats = 16000 bytes)
            # Use different values for each beam to test summation
            data = np.ones((20*20*10), dtype=np.float32) * beam.beam_number
            f.write(data.tobytes())
    
    # Read the trial dose
    test_data_dir = Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/Plan_0'
    dose = DoseReader.read(test_data_dir, trial)
    
    # Verify the dose properties
    assert dose is not None
    assert isinstance(dose, Dose)
    assert dose.dose_summation_type == "PLAN"
    # TODO: Add more assertions once the implementation is complete


def test_dose_writer():
    """Test the DoseWriter (currently not implemented)."""
    dose = Dose(dose_id="1")
    with pytest.raises(NotImplementedError):
        DoseWriter.write(dose, "/path/to/dose")


def test_dose_repr():
    """Test the string representation of Dose."""
    # Create a test trial first
    trial = Trial(trial_id=1, trial_name="Test Trial")
    
    # Create a dose grid and associate it with the trial
    dose_grid = DoseGrid(
        dimension_x=100,
        dimension_y=100,
        dimension_z=50,
        voxel_size_x=2.0,
        voxel_size_y=2.0,
        voxel_size_z=3.0,
        origin_x=-100.0,
        origin_y=-100.0,
        origin_z=0.0,
        trial=trial  # Associate with trial
    )
    
    # Create a dose with required relationships and test data
    dose = Dose(
        dose_id="TestDose123", 
        dose_type="PHYSICAL", 
        dose_grid=dose_grid,
        pixel_data=np.zeros((100, 100, 50), dtype=np.float32)  # Add pixel data to test dimensions
    )
    
    # Get the string representation
    repr_str = repr(dose)
    
    # Verify the format and content
    expected_start = "<Dose(id='TestDose123'"
    expected_type = "type='PHYSICAL'"
    expected_dims = "dimensions=(100, 100, 50)"
    
    assert repr_str.startswith("<Dose(")
    assert repr_str.endswith(")>")
    assert expected_start in repr_str
    assert expected_type in repr_str
    assert expected_dims in repr_str
    
    # Test with a different dose type and ID
    dose_grid.dimension_x = 50
    dose_grid.dimension_y = 50
    dose_grid.dimension_z = 25
    pixel_data = np.zeros((50, 50, 25), dtype=np.float32)
    dose2 = Dose(
        dose_id="AnotherDose", 
        dose_type="EFFECTIVE", 
        dose_grid=dose_grid,
        pixel_data=pixel_data
    )
    
    repr_str2 = repr(dose2)
    assert "id='AnotherDose'" in repr_str2
    assert "type='EFFECTIVE'" in repr_str2
    assert "dimensions=(50, 50, 25)" in repr_str2
