"""
Tests for the MonitorUnitInfo model.
"""

from pinnacle_io.models import (
    MonitorUnitInfo,
    Beam,
)


def test_monitor_unit_info_initialization():
    """Test MonitorUnitInfo initialization with all fields."""
    monitor_unit_info = MonitorUnitInfo(
        prescription_dose=200.0,
        source_to_prescription_point_distance=100.0,
        total_transmission_fraction=0.95,
        transmission_description="Standard transmission",
        prescription_point_depth=10.0,
        prescription_point_rad_depth=9.8,
        depth_to_actual_point=10.2,
        ssd_to_actual_point=90.0,
        rad_depth_to_actual_point=10.1,
        prescription_point_rad_depth_valid=1,
        prescription_point_off_axis_distance=2.5,
        unblocked_field_area_at_sad=400.0,
        unblocked_field_perimeter_at_sad=80.0,
        blocked_field_area_at_sad=380.0,
        intersect_field_area_at_sad=375.0,
        normalized_dose=100.0,
        off_axis_ratio=0.98,
        collimator_output_factor=1.02,
        relative_output_factor=1.0,
        phantom_output_factor=0.99,
        of_measurement_depth=5.0,
        output_factor_info="Standard output factors"
    )

    # Test all fields are set correctly
    assert monitor_unit_info.prescription_dose == 200.0
    assert monitor_unit_info.source_to_prescription_point_distance == 100.0
    assert monitor_unit_info.total_transmission_fraction == 0.95
    assert monitor_unit_info.transmission_description == "Standard transmission"
    assert monitor_unit_info.prescription_point_depth == 10.0
    assert monitor_unit_info.prescription_point_rad_depth == 9.8
    assert monitor_unit_info.depth_to_actual_point == 10.2
    assert monitor_unit_info.ssd_to_actual_point == 90.0
    assert monitor_unit_info.rad_depth_to_actual_point == 10.1
    assert monitor_unit_info.prescription_point_rad_depth_valid == 1
    assert monitor_unit_info.prescription_point_off_axis_distance == 2.5
    assert monitor_unit_info.unblocked_field_area_at_sad == 400.0
    assert monitor_unit_info.unblocked_field_perimeter_at_sad == 80.0
    assert monitor_unit_info.blocked_field_area_at_sad == 380.0
    assert monitor_unit_info.intersect_field_area_at_sad == 375.0
    assert monitor_unit_info.normalized_dose == 100.0
    assert monitor_unit_info.off_axis_ratio == 0.98
    assert monitor_unit_info.collimator_output_factor == 1.02
    assert monitor_unit_info.relative_output_factor == 1.0
    assert monitor_unit_info.phantom_output_factor == 0.99
    assert monitor_unit_info.of_measurement_depth == 5.0
    assert monitor_unit_info.output_factor_info == "Standard output factors"


def test_monitor_unit_info_beam_relationship():
    """Test MonitorUnitInfo relationship with Beam."""
    beam = Beam(name="BEAM1", beam_number=1)
    monitor_unit_info = MonitorUnitInfo(
        prescription_dose=200.0,
        normalized_dose=100.0,
        beam=beam
    )
    
    # Verify beam relationship
    assert monitor_unit_info.beam is beam
    assert monitor_unit_info.beam_id == beam.id
    assert beam.monitor_unit_info is monitor_unit_info


def test_monitor_unit_info_repr():
    """Test the __repr__ method of MonitorUnitInfo."""
    monitor_unit_info = MonitorUnitInfo(
        prescription_dose=200.0,
        normalized_dose=100.0
    )
    
    expected_repr = "<MonitorUnitInfo(id=None, prescription_dose=200.0, normalized_dose=100.0)>"
    assert repr(monitor_unit_info) == expected_repr
    
    # Test with beam relationship
    monitor_unit_info.beam = Beam(name="BEAM1")
    assert "prescription_dose=200.0" in repr(monitor_unit_info)
    assert "normalized_dose=100.0" in repr(monitor_unit_info)


def test_monitor_unit_info_nullable_fields():
    """Test that all fields in MonitorUnitInfo can be null."""
    monitor_unit_info = MonitorUnitInfo()
    
    # Verify all fields can be null
    assert monitor_unit_info.prescription_dose is None
    assert monitor_unit_info.source_to_prescription_point_distance is None
    assert monitor_unit_info.total_transmission_fraction is None
    assert monitor_unit_info.transmission_description is None
    assert monitor_unit_info.prescription_point_depth is None
    assert monitor_unit_info.prescription_point_rad_depth is None
    assert monitor_unit_info.depth_to_actual_point is None
    assert monitor_unit_info.ssd_to_actual_point is None
    assert monitor_unit_info.rad_depth_to_actual_point is None
    assert monitor_unit_info.prescription_point_rad_depth_valid is None
    assert monitor_unit_info.prescription_point_off_axis_distance is None
    assert monitor_unit_info.unblocked_field_area_at_sad is None
    assert monitor_unit_info.unblocked_field_perimeter_at_sad is None
    assert monitor_unit_info.blocked_field_area_at_sad is None
    assert monitor_unit_info.intersect_field_area_at_sad is None
    assert monitor_unit_info.normalized_dose is None
    assert monitor_unit_info.off_axis_ratio is None
    assert monitor_unit_info.collimator_output_factor is None
    assert monitor_unit_info.relative_output_factor is None
    assert monitor_unit_info.phantom_output_factor is None
    assert monitor_unit_info.of_measurement_depth is None
    assert monitor_unit_info.output_factor_info is None
