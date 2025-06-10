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


def test_monitor_unit_info_sqlalchemy_standards_compliance():
    """Test that MonitorUnitInfo model follows SQLAlchemy standards and best practices."""
    # Test relationship naming (no list relationships in this model)
    monitor_unit_info = MonitorUnitInfo(prescription_dose=200.0)

    # Verify single relationships don't have _list suffix
    assert hasattr(monitor_unit_info, 'beam')

    # Test that relationships are properly typed by checking annotations
    # Check MonitorUnitInfo type annotations
    annotations = MonitorUnitInfo.__annotations__
    assert 'Optional' in str(annotations.get('prescription_dose', ''))
    assert 'Optional' in str(annotations.get('normalized_dose', ''))
    assert 'Optional' in str(annotations.get('transmission_description', ''))
    assert 'Optional' in str(annotations.get('output_factor_info', ''))

    # Test inheritance from correct base class
    from pinnacle_io.models.pinnacle_base import PinnacleBase
    assert issubclass(MonitorUnitInfo, PinnacleBase)


def test_monitor_unit_info_documentation_completeness():
    """Test that MonitorUnitInfo has comprehensive documentation."""
    # Test MonitorUnitInfo class docstring
    docstring = MonitorUnitInfo.__doc__
    assert docstring is not None
    assert len(docstring) > 1500  # Should be detailed like Beam class
    assert "Attributes:" in docstring
    assert "Relationships:" in docstring
    assert "Example:" in docstring
    assert "Dosimetric Calculations:" in docstring

    # Test __init__ method documentation
    init_doc = MonitorUnitInfo.__init__.__doc__
    assert init_doc is not None
    assert "Args:" in init_doc
    assert "Dosimetric Parameters:" in init_doc
    assert "Relationship Parameters:" in init_doc
    assert "Example:" in init_doc


def test_monitor_unit_info_lazy_loading_configuration():
    """Test that MonitorUnitInfo relationships have optimal lazy loading strategies."""
    # Create instance to check relationship configurations
    monitor_unit_info = MonitorUnitInfo(prescription_dose=200.0)

    # Check that relationships exist and are properly configured
    # (The actual lazy loading behavior would be tested in integration tests)
    assert hasattr(monitor_unit_info, 'beam')


def test_monitor_unit_info_dosimetric_calculations():
    """Test MonitorUnitInfo with realistic dosimetric values."""
    # Test with realistic monitor unit calculation values
    monitor_unit_info = MonitorUnitInfo(
        prescription_dose=200.0,  # 2 Gy prescription
        source_to_prescription_point_distance=100.0,  # Standard SAD
        total_transmission_fraction=0.95,  # 5% transmission loss
        prescription_point_depth=10.0,  # 10 cm depth
        normalized_dose=100.0,  # Normalized to 100 cGy
        off_axis_ratio=0.98,  # 2% off-axis reduction
        collimator_output_factor=1.02,  # 2% increase for field size
        relative_output_factor=1.0,  # Reference field size
        phantom_output_factor=0.99,  # 1% phantom scatter reduction
        of_measurement_depth=5.0,  # Output factors measured at 5 cm
        output_factor_info="Measured with ion chamber at dmax"
    )

    # Verify all dosimetric values are set correctly
    assert monitor_unit_info.prescription_dose == 200.0
    assert monitor_unit_info.total_transmission_fraction == 0.95
    assert monitor_unit_info.off_axis_ratio == 0.98
    assert monitor_unit_info.collimator_output_factor == 1.02
    assert monitor_unit_info.relative_output_factor == 1.0
    assert monitor_unit_info.phantom_output_factor == 0.99
    assert "ion chamber" in monitor_unit_info.output_factor_info


def test_monitor_unit_info_field_geometry():
    """Test MonitorUnitInfo with field geometry parameters."""
    monitor_unit_info = MonitorUnitInfo(
        unblocked_field_area_at_sad=100.0,  # 10x10 cm field
        unblocked_field_perimeter_at_sad=40.0,  # Perimeter of 10x10 field
        blocked_field_area_at_sad=95.0,  # 5 cm² blocked
        intersect_field_area_at_sad=90.0,  # Effective treatment area
        prescription_point_off_axis_distance=2.5  # 2.5 cm off-axis
    )

    # Verify field geometry values
    assert monitor_unit_info.unblocked_field_area_at_sad == 100.0
    assert monitor_unit_info.unblocked_field_perimeter_at_sad == 40.0
    assert monitor_unit_info.blocked_field_area_at_sad == 95.0
    assert monitor_unit_info.intersect_field_area_at_sad == 90.0
    assert monitor_unit_info.prescription_point_off_axis_distance == 2.5
