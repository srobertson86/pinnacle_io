"""
Tests for the PatientLite model.

This module tests the PatientLite model initialization and relationships.
Reading and writing are covered by the test_institution.py module.
"""
from datetime import datetime

from pinnacle_io.models import PatientLite, Institution


def test_patient_lite_initialization():
    """Test creating a PatientLite directly with kwargs."""
    # Test with direct field assignments
    patient = PatientLite(
        patient_id=123,
        patient_path="Institution_1/Mount_0/Patient_123",
        mount_point="Mount_0",
        dir_size=456.789,
        last_name="Smith",
        first_name="John",
        middle_name="Robert",
        medical_record_number="MRN12345",
        physician="Dr. Johnson",
        last_modified=datetime(2025, 5, 29, 14, 30, 0)
    )
    
    assert patient.patient_id == 123
    assert patient.patient_path == "Institution_1/Mount_0/Patient_123"
    assert patient.mount_point == "Mount_0"
    assert patient.dir_size == 456.789
    assert patient.last_name == "Smith"
    assert patient.first_name == "John"
    assert patient.middle_name == "Robert"
    assert patient.medical_record_number == "MRN12345"
    assert patient.physician == "Dr. Johnson"
    assert patient.last_modified == datetime(2025, 5, 29, 14, 30, 0)


def test_patient_lite_initialization_with_formatted_description():
    """Test creating a PatientLite with a formatted description string."""
    # Test with formatted_description (snake_case)
    patient1 = PatientLite(
        patient_id=123,
        patient_path="Institution_1/Mount_0/Patient_123",
        mount_point="Mount_0",
        formatted_description="Doe&&Jane&&A&&MRN54321&&Dr. Smith&&2025-01-15"
    )
    
    assert patient1.last_name == "Doe"
    assert patient1.first_name == "Jane"
    assert patient1.middle_name == "A"
    assert patient1.medical_record_number == "MRN54321"
    assert patient1.physician == "Dr. Smith"
    assert patient1.last_modified.year == 2025
    assert patient1.last_modified.month == 1
    assert patient1.last_modified.day == 15
    
    # Test with FormattedDescription (PascalCase)
    patient2 = PatientLite(
        patient_id=456,
        patient_path="Institution_1/Mount_0/Patient_456",
        mount_point="Mount_0",
        FormattedDescription="Johnson&&Robert&&B&&MRN98765&&Dr. Brown&&2024-12-31"
    )
    
    assert patient2.last_name == "Johnson"
    assert patient2.first_name == "Robert"
    assert patient2.middle_name == "B"
    assert patient2.medical_record_number == "MRN98765"
    assert patient2.physician == "Dr. Brown"
    assert patient2.last_modified.year == 2024
    assert patient2.last_modified.month == 12
    assert patient2.last_modified.day == 31


def test_patient_lite_partial_formatted_description():
    """Test creating a PatientLite with incomplete formatted description."""
    # Test with partial formatted_description
    patient = PatientLite(
        patient_id=123,
        patient_path="Institution_1/Mount_0/Patient_123",
        mount_point="Mount_0",
        formatted_description="Doe&&Jane"  # Only last_name and first_name
    )
    
    assert patient.last_name == "Doe"
    assert patient.first_name == "Jane"
    
    # Empty string for missing parts
    assert patient.middle_name == ""
    assert patient.medical_record_number == ""
    assert patient.physician == ""
    
    # None for missing datetime
    assert patient.last_modified is None 


def test_patient_lite_repr():
    """Test the string representation of PatientLite."""
    patient = PatientLite(
        id=1,
        patient_id=123,
        last_name="Smith",
        first_name="John"
    )
    
    expected_repr = "<PatientLite(id=1, patient_id=123, name='Smith, John')>"
    assert repr(patient) == expected_repr


def test_patient_lite_institution_relationship():
    """Test the relationship between PatientLite and Institution."""
    # Create an institution
    institution = Institution(
        institution_id=1,
        name="Test Hospital",
        institution_path="Institution_1"
    )
    
    # Create a patient with relationship to institution
    patient = PatientLite(
        patient_id=123,
        patient_path="Institution_1/Mount_0/Patient_123",
        mount_point="Mount_0",
        last_name="Smith",
        first_name="John",
        institution=institution
    )
    
    # Verify institution relationship
    assert patient.institution is institution
    assert patient.institution_id == institution.id
    assert patient in institution.patient_lite_list


def test_patient_lite_institution_relationship_through_constructor():
    """Test adding PatientLite to Institution through constructor."""
    # Create an institution with patient_lite_list
    institution = Institution(
        institution_id=1,
        name="Test Hospital",
        institution_path="Institution_1",
        patient_lite_list=[
            {
                "patient_id": 123,
                "patient_path": "Institution_1/Mount_0/Patient_123",
                "mount_point": "Mount_0",
                "last_name": "Smith",
                "first_name": "John"
            },
            {
                "patient_id": 456,
                "patient_path": "Institution_1/Mount_0/Patient_456",
                "mount_point": "Mount_0",
                "formatted_description": "Doe&&Jane&&A&&MRN54321&&Dr. Smith&&2025-01-15"
            }
        ]
    )
    
    # Verify patient_lite_list relationship
    assert len(institution.patient_lite_list) == 2
    
    # Check first patient
    patient1 = institution.patient_lite_list[0]
    assert patient1.patient_id == 123
    assert patient1.patient_path == "Institution_1/Mount_0/Patient_123"
    assert patient1.mount_point == "Mount_0"
    assert patient1.last_name == "Smith"
    assert patient1.first_name == "John"
    assert patient1.institution is institution
    
    # Check second patient
    patient2 = institution.patient_lite_list[1]
    assert patient2.patient_id == 456
    assert patient2.patient_path == "Institution_1/Mount_0/Patient_456"
    assert patient2.mount_point == "Mount_0"
    assert patient2.last_name == "Doe"
    assert patient2.first_name == "Jane"
    assert patient2.middle_name == "A"
    assert patient2.medical_record_number == "MRN54321"
    assert patient2.physician == "Dr. Smith"
    assert patient2.institution is institution


def test_patient_lite_case_insensitive_initialization():
    """Test case-insensitive initialization of PatientLite."""
    # Test with mixed case field names
    patient = PatientLite(
        PatientID=123,
        patientPath="Institution_1/Mount_0/Patient_123",
        MOUNT_POINT="Mount_0",
        Last_Name="Smith",
        firstName="John"
    )
    
    assert patient.patient_id == 123
    assert patient.patient_path == "Institution_1/Mount_0/Patient_123"
    assert patient.mount_point == "Mount_0"
    assert patient.last_name == "Smith"
    assert patient.first_name == "John"


def test_patient_lite_with_non_existent_fields():
    """Test that non-existent fields are ignored during initialization."""
    # Include fields that don't exist in the model
    patient = PatientLite(
        patient_id=123,
        patient_path="Institution_1/Mount_0/Patient_123",
        non_existent_field="This should be ignored",
        another_fake_field=42
    )
    
    assert patient.patient_id == 123
    assert patient.patient_path == "Institution_1/Mount_0/Patient_123"
    assert not hasattr(patient, "non_existent_field")
    assert not hasattr(patient, "another_fake_field")
