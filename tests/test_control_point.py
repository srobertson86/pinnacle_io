"""
Tests for the ControlPoint model.
"""

import numpy as np
import pytest

from pinnacle_io.models import (
    ControlPoint,
    Beam,
    CPManager,
    MLCLeafPositions,
    WedgeContext,
)


def test_control_point_initialization():
    """Test creating a ControlPoint directly with kwargs."""
    # Test with minimal data
    control_point = ControlPoint(
        gantry=45.0,
        couch=0.0,
        collimator=90.0,
        left_jaw_position=-10.0,
        right_jaw_position=10.0,
        top_jaw_position=10.0,
        bottom_jaw_position=-10.0,
        weight=1.0,
    )

    assert control_point.gantry == 45.0
    assert control_point.couch == 0.0
    assert control_point.collimator == 90.0
    assert control_point.left_jaw_position == -10.0
    assert control_point.right_jaw_position == 10.0
    assert control_point.top_jaw_position == 10.0
    assert control_point.bottom_jaw_position == -10.0
    assert control_point.weight == 1.0
    assert control_point.beam is None
    assert control_point.cp_manager is None
    assert control_point._mlc_leaf_positions is None
    assert control_point.wedge_context is None


def test_control_point_with_mlc_leaf_positions():
    """Test ControlPoint with MLCLeafPositions."""
    # Create MLC leaf positions (60 leaves with X1, X2 positions)
    mlc_positions = np.zeros((60, 2))
    # Set some leaf positions
    mlc_positions[20:40, 0] = -5.0  # X1 positions for leaves 20-40
    mlc_positions[20:40, 1] = 5.0   # X2 positions for leaves 20-40

    # Test creating with mlc_leaf_positions as numpy array
    control_point = ControlPoint(gantry=0.0, mlc_leaf_positions={'points': mlc_positions})

    assert control_point.has_mlc is True
    assert control_point.mlc_leaf_positions is not None
    assert isinstance(control_point.mlc_leaf_positions, np.ndarray)
    assert control_point.mlc_leaf_positions.shape == (60, 2)
    assert np.all(control_point.mlc_leaf_positions[20:40, 0] == -5.0)
    assert np.all(control_point.mlc_leaf_positions[20:40, 1] == 5.0)

    # Test creating with MLCLeafPositions object
    mlc_leaf_positions = MLCLeafPositions(points=mlc_positions)
    control_point2 = ControlPoint(gantry=0.0, mlc_leaf_positions=mlc_leaf_positions)

    assert control_point2.has_mlc is True
    assert control_point2.mlc_leaf_positions is not None
    assert np.all(control_point2.mlc_leaf_positions == mlc_positions)

    # Test creating with dictionary
    control_point3 = ControlPoint(
        gantry=0.0, mlc_leaf_positions={"points": mlc_positions}
    )

    assert control_point3.has_mlc is True
    assert control_point3.mlc_leaf_positions is not None
    assert np.all(control_point3.mlc_leaf_positions == mlc_positions)

    # Test setting mlc_leaf_positions to None
    control_point.mlc_leaf_positions = None
    assert control_point.has_mlc is False
    assert control_point.mlc_leaf_positions is None


def test_control_point_with_wedge_context():
    """Test ControlPoint with WedgeContext."""
    # Create a control point with a wedge context
    control_point = ControlPoint(
        gantry=0.0,
        wedge_context=WedgeContext(wedge_name="WEDGE45", angle="45", orientation="IN"),
    )

    assert control_point.wedge_context is not None
    assert control_point.wedge_context.wedge_name == "WEDGE45"
    assert control_point.wedge_context.angle == "45"
    assert control_point.wedge_context.orientation == "IN"
    assert control_point.wedge_context.control_point is control_point


def test_control_point_beam_relationship():
    """Test ControlPoint relationship with Beam."""
    # Create a beam
    beam = Beam(name="BEAM1", beam_number=1)

    # Create a control point with relationship to beam
    control_point = ControlPoint(gantry=0.0, beam=beam)

    # Verify beam relationship
    assert control_point.beam is beam
    assert control_point.beam_id == beam.id
    assert control_point in beam.control_point_list


def test_control_point_cp_manager_relationship():
    """Test ControlPoint relationship with CPManager."""
    # Create a CPManager
    cp_manager = CPManager(number_of_control_points=2)

    # Create control points with relationship to CPManager
    control_point1 = ControlPoint(gantry=0.0, cp_manager=cp_manager)

    control_point2 = ControlPoint(gantry=180.0, cp_manager=cp_manager)

    # Verify CPManager relationship
    assert control_point1.cp_manager is cp_manager
    assert control_point1.cp_manager_id == cp_manager.id
    assert control_point1 in cp_manager.control_point_list
    assert control_point2 in cp_manager.control_point_list
    assert len(cp_manager.control_point_list) == 2


def test_get_jaw_positions():
    """Test the get_jaw_positions method."""
    control_point = ControlPoint(
        left_jaw_position=-10.0,
        right_jaw_position=10.0,
        top_jaw_position=15.0,
        bottom_jaw_position=-15.0,
    )

    jaw_positions = control_point.get_jaw_positions()
    assert isinstance(jaw_positions, tuple)
    assert len(jaw_positions) == 4
    assert jaw_positions == (-10.0, 10.0, 15.0, -15.0)


def test_get_field_size():
    """Test the get_field_size method."""
    control_point = ControlPoint(
        left_jaw_position=-10.0,
        right_jaw_position=10.0,
        top_jaw_position=15.0,
        bottom_jaw_position=-15.0,
    )

    field_size = control_point.get_field_size()
    assert isinstance(field_size, tuple)
    assert len(field_size) == 2
    assert field_size == (20.0, 30.0)  # (right - left, top - bottom)


def test_control_point_repr():
    """Test the __repr__ method."""
    # Create a control point with known values
    control_point = ControlPoint(
        id=42,
        index=0,
        gantry=45.0, 
        collimator=90.0, 
        couch=0.0
    )
    
    # Verify the __repr__ output matches the expected format
    expected_repr = "<ControlPoint(id=42, index=0, gantry=45.0, collimator=90.0, couch=0.0)>"
    assert repr(control_point) == expected_repr


def test_optional_fields():
    """Test initialization and access of all optional fields."""
    control_point = ControlPoint(
        weight_locked=1,
        percent_of_arc=45.0,
        has_shared_modifier_list=0,
        mlc_trans_for_display=2.5,
        c_arm_angle=30.0,
        target_projection_valid=1,
        dose_rate=600.0,
        delivery_time=15.0,
        odm="CUSTOM_ODM",
        dose_vector="1,2,3,4",
        cumulative_meterset_weight=0.5
    )

    # Verify all optional fields
    assert control_point.weight_locked == 1
    assert control_point.percent_of_arc == 45.0
    assert control_point.has_shared_modifier_list == 0
    assert control_point.mlc_trans_for_display == 2.5
    assert control_point.c_arm_angle == 30.0
    assert control_point.target_projection_valid == 1
    assert control_point.dose_rate == 600.0
    assert control_point.delivery_time == 15.0
    assert control_point.odm == "CUSTOM_ODM"
    assert control_point.dose_vector == "1,2,3,4"
    assert control_point.cumulative_meterset_weight == 0.5


def test_null_optional_fields():
    """Test that all optional fields can be null."""
    control_point = ControlPoint()  # Create with no arguments
    
    # Verify all optional fields are None
    assert control_point.gantry is None
    assert control_point.couch is None
    assert control_point.collimator is None
    assert control_point.weight is None
    assert control_point.weight_locked is None
    assert control_point.percent_of_arc is None
    assert control_point.has_shared_modifier_list is None
    assert control_point.mlc_trans_for_display is None
    assert control_point.c_arm_angle is None
    assert control_point.target_projection_valid is None
    assert control_point.dose_rate is None
    assert control_point.delivery_time is None
    assert control_point.odm is None
    assert control_point.dose_vector is None
    assert control_point.cumulative_meterset_weight is None


def test_invalid_mlc_positions():
    """Test MLCLeafPositions with invalid data."""
    # Test with wrong number of leaves
    invalid_mlc_data = np.zeros((40, 2))
    with pytest.raises(ValueError) as exc_info:
        ControlPoint(mlc_leaf_positions=invalid_mlc_data)
    assert "MLC positions must be a 60x2 array" in str(exc_info.value)
    
    # Test with wrong dimensions
    invalid_mlc_data = np.zeros((60, 3))
    with pytest.raises(ValueError) as exc_info:
        ControlPoint(mlc_leaf_positions=invalid_mlc_data)
    assert "MLC positions must be a 60x2 array" in str(exc_info.value)
    
    # Test with non-array that can be converted
    convertible_data = [[0, 0]] * 60  # List of lists that can be converted to array
    control_point = ControlPoint(mlc_leaf_positions=convertible_data)
    assert control_point.mlc_leaf_positions.shape == (60, 2)
    
    # Test with non-convertible data
    with pytest.raises(TypeError) as exc_info:
        ControlPoint(mlc_leaf_positions="invalid data")
    assert "Could not convert input to numpy array" in str(exc_info.value)


def test_invalid_jaw_positions():
    """Test invalid jaw position combinations."""
    # Test left jaw greater than right jaw
    with pytest.raises(ValueError):
        ControlPoint(
            left_jaw_position=10.0,
            right_jaw_position=-10.0,
            top_jaw_position=10.0,
            bottom_jaw_position=10.0
        ).get_field_size()
    
    # Test bottom jaw greater than top jaw
    with pytest.raises(ValueError):
        ControlPoint(
            left_jaw_position=-10.0,
            right_jaw_position=10.0,
            top_jaw_position=-10.0,
            bottom_jaw_position=10.0
        ).get_field_size()
