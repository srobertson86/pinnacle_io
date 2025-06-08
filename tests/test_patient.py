"""
Tests for the Patient model, reader, and writer.
"""
from pathlib import Path
from datetime import date
import pytest

from pinnacle_io.models import Patient
from pinnacle_io.readers.patient_reader import PatientReader
from pinnacle_io.writers.patient_writer import PatientWriter


def test_patient_initialization():
    """Test creating a Patient directly with kwargs."""
    # Test with minimal data
    patient = Patient(
        patient_id=123,
        first_name="John",
        middle_name="A",
        last_name="Doe",
        gender="Male",
        medical_record_number="MRN12345",
        diagnosis="Healthy",
        comment="Test patient",
        date_of_birth="1980-01-15 00:00:00"
    )
    
    assert patient.patient_id == 123
    assert patient.first_name == "John"
    assert patient.middle_name == "A"
    assert patient.last_name == "Doe"
    assert patient.gender == "Male"
    assert patient.medical_record_number == "MRN12345"
    assert patient.diagnosis == "Healthy"
    assert patient.comment == "Test patient"
    assert patient.date_of_birth.strftime('%Y-%m-%d %H:%M:%S') == "1980-01-15 00:00:00"


def test_patient_name_methods():
    """Test the patient name formatting methods."""
    patient = Patient(
        first_name="John",
        middle_name="Robert",
        last_name="Doe"
    )
    
    # Test get_full_name
    assert patient.get_full_name() == "John Robert Doe"
    assert patient.name == "John Robert Doe"  # Test the name property
    
    # Test get_dicom_name
    assert patient.get_dicom_name() == "Doe^John^Robert"
    
    # Test with missing components
    patient2 = Patient(
        first_name="Jane",
        last_name="Smith"
    )
    assert patient2.get_full_name() == "Jane Smith"
    assert patient2.get_dicom_name() == "Smith^Jane^"
    
    # Test with only last name
    patient3 = Patient(
        last_name="Johnson"
    )
    assert patient3.get_full_name() == "Johnson"
    assert patient3.get_dicom_name() == "Johnson^^"


def test_patient_age_calculation():
    """Test the patient age calculation method."""
    # Test with date string
    patient1 = Patient(date_of_birth="1980-01-15")
    age1 = patient1.get_age(reference_date=date(2025, 5, 21))
    assert age1 == 45
    
    # Test with date before birthday in reference year
    patient2 = Patient(date_of_birth="1980-06-15")
    age2 = patient2.get_age(reference_date=date(2025, 5, 21))
    assert age2 == 44  # Birthday hasn't occurred yet in 2025
    
    # Test with different date format
    patient3 = Patient(date_of_birth="01/15/1980")
    age3 = patient3.get_age(reference_date=date(2025, 5, 21))
    assert age3 == 45
    
    # Test with no birth date
    patient4 = Patient()
    assert patient4.get_age() is None
    
    # Test with invalid date format
    patient5 = Patient(date_of_birth="invalid-date")
    assert patient5.get_age() is None


def test_read_patient_file():
    """Tests reading a valid Patient file."""
    patient = PatientReader.read(Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1')

    assert isinstance(patient, Patient)
    assert patient.patient_id == 10000
    assert patient.name == "FIRST M LAST"
    assert patient.patient_path == "Institution_1/Mount_0/Patient_1"
    assert patient.last_name == "LAST"
    assert patient.first_name == "FIRST"
    assert patient.middle_name == "M"
    assert patient.medical_record_number == "000000"
    assert patient.radiation_oncologist == "TEST, MD"
    assert patient.date_of_birth.strftime('%Y-%m-%d') == "2020-01-01"

    assert len(patient.plan_list) >= 1
    plan = patient.plan_list[0]
    assert plan.plan_id == 0
    assert plan.name == "BRAIN"
    assert plan.primary_ct_image_set_id == 0

    assert len(patient.image_set_list) >= 1
    image_set = patient.image_set_list[0]
    assert image_set.image_set_id == 0
    assert image_set.modality == "CT"
    assert image_set.image_name == "ImageSet_0"
    assert image_set.series_description == "HEAD"


def test_write_patient_file(tmp_path):
    """Tests writing a Patient file."""
    patient = Patient()
    with pytest.raises(NotImplementedError):
        PatientWriter.write(patient, tmp_path / "Patient_1")


def test_patient_relationships():
    """Test Patient relationships with Institution, Plan, and ImageSet."""
    from pinnacle_io.models import Institution
    
    # Create an institution
    institution = Institution(
        institution_id=1,
        name="Test Hospital",
        institution_path="/test/path"
    )
    
    # Create a patient with relationship to institution
    patient = Patient(
        patient_id=123,
        first_name="John",
        last_name="Doe",
        institution=institution
    )
    
    # Verify institution relationship
    assert patient.institution is institution
    assert patient.institution_id == institution.id
    assert patient in institution.patient_list
    
    # Test adding plans through constructor
    patient_with_plans = Patient(
        patient_id=456,
        first_name="Jane",
        last_name="Smith",
        plan_list=[
            {
                "plan_id": 1,
                "plan_name": "Test Plan 1"
            },
            {
                "plan_id": 2,
                "plan_name": "Test Plan 2"
            }
        ]
    )
    
    # Verify plans relationship
    assert len(patient_with_plans.plan_list) == 2
    assert patient_with_plans.plan_list[0].plan_id == 1
    assert patient_with_plans.plan_list[0].name == "Test Plan 1"
    assert patient_with_plans.plan_list[1].plan_id == 2
    assert patient_with_plans.plan_list[1].name == "Test Plan 2"
    assert all(plan.patient is patient_with_plans for plan in patient_with_plans.plan_list)
    
    # Test adding image sets through constructor
    patient_with_image_sets = Patient(
        patient_id=789,
        first_name="Robert",
        last_name="Johnson",
        image_set_list=[
            {
                "image_set_id": 1,
                "modality": "CT",
                "image_name": "Test Image 1"
            },
            {
                "image_set_id": 2,
                "modality": "MR",
                "image_name": "Test Image 2"
            }
        ]
    )
    
    # Verify image sets relationship
    assert len(patient_with_image_sets.image_set_list) == 2
    assert patient_with_image_sets.image_set_list[0].modality == "CT"
    assert patient_with_image_sets.image_set_list[0].image_name == "Test Image 1"
    assert patient_with_image_sets.image_set_list[1].modality == "MR"
    assert patient_with_image_sets.image_set_list[1].image_name == "Test Image 2"
    assert all(image_set.patient is patient_with_image_sets for image_set in patient_with_image_sets.image_set_list)
    
    # Test adding both plans and image sets
    complete_patient = Patient(
        patient_id=101,
        first_name="Complete",
        last_name="Patient",
        institution=institution,
        plan_list=[
            {"plan_id": 3, "plan_name": "Complete Plan"}
        ],
        image_set_list=[
            {"image_set_id": 3, "modality": "PT", "image_name": "Complete Image"}
        ]
    )
    
    # Verify all relationships
    assert complete_patient.institution is institution
    assert len(complete_patient.plan_list) == 1
    assert complete_patient.plan_list[0].name == "Complete Plan"
    assert len(complete_patient.image_set_list) == 1
    assert complete_patient.image_set_list[0].image_name == "Complete Image"
