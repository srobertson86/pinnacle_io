"""
Tests for the base SQLAlchemy models.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from pinnacle_io.models.types import JsonList, VoxelSize, Coordinate, Dimension
from tests.conftest import TestModel, TestVersionedModel


def test_pinnacle_base_initialization():
    """Test basic initialization of PinnacleBase model."""
    # Create a new instance
    model = TestModel(
        name="Test Model",
        description="Test Description"
    )
    
    # Check attributes
    assert model.name == "Test Model"
    assert model.description == "Test Description"
    assert model.id is None  # Not persisted yet
    assert model.created_at is not None
    assert model.updated_at is not None
    assert model.created_at.tzinfo is not None  # Timezone-aware
    assert model.updated_at.tzinfo is not None  # Timezone-aware
    assert model.created_at.tzinfo == timezone.utc  # UTC timezone
    assert model.updated_at.tzinfo == timezone.utc  # UTC timezone

def test_pinnacle_base_save_to_database(db_session: Session):
    """Test saving PinnacleBase model to database."""
    # Create and save model
    model = TestModel(name="Database Test")
    db_session.add(model)
    db_session.commit()
    
    # Verify ID was assigned
    assert model.id is not None
    
    # Retrieve from database
    db_model = db_session.query(TestModel).filter_by(id=model.id).first()
    assert db_model is not None
    assert db_model.name == "Database Test"

def test_versioned_base_initialization():
    """Test initialization of VersionedBase model."""
    # Create a new instance
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    model = TestVersionedModel(
        name="Versioned Test",
        login_name="testuser",
        create_time_stamp=now,
        write_time_stamp=now,
        last_modified_time_stamp=now
    )
    
    # Check attributes
    assert model.name == "Versioned Test"
    assert model.login_name == "testuser"
    assert model.create_time_stamp == now
    assert model.write_time_stamp == now
    assert model.last_modified_time_stamp == now

def test_json_list_type():
    """Test the JsonList custom type."""
    # Test with list
    test_list = [1, 2, 3, "test"]
    json_list = JsonList()
    
    # Test process_bind_param
    json_str = json_list.process_bind_param(test_list, None)
    assert isinstance(json_str, str)
    
    # Test process_result_value
    result = json_list.process_result_value(json_str, None)
    assert result == test_list
    
    # Test with None
    assert json_list.process_bind_param(None, None) is None
    assert json_list.process_result_value(None, None) is None

def test_voxel_size_initialization():
    """Test VoxelSize class initialization and methods."""
    # Test initialization with values
    vs = VoxelSize(1.0, 2.0, 3.0)
    assert vs.x == 1.0
    assert vs.y == 2.0
    assert vs.z == 3.0
    
    # Test volume calculation
    assert vs.volume() == 6.0
    
    # Test validation (negative values not allowed)
    try:
        VoxelSize(-1.0, 1.0, 1.0)
        assert False, "Should raise ValueError for negative values"
    except ValueError:
        pass


def test_dimension_initialization():
    """Test Dimension class initialization and methods."""
    # Test initialization with values
    dim = Dimension(10, 20, 30)
    assert dim.x == 10
    assert dim.y == 20
    assert dim.z == 30
    
    # Test num_voxels calculation
    assert dim.num_voxels() == 10 * 20 * 30
    
    # Test validation (non-positive values not allowed)
    try:
        Dimension(0, 1, 1)
        assert False, "Should raise ValueError for non-positive values"
    except ValueError:
        pass


def test_coordinate_operations():
    """Test Coordinate class operations."""
    c1 = Coordinate(1.0, 2.0, 3.0)
    c2 = Coordinate(4.0, 5.0, 6.0)
    
    # Test distance calculation
    distance = c1.distance_to(c2)
    expected_distance = (3.0**2 + 3.0**2 + 3.0**2)**0.5
    assert abs(distance - expected_distance) < 1e-10
    
    # Test addition
    c3 = c1 + c2
    assert c3.x == 5.0
    assert c3.y == 7.0
    assert c3.z == 9.0
    
    # Test scalar multiplication
    c4 = c1 * 2
    assert c4.x == 2.0
    assert c4.y == 4.0
    assert c4.z == 6.0
