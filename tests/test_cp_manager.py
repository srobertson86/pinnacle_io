"""
Tests for the CPManager model.
"""

from pinnacle_io.models import (
    ControlPoint,
    Beam,
    CPManager,
)

def test_cp_manager_initialization():
    """Test CPManager initialization with all fields."""
    cp_manager = CPManager(
        is_gantry_start_stop_locked=1,
        is_couch_start_stop_locked=1,
        is_collimator_start_stop_locked=1,
        is_left_right_independent=1,
        is_top_bottom_independent=1,
        gantry_is_ccw=1,
        mlc_push_method="AUTO",
        jaws_conformance="INNER",
        _number_of_control_points=2
    )

    # Test all fields are set correctly
    assert cp_manager.is_gantry_start_stop_locked == 1
    assert cp_manager.is_couch_start_stop_locked == 1
    assert cp_manager.is_collimator_start_stop_locked == 1
    assert cp_manager.is_left_right_independent == 1
    assert cp_manager.is_top_bottom_independent == 1
    assert cp_manager.gantry_is_ccw == 1
    assert cp_manager.mlc_push_method == "AUTO"
    assert cp_manager.jaws_conformance == "INNER"
    assert cp_manager._number_of_control_points == 2
    assert cp_manager.control_point_list == []


def test_cp_manager_number_of_control_points():
    """Test the number_of_control_points property and setter."""
    cp_manager = CPManager(_number_of_control_points=3)
    
    # Initially no control points
    assert cp_manager.number_of_control_points == 0
    
    # Add control points
    ControlPoint(gantry=0.0, cp_manager=cp_manager)
    assert cp_manager.number_of_control_points == 1
    
    ControlPoint(gantry=180.0, cp_manager=cp_manager)
    assert cp_manager.number_of_control_points == 2
    
    # Test that _number_of_control_points can be different from actual number
    cp_manager.number_of_control_points = 5
    assert cp_manager._number_of_control_points == 5
    assert cp_manager.number_of_control_points == 2  # Still returns actual count


def test_cp_manager_beam_relationship():
    """Test CPManager relationship with Beam."""
    beam = Beam(name="BEAM1", beam_number=1)
    cp_manager = CPManager(_number_of_control_points=2, beam=beam)
    
    # Verify beam relationship
    assert cp_manager.beam is beam
    assert cp_manager.beam_id == beam.id
    assert beam.cp_manager is cp_manager
    
    # Test control points are accessible through beam
    cp1 = ControlPoint(gantry=0.0, beam=beam)
    cp2 = ControlPoint(gantry=90.0, cp_manager=cp_manager)
    cp3 = ControlPoint(gantry=180.0, beam=beam, cp_manager=cp_manager)
    
    assert cp1 in beam.control_point_list
    assert cp2 in beam.control_point_list
    assert cp3 in beam.control_point_list


def test_cp_manager_repr():
    """Test the __repr__ method of CPManager."""
    cp_manager = CPManager()
    ControlPoint(gantry=0.0, cp_manager=cp_manager)
    ControlPoint(gantry=180.0, cp_manager=cp_manager)
    
    expected_repr = "<CPManager(id=None, beam='', number_of_control_points=2)>"
    assert repr(cp_manager) == expected_repr
    
    cp_manager.beam = Beam(name="BEAM1")
    expected_repr = "<CPManager(id=None, beam='BEAM1', number_of_control_points=2)>"
    assert repr(cp_manager) == expected_repr
    
