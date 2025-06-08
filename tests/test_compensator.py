"""
Tests for the Compensator model.
"""

from pinnacle_io.models import Compensator, Beam


def test_compensator_repr():
    """Test the __repr__ method of the Compensator class."""
    # Create a compensator with known values
    compensator = Compensator(
        id=42,
        name="TestComp",
        tray_number="1",
        is_valid=1,
        width=10.0,
        height=15.0
    )

    # Verify the __repr__ output matches the expected format
    expected_repr = "<Compensator(id=42, name='TestComp')>"
    assert repr(compensator) == expected_repr


def test_compensator_beam_relationship():
    """Test Compensator relationship with Beam."""
    # Create a beam
    beam = Beam(name="BEAM1", beam_number=1)

    # Create a compensator with relationship to beam
    compensator = Compensator(
        name="TestComp",
        beam=beam
    )

    # Verify beam relationship
    assert compensator.beam is beam
    assert beam.compensator is compensator


def test_compensator_initialization():
    """Test creating a Compensator with all fields."""
    compensator = Compensator(
        name="TestComp",
        export_name="COMP1",
        tray_number="1",
        export_format="STL",
        is_valid=1,
        generated_automatically=1,
        proton_source_to_compensator_distance=100.0,
        scale_width_height=1,
        width=10.0,
        height=15.0,
        resolution_x=0.1,
        resolution_y=0.1,
        display_resolution=0.5,
        compensator_hangs_down=1
    )

    # Verify all fields are set correctly
    assert compensator.name == "TestComp"
    assert compensator.export_name == "COMP1"
    assert compensator.tray_number == "1"
    assert compensator.export_format == "STL"
    assert compensator.is_valid == 1
    assert compensator.generated_automatically == 1
    assert compensator.proton_source_to_compensator_distance == 100.0
    assert compensator.scale_width_height == 1
    assert compensator.width == 10.0
    assert compensator.height == 15.0
    assert compensator.resolution_x == 0.1
    assert compensator.resolution_y == 0.1
    assert compensator.display_resolution == 0.5
    assert compensator.compensator_hangs_down == 1
