"""
Tests for the PatientRepresentation model.
"""

from pinnacle_io.models import (
    PatientRepresentation,
    Trial,
)


def test_patient_representation_initialization():
    """Test PatientRepresentation initialization with all fields."""
    patient_representation = PatientRepresentation(
        patient_volume_name="BODY",
        ct_to_density_name="Standard CT",
        ct_to_density_version="1.0",
        dm_table_name="DM_TABLE",
        dm_table_version="2.0",
        top_z_padding=10,
        bottom_z_padding=15,
        high_res_z_spacing_for_variable=0.25,
        outside_patient_is_ct_number=1,
        outside_patient_air_threshold=-1000.0,
        ct_to_density_table_accepted=1,
        ct_to_density_table_extended=0,
        ct_to_stopping_power_table_name="Stopping Power Table",
        ct_to_stopping_power_version="1.0",
        ct_to_stopping_power_extended=0,
        ct_to_stopping_power_accepted=1
    )

    # Test all fields are set correctly
    assert patient_representation.patient_volume_name == "BODY"
    assert patient_representation.ct_to_density_name == "Standard CT"
    assert patient_representation.ct_to_density_version == "1.0"
    assert patient_representation.dm_table_name == "DM_TABLE"
    assert patient_representation.dm_table_version == "2.0"
    assert patient_representation.top_z_padding == 10
    assert patient_representation.bottom_z_padding == 15
    assert patient_representation.high_res_z_spacing_for_variable == 0.25
    assert patient_representation.outside_patient_is_ct_number == 1
    assert patient_representation.outside_patient_air_threshold == -1000.0
    assert patient_representation.ct_to_density_table_accepted == 1
    assert patient_representation.ct_to_density_table_extended == 0
    assert patient_representation.ct_to_stopping_power_table_name == "Stopping Power Table"
    assert patient_representation.ct_to_stopping_power_version == "1.0"
    assert patient_representation.ct_to_stopping_power_extended == 0
    assert patient_representation.ct_to_stopping_power_accepted == 1


def test_patient_representation_trial_relationship():
    """Test PatientRepresentation relationship with Trial."""
    trial = Trial(name="Trial1")
    patient_representation = PatientRepresentation(
        patient_volume_name="BODY",
        top_z_padding=10,
        bottom_z_padding=15,
        trial=trial
    )
    
    # Verify trial relationship
    assert patient_representation.trial is trial
    assert patient_representation.trial_id == trial.id
    assert trial.patient_representation is patient_representation


def test_patient_representation_repr():
    """Test the __repr__ method of PatientRepresentation."""
    patient_representation = PatientRepresentation(
        top_z_padding=10,
        bottom_z_padding=15
    )
    
    expected_repr = "<PatientRepresentation(id=None, top_z_padding=10, bottom_z_padding=15)>"
    assert repr(patient_representation) == expected_repr
    
    # Test with trial relationship
    patient_representation.trial = Trial(name="Trial1")
    assert "top_z_padding=10" in repr(patient_representation)
    assert "bottom_z_padding=15" in repr(patient_representation)


def test_patient_representation_nullable_fields():
    """Test that all fields in PatientRepresentation can be null."""
    patient_representation = PatientRepresentation()
    
    # Verify all fields can be null
    assert patient_representation.patient_volume_name is None
    assert patient_representation.ct_to_density_name is None
    assert patient_representation.ct_to_density_version is None
    assert patient_representation.dm_table_name is None
    assert patient_representation.dm_table_version is None
    assert patient_representation.top_z_padding is None
    assert patient_representation.bottom_z_padding is None
    assert patient_representation.high_res_z_spacing_for_variable is None
    assert patient_representation.outside_patient_is_ct_number is None
    assert patient_representation.outside_patient_air_threshold is None
    assert patient_representation.ct_to_density_table_accepted is None
    assert patient_representation.ct_to_density_table_extended is None
    assert patient_representation.ct_to_stopping_power_table_name is None
    assert patient_representation.ct_to_stopping_power_version is None
    assert patient_representation.ct_to_stopping_power_extended is None
    assert patient_representation.ct_to_stopping_power_accepted is None


def test_patient_representation_field_types():
    """Test that fields are stored with correct types."""
    patient_representation = PatientRepresentation(
        patient_volume_name="BODY",            # String
        top_z_padding=10,                      # Integer
        high_res_z_spacing_for_variable=0.25,  # Float
        outside_patient_is_ct_number=1         # Integer (boolean-like)
    )
    
    # Verify field types
    assert isinstance(patient_representation.patient_volume_name, str)
    assert isinstance(patient_representation.top_z_padding, int)
    assert isinstance(patient_representation.high_res_z_spacing_for_variable, float)
    assert isinstance(patient_representation.outside_patient_is_ct_number, int)
