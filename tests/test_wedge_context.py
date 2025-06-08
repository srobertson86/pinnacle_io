"""
Unit tests for WedgeContext class.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from pinnacle_io.models.wedge_context import WedgeContext
from pinnacle_io.models.control_point import ControlPoint


@pytest.fixture
def engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    WedgeContext.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Create a new database session for testing."""
    session = Session(engine)
    yield session
    session.close()


def test_wedge_context_initialization_required_fields():
    """Test initialization with only required fields."""
    wedge = WedgeContext(
        wedge_id="W1",
        wedge_number=1,
        wedge_angle=45.0,
    )
    
    assert wedge.wedge_id == "W1"
    assert wedge.wedge_number == 1
    assert wedge.wedge_angle == 45.0
    assert wedge.wedge_type is None
    assert wedge.control_point is None


def test_wedge_context_initialization_all_fields():
    """Test initialization with all fields."""
    wedge = WedgeContext(
        wedge_id="W2",
        wedge_number=2,
        wedge_angle=30.0,
        wedge_type="STANDARD",
        wedge_orientation="X",
        wedge_position="IN",
        material="STEEL",
        source_to_wedge_distance=1000.0,
        wedge_name="EDW30",
        orientation="LEFT",
        offset_origin="ISOCENTER",
        offset_distance=50.0,
        angle="30",
        min_deliverable_mu=2,
        max_deliverable_mu=999.9
    )
    
    assert wedge.wedge_id == "W2"
    assert wedge.wedge_name == "EDW30"
    assert wedge.wedge_type == "STANDARD"
    assert wedge.source_to_wedge_distance == 1000.0
    assert wedge.min_deliverable_mu == 2
    assert wedge.max_deliverable_mu == 999.9


def test_wedge_context_repr():
    """Test the string representation of WedgeContext."""
    wedge = WedgeContext(
        id=1,
        wedge_id="W3",
        wedge_number=3,
        wedge_angle=15.0,
        wedge_name="EDW15",
        angle="15",
        orientation="RIGHT"
    )
    
    expected = "<WedgeContext(id=1, name='EDW15', angle='15', orientation='RIGHT')>"
    assert repr(wedge) == expected


def test_wedge_context_relationship(session):
    """Test the relationship between WedgeContext and ControlPoint."""
    # Create a ControlPoint first
    control_point = ControlPoint()
    session.add(control_point)
    session.commit()
    
    # Create WedgeContext with relationship
    wedge = WedgeContext(
        wedge_id="W4",
        wedge_number=4,
        wedge_angle=60.0,
        control_point=control_point
    )
    session.add(wedge)
    session.commit()
    
    # Test relationship from wedge to control point
    assert wedge.control_point == control_point
    assert wedge.control_point_id == control_point.id
    
    # Test relationship from control point to wedge
    assert control_point.wedge_context == wedge


def test_wedge_context_nullable_fields():
    """Test that nullable fields can be omitted or set to None."""
    wedge = WedgeContext(
        wedge_id="W5",
        wedge_number=5,
        wedge_angle=45.0,
        wedge_type=None,
        material=None,
        source_to_wedge_distance=None
    )
    
    assert wedge.wedge_type is None
    assert wedge.material is None
    assert wedge.source_to_wedge_distance is None


def test_wedge_context_float_conversion():
    """Test numeric field type conversions."""
    wedge = WedgeContext(
        wedge_id="W7",
        wedge_number=7,
        wedge_angle="45.5",  # String that should convert to float
        source_to_wedge_distance="1000.5",  # String that should convert to float
        offset_distance=75  # Integer that should convert to float
    )
    
    assert isinstance(wedge.wedge_angle, float)
    assert wedge.wedge_angle == 45.5
    assert isinstance(wedge.source_to_wedge_distance, float)
    assert wedge.source_to_wedge_distance == 1000.5
    assert isinstance(wedge.offset_distance, float)
    assert wedge.offset_distance == 75.0