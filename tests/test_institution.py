"""
Tests for the Institution model, reader, and writer.
"""
from pathlib import Path
import pytest

from pinnacle_io.models import Institution
from pinnacle_io.readers.institution_reader import InstitutionReader
from pinnacle_io.writers.institution_writer import InstitutionWriter



def test_institution_initialization():
    """Test creating an Institution directly with kwargs."""
    # Test with minimal data. Include one input not in the model to ensure it is ignored.
    institution = Institution(
        patient_lite_list=[
            {
                "patient_id": 123,
                "patient_path": "/path/to/patient",
                "mount_point": "Mount_0",
                "formatted_description": "Doe&&John&&Middle&&12345&&Dr. Smith&&01/15/1980",
            }
        ],
        institution_id=456,
        institution_path="/path/to/institution",
        name="Test Institution",
        street_address="123 Main St",
        city="Anytown",
        state="CA",
        zip_code="12345",
        country="USA",
        non_existent_field="This should be ignored",
    )
    
    assert institution.institution_id == 456
    assert institution.institution_path == "/path/to/institution"
    assert institution.name == "Test Institution"
    assert institution.street_address == "123 Main St"
    assert institution.city == "Anytown"
    assert institution.state == "CA"
    assert institution.zip_code == "12345"
    assert institution.country == "USA"
    assert not hasattr(institution, "non_existent_field")
    
    assert len(institution.patient_lite_list) == 1
    patient = institution.patient_lite_list[0]
    assert patient.patient_id == 123
    assert patient.patient_path == "/path/to/patient"
    assert patient.last_name == "Doe"
    assert patient.first_name == "John"
    assert patient.institution.institution_id == institution.institution_id


def test_read_institution_file():
    """Tests reading a valid Institution file."""
    institution = InstitutionReader.read(Path(__file__).parent / 'test_data/01')

    assert isinstance(institution, Institution)
    assert institution.institution_id == 1
    assert institution.name == "16.2 Smart Enterprise"
    assert institution.institution_path == "Institution_1"
    assert institution.default_mount_point == "Mount_0"

    # Check PatientLiteList
    assert len(institution.patient_lite_list) >= 1
    patient_lite = institution.patient_lite_list[0]
    assert patient_lite.patient_id == 1
    assert patient_lite.patient_path == "Institution_1/Mount_0/Patient_1"
    assert patient_lite.mount_point == "Mount_0"
    assert patient_lite.last_name == "LAST"
    assert patient_lite.first_name == "FIRST"
    assert patient_lite.middle_name == "M"
    assert patient_lite.medical_record_number == "000000"
    assert patient_lite.physician == "TEST,MD"
    assert patient_lite.last_modified.strftime('%Y-%m-%d %H:%M:%S') == "2020-01-01 10:00:00"
    assert patient_lite.dir_size == 750.131
    assert patient_lite.institution.institution_id == institution.institution_id

    # Check ObjectVersion
    assert institution.write_version == "Launch Pad: 16.2"
    assert institution.create_version == "Launch Pad: 16.0"
    assert institution.login_name == "candor01"
    assert institution.create_time_stamp.strftime('%Y-%m-%d %H:%M:%S') == "2020-01-01 10:00:00"
    assert institution.write_time_stamp.strftime('%Y-%m-%d %H:%M:%S') == "2020-01-01 10:00:00"
    assert institution.last_modified_time_stamp.strftime('%Y-%m-%d.%H:%M:%S') == "2020-01-01.10:00:00"


def test_write_institution_file():
    """Tests writing an Institution file."""
    institution = Institution()

    with pytest.raises(NotImplementedError):
        InstitutionWriter.write(institution, "/path/to/institution")


def test_institution_repr():
    """Test the string representation of an Institution."""
    # Test with all fields
    institution = Institution(
        institution_id=123,
        name="Test Hospital",
        institution_path="/path/to/institution"
    )
    assert repr(institution) == f"<Institution(id={institution.id}, institution_id=123, name='Test Hospital')>"
    
    # Test with minimal fields
    institution = Institution(
        institution_id=456,
        name=""
    )
    assert repr(institution) == f"<Institution(id={institution.id}, institution_id=456, name='')>"


def test_institution_relationships():
    """Test Institution relationships with PatientLite and Patient models."""
    from pinnacle_io.models import Patient
    
    # Create an institution
    institution = Institution(
        institution_id=1,
        name="Test Hospital",
        institution_path="/test/path"
    )
    
    # Test adding PatientLite models through constructor
    institution_with_patient_lites = Institution(
        institution_id=2,
        name="Hospital with PatientLites",
        institution_path="/test/path2",
        patient_lite_list=[
            {
                "patient_id": 101,
                "patient_path": "/path/to/patient1",
                "mount_point": "Mount_0",
                "formatted_description": "Smith&&John&&A&&MRN101&&Dr. Jones&&2025-01-15"
            },
            {
                "patient_id": 102,
                "patient_path": "/path/to/patient2",
                "mount_point": "Mount_0",
                "last_name": "Johnson",
                "first_name": "Mary",
                "medical_record_number": "MRN102"
            }
        ]
    )
    
    # Verify PatientLite relationships
    assert len(institution_with_patient_lites.patient_lite_list) == 2
    
    # Check first patient (created with formatted_description)
    patient_lite1 = institution_with_patient_lites.patient_lite_list[0]
    assert patient_lite1.patient_id == 101
    assert patient_lite1.patient_path == "/path/to/patient1"
    assert patient_lite1.mount_point == "Mount_0"
    assert patient_lite1.last_name == "Smith"
    assert patient_lite1.first_name == "John"
    assert patient_lite1.middle_name == "A"
    assert patient_lite1.medical_record_number == "MRN101"
    assert patient_lite1.physician == "Dr. Jones"
    assert patient_lite1.institution is institution_with_patient_lites
    
    # Check second patient (created with direct attributes)
    patient_lite2 = institution_with_patient_lites.patient_lite_list[1]
    assert patient_lite2.patient_id == 102
    assert patient_lite2.patient_path == "/path/to/patient2"
    assert patient_lite2.last_name == "Johnson"
    assert patient_lite2.first_name == "Mary"
    assert patient_lite2.medical_record_number == "MRN102"
    assert patient_lite2.institution is institution_with_patient_lites
    
    # Test adding Patient models directly
    # These Patient objects are automatically added to institution.patients
    # when the institution parameter is provided
    Patient(
        patient_id=201,
        first_name="Robert",
        last_name="Brown",
        institution=institution
    )
    
    Patient(
        patient_id=202,
        first_name="Lisa",
        last_name="Davis",
        institution=institution
    )
    
    # Verify Patient relationships
    assert len(list(institution.patient_list)) == 2  # Using list() because patients is lazy-loaded
    patients = list(institution.patient_list)
    assert patients[0].patient_id == 201
    assert patients[0].first_name == "Robert"
    assert patients[0].last_name == "Brown"
    assert patients[0].institution is institution
    
    assert patients[1].patient_id == 202
    assert patients[1].first_name == "Lisa"
    assert patients[1].last_name == "Davis"
    assert patients[1].institution is institution
    
    # Test adding both PatientLite and Patient models
    complete_institution = Institution(
        institution_id=3,
        name="Complete Hospital",
        institution_path="/test/path3",
        patient_lite_list=[
            {"patient_id": 301, "patient_path": "/path/to/patient3", "last_name": "Complete", "first_name": "Patient"}
        ]
    )
    
    # This Patient is automatically added to complete_institution.patients
    Patient(
        patient_id=301,
        first_name="Complete",
        last_name="Patient",
        institution=complete_institution
    )
    
    # Verify all relationships
    assert len(complete_institution.patient_lite_list) == 1
    assert complete_institution.patient_lite_list[0].patient_id == 301
    assert len(list(complete_institution.patient_list)) == 1
    assert list(complete_institution.patient_list)[0].patient_id == 301
