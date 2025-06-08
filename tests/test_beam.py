"""
Tests for the Beam model.
"""

from pinnacle_io.models import (
    Beam,
    Trial,
    ControlPoint,
    Compensator,
    DoseEngine,
    MonitorUnitInfo,
    CPManager,
    Dose,
)


def test_beam_initialization():
    """Test creating a Beam directly with kwargs."""
    # Test with minimal data
    beam = Beam(
        name="Test Beam",
        beam_number=1,
        modality="Photon",
        machine_energy_name="6MV",
        weight=1.0,
    )

    assert beam.name == "Test Beam"
    assert beam.beam_number == 1
    assert beam.modality == "Photon"
    assert beam.machine_energy_name == "6MV"
    assert beam.weight == 1.0
    assert beam.monitor_units_valid is None # Not specified


def test_beam_with_trial_relationship():
    """Test Beam relationship with Trial."""
    # Create a trial
    trial = Trial(trial_id=1, trial_name="Test Trial")

    # Create a beam with relationship to trial
    beam = Beam(name="Test Beam", beam_number=1, trial=trial)

    # Verify trial relationship
    assert beam.trial is trial
    assert beam.trial_id == trial.id
    assert beam in trial.beam_list


def test_beam_with_control_points():
    """Test Beam relationship with ControlPoints."""
    # Create a beam
    beam = Beam(name="Test Beam", beam_number=1)

    # Create control points and add to beam
    cp1 = ControlPoint(
        control_point_number=0, gantry_angle=0.0, collimator_angle=0.0, beam=beam
    )

    cp2 = ControlPoint(
        control_point_number=1, gantry_angle=10.0, collimator_angle=5.0, beam=beam
    )

    # Verify control points relationship
    assert len(beam.control_point_list) == 2
    assert beam.control_point_list[0] is cp1
    assert beam.control_point_list[1] is cp2
    assert all(cp.beam is beam for cp in beam.control_point_list)


def test_beam_with_compensator():
    """Test Beam relationship with Compensator and Compensator attributes."""
    # Create a beam
    beam = Beam(name="Test Beam", beam_number=1)

    # Create compensator with various attributes and add to beam
    compensator = Compensator(
        beam=beam,
        name="Test Compensator",
        export_name="ExportComp",
        tray_number="T1",
        export_format="FormatA",
        is_valid=1,
        generated_automatically=0,
        width=10.5,
        height=5.2,
        density=2.7,
        type="Brass",
        min_allowable_thickness=0.1,
        max_allowable_thickness=5.0,
        dose_min=1.0,
        dose_max=2.0,
        dose_mean=1.5,
        dose_std_dev=0.2,
    )

    # Verify compensator relationship
    assert beam.compensator is compensator
    assert compensator.beam is beam

    # Verify compensator attributes
    assert compensator.name == "Test Compensator"
    assert compensator.export_name == "ExportComp"
    assert compensator.tray_number == "T1"
    assert compensator.export_format == "FormatA"
    assert compensator.is_valid == 1
    assert compensator.generated_automatically == 0
    assert compensator.width == 10.5
    assert compensator.height == 5.2
    assert compensator.density == 2.7
    assert compensator.type == "Brass"
    assert compensator.min_allowable_thickness == 0.1
    assert compensator.max_allowable_thickness == 5.0
    assert compensator.dose_min == 1.0
    assert compensator.dose_max == 2.0
    assert compensator.dose_mean == 1.5
    assert compensator.dose_std_dev == 0.2

    # Test __repr__
    repr_str = repr(compensator)
    assert "Compensator" in repr_str
    assert f"id={compensator.id}" in repr_str
    assert f"name='{compensator.name}'" in repr_str


def test_beam_with_dose_engine():
    """Test Beam relationship with DoseEngine."""
    # Create a beam
    beam = Beam(name="Test Beam", beam_number=1)

    # Create dose engine and add to beam
    dose_engine = DoseEngine(beam=beam)

    # Verify dose engine relationship
    assert beam.dose_engine is dose_engine
    assert dose_engine.beam is beam


def test_beam_with_monitor_unit_info():
    """Test Beam relationship with MonitorUnitInfo."""
    # Create a beam
    beam = Beam(name="Test Beam", beam_number=1)

    # Create monitor unit info and add to beam
    monitor_unit_info = MonitorUnitInfo(beam=beam)

    # Verify monitor unit info relationship
    assert beam.monitor_unit_info is monitor_unit_info
    assert monitor_unit_info.beam is beam


def test_beam_with_cp_manager():
    """Test Beam relationship with CPManager."""
    # Create a beam
    beam = Beam(name="Test Beam", beam_number=1)

    # Create CP manager and add to beam
    cp_manager = CPManager(beam=beam)

    # Verify CP manager relationship
    assert beam.cp_manager is cp_manager
    assert cp_manager.beam is beam


def test_beam_with_dose():
    """Test Beam relationship with Dose."""
    # Create a beam
    beam = Beam(name="Test Beam", beam_number=1)

    # Create dose and add to beam
    dose = Dose(beam=beam)

    # Verify dose relationship
    assert beam.dose is dose
    assert dose.beam is beam


def test_beam_with_all_relationships():
    """Test Beam with all relationships."""
    # Create a trial
    trial = Trial(trial_id=1, trial_name="Test Trial")

    # Create a beam with all relationships
    beam = Beam(name="Test Beam", beam_number=1, trial=trial)

    # Add control points
    ControlPoint(
        control_point_number=0, gantry_angle=0.0, collimator_angle=0.0, beam=beam
    )

    ControlPoint(
        control_point_number=1, gantry_angle=10.0, collimator_angle=5.0, beam=beam
    )

    # Add other relationships
    compensator = Compensator(beam=beam)
    dose_engine = DoseEngine(beam=beam)
    monitor_unit_info = MonitorUnitInfo(beam=beam)
    cp_manager = CPManager(beam=beam)
    dose = Dose(beam=beam)

    # Verify all relationships
    assert beam.trial is trial
    assert len(beam.control_point_list) == 2
    assert beam.compensator is compensator
    assert beam.dose_engine is dose_engine
    assert beam.monitor_unit_info is monitor_unit_info
    assert beam.cp_manager is cp_manager
    assert beam.dose is dose

    # Verify bidirectional relationships
    assert beam in trial.beam_list
    assert all(cp.beam is beam for cp in beam.control_point_list)
    assert compensator.beam is beam
    assert dose_engine.beam is beam
    assert monitor_unit_info.beam is beam
    assert cp_manager.beam is beam
    assert dose.beam is beam


def test_beam_attributes():
    """Test Beam attributes."""
    beam = Beam(
        name="Test Beam",
        beam_number=1,
        isocenter_name="ISO1",
        prescription_name="PRESC1",
        use_poi_for_prescription_point=1,
        prescription_point_name="POI1",
        prescription_point_depth=5.0,
        machine_name_and_version="LINAC_v1",
        modality="Photon",
        machine_energy_name="6MV",
        set_beam_type="Static",
        use_mlc=1,
        ssd=100.0,
        weight=1.0,
        field_id="FIELD1",
        dose_rate=600.0,
    )

    # Verify attributes
    assert beam.name == "Test Beam"
    assert beam.beam_number == 1
    assert beam.isocenter_name == "ISO1"
    assert beam.prescription_name == "PRESC1"
    assert beam.use_poi_for_prescription_point == 1
    assert beam.prescription_point_name == "POI1"
    assert beam.prescription_point_depth == 5.0
    assert beam.machine_name_and_version == "LINAC_v1"
    assert beam.modality == "Photon"
    assert beam.machine_energy_name == "6MV"
    assert beam.set_beam_type == "Static"
    assert beam.use_mlc == 1
    assert beam.ssd == 100.0
    assert beam.weight == 1.0
    assert beam.field_id == "FIELD1"
    assert beam.dose_rate == 600.0


def test_beam_repr():
    """Test the string representation of a Beam."""
    # Create a beam with a known ID, name, and beam_number
    beam = Beam(
        id=42,
        name="Test Beam",
        beam_number=3
    )
    
    # Verify the __repr__ output matches the expected format
    expected_repr = "<Beam(id=42, beam_number=3, name='Test Beam')>"
    assert repr(beam) == expected_repr
