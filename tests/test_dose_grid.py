"""
Unit tests for the DoseGrid model.
"""
from pathlib import Path

from pinnacle_io.models import DoseGrid, Trial, Dose, VoxelSize, Dimension, Coordinate
from pinnacle_io.readers.trial_reader import TrialReader


def test_init_with_kwargs():
    """Test initializing a DoseGrid with keyword arguments."""
    dose_grid = DoseGrid(
        voxel_size_x=0.3,
        voxel_size_y=0.3, 
        voxel_size_z=0.3,
        dimension_x=93,
        dimension_y=110,
        dimension_z=89,
        origin_x=-14.9044,
        origin_y=-17.5729,
        origin_z=-10.7747,
        vol_rot_delta_x=0,
        vol_rot_delta_y=0,
        vol_rot_delta_z=0,
        display_2d=1,
        dose_summation_type=1
    )
    
    assert dose_grid.voxel_size_x == 0.3
    assert dose_grid.voxel_size_y == 0.3
    assert dose_grid.voxel_size_z == 0.3
    assert dose_grid.dimension_x == 93
    assert dose_grid.dimension_y == 110
    assert dose_grid.dimension_z == 89
    assert dose_grid.origin_x == -14.9044
    assert dose_grid.origin_y == -17.5729
    assert dose_grid.origin_z == -10.7747
    assert dose_grid.vol_rot_delta_x == 0
    assert dose_grid.vol_rot_delta_y == 0
    assert dose_grid.vol_rot_delta_z == 0
    assert dose_grid.display_2d == 1
    assert dose_grid.dose_summation_type == 1


def test_init_with_spatial_objects():
    """Test initializing a DoseGrid with spatial type objects."""
    dose_grid = DoseGrid(
        voxel_size=VoxelSize(0.3, 0.3, 0.3),
        dimension=Dimension(93, 110, 89),
        origin=Coordinate(-14.9044, -17.5729, -10.7747),
        vol_rot_delta=Coordinate(0, 0, 0),
        display_2d=1,
        dose_summation_type=1
    )
    
    assert dose_grid.voxel_size_x == 0.3
    assert dose_grid.voxel_size_y == 0.3
    assert dose_grid.voxel_size_z == 0.3
    assert dose_grid.dimension_x == 93
    assert dose_grid.dimension_y == 110
    assert dose_grid.dimension_z == 89
    assert dose_grid.origin_x == -14.9044
    assert dose_grid.origin_y == -17.5729
    assert dose_grid.origin_z == -10.7747
    assert dose_grid.vol_rot_delta_x == 0
    assert dose_grid.vol_rot_delta_y == 0
    assert dose_grid.vol_rot_delta_z == 0
    
    # Test the spatial type properties
    assert isinstance(dose_grid.voxel_size, VoxelSize)
    assert isinstance(dose_grid.dimension, Dimension)
    assert isinstance(dose_grid.origin, Coordinate)
    assert isinstance(dose_grid.vol_rot_delta, Coordinate)


def test_init_with_dict_objects():
    """Test initializing a DoseGrid with dictionary objects."""
    dose_grid = DoseGrid(
        voxel_size={"x": 0.3, "y": 0.3, "z": 0.3},
        dimension={"x": 93, "y": 110, "z": 89},
        origin={"x": -14.9044, "y": -17.5729, "z": -10.7747},
        vol_rot_delta={"x": 0, "y": 0, "z": 0},
        display_2d=1,
        dose_summation_type=1
    )
    
    assert dose_grid.voxel_size_x == 0.3
    assert dose_grid.voxel_size_y == 0.3
    assert dose_grid.voxel_size_z == 0.3
    assert dose_grid.dimension_x == 93
    assert dose_grid.dimension_y == 110
    assert dose_grid.dimension_z == 89
    assert dose_grid.origin_x == -14.9044
    assert dose_grid.origin_y == -17.5729
    assert dose_grid.origin_z == -10.7747
    assert dose_grid.vol_rot_delta_x == 0
    assert dose_grid.vol_rot_delta_y == 0
    assert dose_grid.vol_rot_delta_z == 0


def test_init_with_pascal_case_dict_objects():
    """Test initializing a DoseGrid with PascalCase dictionary objects."""
    dose_grid = DoseGrid(
        VoxelSize={"X": 0.3, "Y": 0.3, "Z": 0.3},
        Dimension={"X": 93, "Y": 110, "Z": 89},
        Origin={"X": -14.9044, "Y": -17.5729, "Z": -10.7747},
        VolRotDelta={"X": 0, "Y": 0, "Z": 0},
        display_2d=1,
        dose_summation_type=1
    )
    
    assert dose_grid.voxel_size_x == 0.3
    assert dose_grid.voxel_size_y == 0.3
    assert dose_grid.voxel_size_z == 0.3
    assert dose_grid.dimension_x == 93
    assert dose_grid.dimension_y == 110
    assert dose_grid.dimension_z == 89
    assert dose_grid.origin_x == -14.9044
    assert dose_grid.origin_y == -17.5729
    assert dose_grid.origin_z == -10.7747
    assert dose_grid.vol_rot_delta_x == 0
    assert dose_grid.vol_rot_delta_y == 0
    assert dose_grid.vol_rot_delta_z == 0


def test_spatial_properties():
    """Test that spatial properties return the correct spatial type objects."""
    dose_grid = DoseGrid(
        voxel_size_x=0.3,
        voxel_size_y=0.3,
        voxel_size_z=0.3,
        dimension_x=93,
        dimension_y=110,
        dimension_z=89,
        origin_x=-14.9044,
        origin_y=-17.5729,
        origin_z=-10.7747,
        vol_rot_delta_x=0,
        vol_rot_delta_y=0,
        vol_rot_delta_z=0,
    )
    
    # Test voxel_size property
    voxel_size = dose_grid.voxel_size
    assert isinstance(voxel_size, VoxelSize)
    assert voxel_size.x == 0.3
    assert voxel_size.y == 0.3
    assert voxel_size.z == 0.3
    
    # Test dimension property
    dimension = dose_grid.dimension
    assert isinstance(dimension, Dimension)
    assert dimension.x == 93
    assert dimension.y == 110
    assert dimension.z == 89
    
    # Test origin property
    origin = dose_grid.origin
    assert isinstance(origin, Coordinate)
    assert origin.x == -14.9044
    assert origin.y == -17.5729
    assert origin.z == -10.7747
    
    # Test vol_rot_delta property
    vol_rot_delta = dose_grid.vol_rot_delta
    assert isinstance(vol_rot_delta, Coordinate)
    assert vol_rot_delta.x == 0
    assert vol_rot_delta.y == 0
    assert vol_rot_delta.z == 0


def test_relationship_with_trial():
    """Test the relationship between DoseGrid and Trial."""
    trial = Trial(trial_id=1, trial_name="Test Trial")
    dose_grid = DoseGrid(trial=trial)
    
    assert dose_grid.trial == trial
    assert dose_grid.trial_id == trial.id
    assert trial.dose_grid == dose_grid


def test_relationship_with_doses():
    """Test the relationship between DoseGrid and Dose."""
    dose_grid = DoseGrid()
    
    # Create some test doses
    dose1 = Dose(dose_id="Dose1", dose_grid=dose_grid)
    dose2 = Dose(dose_id="Dose2", dose_grid=dose_grid)
    
    # Check the relationship
    assert len(dose_grid.dose_list) == 2
    assert dose_grid.dose_list[0] == dose1
    assert dose_grid.dose_list[1] == dose2
    assert dose1.dose_grid == dose_grid
    assert dose2.dose_grid == dose_grid
    assert dose1.dose_grid_id == dose_grid.id
    assert dose2.dose_grid_id == dose_grid.id


def test_from_plan_trial_file():
    """Test loading DoseGrid data from a plan.Trial file."""
    plan_path = Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/Plan_0'
    trials = TrialReader.read(str(plan_path))
    
    # Verify the first trial has a dose grid with expected values
    assert len(trials) > 0
    trial = trials[0]
    
    assert hasattr(trial, 'dose_grid')
    dose_grid = trial.dose_grid
    
    # Check that values match those in the plan.Trial file
    assert dose_grid.voxel_size_x == 0.3
    assert dose_grid.voxel_size_y == 0.3
    assert dose_grid.voxel_size_z == 0.3
    assert dose_grid.dimension_x == 93
    assert dose_grid.dimension_y == 110
    assert dose_grid.dimension_z == 89
    assert dose_grid.origin_x == -14.9044
    assert dose_grid.origin_y == -17.5729
    assert dose_grid.origin_z == -10.7747
    assert dose_grid.vol_rot_delta_x == 0
    assert dose_grid.vol_rot_delta_y == 0
    assert dose_grid.vol_rot_delta_z == 0
    assert dose_grid.display_2d == 1
    assert dose_grid.dose_summation_type == 1


def test_partial_vector_initialization():
    """Test initializing with partial vector data."""
    # Test with some vector components missing
    dose_grid = DoseGrid(
        voxel_size={"x": 0.3, "y": 0.3},  # Missing z
        dimension=Dimension(93, 110, 89), # 0 and None throw errors
        origin_x=-14.9044,  # Individual components
        origin_y=-17.5729,
        vol_rot_delta=None  # None for entire vector
    )
    
    assert dose_grid.voxel_size_x == 0.3
    assert dose_grid.voxel_size_y == 0.3
    assert dose_grid.voxel_size_z is None  # Not set
    assert dose_grid.dimension_x == 93
    assert dose_grid.dimension_y == 110
    assert dose_grid.dimension_z == 89
    assert dose_grid.origin_x == -14.9044
    assert dose_grid.origin_y == -17.5729
    assert dose_grid.origin_z is None  # Not set
    assert dose_grid.vol_rot_delta_x is None  # Not set
    assert dose_grid.vol_rot_delta_y is None  # Not set
    assert dose_grid.vol_rot_delta_z is None  # Not set


def test_complete_relationship_chain():
    """Test the complete relationship chain from Trial to DoseGrid to Dose."""
    # Create a trial
    trial = Trial(trial_id=1, trial_name="Test Trial")
    
    # Create a dose grid linked to the trial
    dose_grid = DoseGrid(trial=trial)
    
    # Create doses linked to the dose grid
    dose1 = Dose(dose_id="Dose1", dose_grid=dose_grid)
    dose2 = Dose(dose_id="Dose2", dose_grid=dose_grid)
    
    # Link a dose directly to the trial (plan dose)
    trial_dose = Dose(dose_id="TrialDose", trial=trial)
    
    # Verify relationships
    assert trial.dose_grid == dose_grid
    assert dose_grid.trial == trial
    assert dose1 in dose_grid.dose_list
    assert dose2 in dose_grid.dose_list
    assert dose1.dose_grid == dose_grid
    assert dose2.dose_grid == dose_grid
    assert trial.dose == trial_dose
    assert trial_dose.trial == trial


def test_mixed_case_parameters():
    """Test initializing a DoseGrid with a mix of snake_case and PascalCase parameters."""
    dose_grid = DoseGrid(
        voxel_size_x=0.3,  # snake_case individual component
        VoxelSize={"Y": 0.3},  # PascalCase dict with PascalCase key
        dimension={"z": 89},  # snake_case dict with snake_case key
        Origin={"X": -14.9044, "y": -17.5729},  # PascalCase dict with mixed keys
        vol_rot_delta_z=0  # snake_case individual component
    )
    
    assert dose_grid.voxel_size_x == 0.3
    assert dose_grid.voxel_size_y == 0.3
    assert dose_grid.voxel_size_z is None # Not set
    assert dose_grid.dimension_x is None  # Not set
    assert dose_grid.dimension_y is None  # Not set
    assert dose_grid.dimension_z == 89
    assert dose_grid.origin_x == -14.9044
    assert dose_grid.origin_y == -17.5729
    assert dose_grid.origin_z is None  # Not set
    assert dose_grid.vol_rot_delta_x is None  # Not set
    assert dose_grid.vol_rot_delta_y is None  # Not set
    assert dose_grid.vol_rot_delta_z == 0


def test_empty_vector_parameters():
    """Test initializing a DoseGrid with empty vector parameters."""
    dose_grid = DoseGrid(
        voxel_size={},  # Empty dict
        dimension=Dimension(1, 1, 1),  # Non-zero vector
        origin=None,  # None
        vol_rot_delta={}  # Empty dict
    )
    
    # Check that default values are used
    assert dose_grid.voxel_size_x is None  # Not set by empty dict
    assert dose_grid.voxel_size_y is None  # Not set by empty dict
    assert dose_grid.voxel_size_z is None  # Not set by empty dict
    assert dose_grid.dimension_x == 1
    assert dose_grid.dimension_y == 1
    assert dose_grid.dimension_z == 1
    assert dose_grid.origin_x is None  # Not set by None
    assert dose_grid.origin_y is None  # Not set by None
    assert dose_grid.origin_z is None  # Not set by None
    assert dose_grid.vol_rot_delta_x is None  # Not set by empty dict
    assert dose_grid.vol_rot_delta_y is None  # Not set by empty dict
    assert dose_grid.vol_rot_delta_z is None  # Not set by empty dict


def test_dose_grid_repr():
    """Test the string representation of a DoseGrid with different combinations of trial and dimension."""
    # Test with trial and dimension
    trial = Trial(trial_id=1, name="Test Trial")
    dose_grid = DoseGrid(
        id=42,
        trial=trial,
        dimension=Dimension(93, 110, 89)
    )
    expected_repr = "<DoseGrid(id=42, trial='Test Trial', dimension=(93, 110, 89))>"
    assert repr(dose_grid) == expected_repr

    # Test with trial but no dimension
    dose_grid = DoseGrid(id=42, trial=trial)
    expected_repr = "<DoseGrid(id=42, trial='Test Trial', dimension=(0, 0, 0))>"
    assert repr(dose_grid) == expected_repr

    # Test with dimension but no trial
    dose_grid = DoseGrid(
        id=42,
        dimension=Dimension(93, 110, 89)
    )
    expected_repr = "<DoseGrid(id=42, trial='', dimension=(93, 110, 89))>"
    assert repr(dose_grid) == expected_repr

    # Test with neither trial nor dimension
    dose_grid = DoseGrid(id=42)
    expected_repr = "<DoseGrid(id=42, trial='', dimension=(0, 0, 0))>"
    assert repr(dose_grid) == expected_repr
