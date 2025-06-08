"""
Unit tests for the MaxDosePoint model.
"""
from pinnacle_io.models import MaxDosePoint, Beam, Dose, Trial


def test_init_with_kwargs():
    """Test initializing a MaxDosePoint with keyword arguments."""
    max_dose_point = MaxDosePoint(
        color="Red",
        display_2d="1",
        dose_value=75.5,
        dose_units="Gy",
        location_x=10.5,
        location_y=20.6,
        location_z=30.7
    )
    
    assert max_dose_point.color == "Red"
    assert max_dose_point.display_2d == "1"
    assert max_dose_point.dose_value == 75.5
    assert max_dose_point.dose_units == "Gy"
    assert max_dose_point.location_x == 10.5
    assert max_dose_point.location_y == 20.6
    assert max_dose_point.location_z == 30.7


def test_init_with_pascal_case():
    """Test initializing a MaxDosePoint with PascalCase parameters."""
    max_dose_point = MaxDosePoint(
        Color="Blue",
        Display2D="0",
        DoseValue=80.2,
        DoseUnits="cGy",
        LocationX=15.1,
        LocationY=25.2,
        LocationZ=35.3
    )
    
    assert max_dose_point.color == "Blue"
    assert max_dose_point.display_2d == "0"
    assert max_dose_point.dose_value == 80.2
    assert max_dose_point.dose_units == "cGy"
    assert max_dose_point.location_x == 15.1
    assert max_dose_point.location_y == 25.2
    assert max_dose_point.location_z == 35.3


def test_relationship_with_trial():
    """Test the relationship between MaxDosePoint and Trial."""
    trial = Trial(trial_name="Test Trial")
    max_dose_point = MaxDosePoint(color="Green", trial=trial)
    
    assert max_dose_point.trial == trial
    assert max_dose_point.trial_id == trial.id
    assert trial.max_dose_point == max_dose_point


def test_relationship_with_beam():
    """Test the relationship between MaxDosePoint and Beam."""
    beam = Beam(name="Test Beam")
    max_dose_point = MaxDosePoint(color="Yellow", beam=beam)
    
    assert max_dose_point.beam == beam
    assert max_dose_point.beam_id == beam.id
    assert beam.max_dose_point == max_dose_point


def test_relationship_with_dose():
    """Test the relationship between MaxDosePoint and Dose."""
    dose = Dose(dose_id="TestDose")
    max_dose_point = MaxDosePoint(color="Purple", dose=dose)
    
    assert max_dose_point.dose == dose
    assert max_dose_point.dose_id == dose.id
    assert dose.max_dose_point == max_dose_point


def test_complete_relationship_chain():
    """Test the complete relationship chain with Trial, Beam, and Dose."""
    trial = Trial(trial_name="Test Trial")
    beam = Beam(name="Test Beam", trial=trial)
    dose = Dose(dose_id="TestDose")
    
    max_dose_point = MaxDosePoint(
        color="Orange",
        trial=trial,
        beam=beam,
        dose=dose
    )
    
    # Verify relationships
    assert max_dose_point.trial == trial
    assert max_dose_point.beam == beam
    assert max_dose_point.dose == dose
    assert trial.max_dose_point == max_dose_point
    assert beam.max_dose_point == max_dose_point
    assert dose.max_dose_point == max_dose_point


def test_repr_method():
    """Test the __repr__ method of MaxDosePoint."""
    # With all fields populated
    max_dose_point = MaxDosePoint(
        id=123,
        color="Red",
        dose_value=75.5,
        dose_units="Gy"
    )
    repr_str = repr(max_dose_point)
    assert "<MaxDosePoint(id=123, color=Red, dose=75.5 Gy)>" == repr_str
    
    # With no color
    max_dose_point = MaxDosePoint(
        id=456,
        dose_value=80.0,
        dose_units="cGy"
    )
    repr_str = repr(max_dose_point)
    assert "<MaxDosePoint(id=456, color=None, dose=80.0 cGy)>" == repr_str
    
    # With no dose value
    max_dose_point = MaxDosePoint(
        id=789,
        color="Blue"
    )
    repr_str = repr(max_dose_point)
    assert "<MaxDosePoint(id=789, color=Blue, dose=None)>" == repr_str


def test_nullable_fields():
    """Test that nullable fields can be set to None."""
    max_dose_point = MaxDosePoint(
        color="White",
        display_2d="1",
        dose_value=None,
        dose_units=None,
        location_x=None,
        location_y=None,
        location_z=None
    )
    
    assert max_dose_point.color == "White"
    assert max_dose_point.display_2d == "1"
    assert max_dose_point.dose_value is None
    assert max_dose_point.dose_units is None
    assert max_dose_point.location_x is None
    assert max_dose_point.location_y is None
    assert max_dose_point.location_z is None
