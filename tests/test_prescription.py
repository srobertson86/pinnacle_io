"""Unit tests for Prescription model class."""

import pytest
from pinnacle_io.models.prescription import Prescription
from pinnacle_io.models.trial import Trial


@pytest.fixture
def sample_prescription_data():
    """Fixture providing sample prescription data."""
    return {
        "id": 1,
        "name": "Test Prescription",
        "requested_monitor_units_per_fraction": 100,
        "prescription_dose": 50.0,
        "prescription_percent": 95,
        "number_of_fractions": 25,
        "prescription_point": "ISOCENTER",
        "method": "Standard",
        "normalization_method": "MaxDose",
        "prescription_period": "Treatment",
        "weights_proportional_to": "MUs",
        "dose_uncertainty": 1,
        "prescription_uncertainty": 2,
        "dose_uncertainty_valid": 1,
        "prescrip_uncertainty_valid": 1,
        "color": "Red",
        "trial_id": 1
    }


@pytest.fixture
def sample_prescription(sample_prescription_data):
    """Fixture providing a sample Prescription instance."""
    return Prescription(**sample_prescription_data)


def test_prescription_initialization(sample_prescription_data, sample_prescription):
    """Test Prescription initialization with all attributes."""
    for key, value in sample_prescription_data.items():
        if key != "trial_id":  # trial_id is handled by SQLAlchemy relationship
            assert getattr(sample_prescription, key) == value


def test_prescription_minimal_initialization():
    """Test Prescription initialization with minimal attributes."""
    prescription = Prescription(id=1, name="Minimal Prescription")
    assert prescription.id == 1
    assert prescription.name == "Minimal Prescription"
    assert prescription.prescription_dose is None
    assert prescription.number_of_fractions is None
    assert prescription.trial_id is None


def test_prescription_nullable_fields():
    """Test that all fields are nullable."""
    prescription = Prescription()
    assert prescription.name is None
    assert prescription.requested_monitor_units_per_fraction is None
    assert prescription.prescription_dose is None
    assert prescription.prescription_percent is None
    assert prescription.number_of_fractions is None
    assert prescription.prescription_point is None
    assert prescription.method is None
    assert prescription.normalization_method is None
    assert prescription.prescription_period is None
    assert prescription.weights_proportional_to is None
    assert prescription.dose_uncertainty is None
    assert prescription.prescription_uncertainty is None
    assert prescription.dose_uncertainty_valid is None
    assert prescription.prescrip_uncertainty_valid is None
    assert prescription.color is None


def test_prescription_repr(sample_prescription):
    """Test the string representation of Prescription."""
    expected = "<Prescription(id=1, name='Test Prescription', prescription_dose=50.0, number_of_fractions=25)>"
    assert repr(sample_prescription) == expected


def test_prescription_trial_relationship():
    """Test the relationship between Prescription and Trial."""
    # Create a trial and a prescription
    trial = Trial(id=1, name="Test Trial")
    prescription = Prescription(id=1, name="Test Prescription", trial_id=1)
    
    # Set up the relationship
    prescription.trial = trial
    
    # Test the relationship
    assert prescription.trial == trial
    assert prescription in trial.prescription_list
    assert prescription.trial_id == trial.id


def test_prescription_trial_backref():
    """Test the back reference from Trial to Prescription."""
    # Create a trial and multiple prescriptions
    trial = Trial(id=1, name="Test Trial")
    prescription1 = Prescription(id=1, name="Prescription 1", trial_id=1)
    prescription2 = Prescription(id=2, name="Prescription 2", trial_id=1)
    
    # Set up the relationships
    trial.prescription_list.extend([prescription1, prescription2])
    
    # Test the back references
    assert len(trial.prescription_list) == 2
    assert prescription1.trial == trial
    assert prescription2.trial == trial
    assert trial.prescription_list == [prescription1, prescription2]