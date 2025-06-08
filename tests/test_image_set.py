"""
Tests for the ImageSet model, reader, and writer.
"""
from pathlib import Path
import pytest

from pinnacle_io.models import ImageSet, ImageInfo, Patient
from pinnacle_io.readers.image_set_reader import ImageSetReader
from pinnacle_io.writers.image_set_writer import ImageSetWriter


def test_image_info_initialization():
    """Test creating an ImageInfo directly with kwargs."""
    # Test with minimal data
    image_info = ImageInfo(
        table_position=10.5,
        couch_pos=15.2,
        slice_number=5,
        series_uid="1.2.3.4.5",
        study_instance_uid="1.2.3.4.6",
        frame_uid="1.2.3.4.7",
        class_uid="1.2.3.4.8",
        instance_uid="1.2.3.4.9",
        dicom_file_name="slice_5.dcm"
    )
    
    assert image_info.table_position == 10.5
    assert image_info.couch_pos == 15.2
    assert image_info.slice_number == 5
    assert image_info.series_uid == "1.2.3.4.5"
    assert image_info.study_instance_uid == "1.2.3.4.6"
    assert image_info.frame_uid == "1.2.3.4.7"
    assert image_info.class_uid == "1.2.3.4.8"
    assert image_info.instance_uid == "1.2.3.4.9"
    assert image_info.dicom_file_name == "slice_5.dcm"


def test_image_set_initialization():
    """Test creating an ImageSet directly with kwargs."""
    # Test with minimal data
    image_set = ImageSet(
        series_uid="1.2.3.4.5",
        study_uid="1.2.3.4.6",
        series_number=1,
        acquisition_number=2,
        image_name="Test Image",
        modality="CT",
        x_dim=512,
        y_dim=512,
        z_dim=101,
        x_pixdim=0.097656,
        y_pixdim=0.097656,
        z_pixdim=0.25,
        image_info_list=[
            {
                "table_position": 10.5,
                "couch_pos": 15.2,
                "slice_number": 0,
                "series_uid": "1.2.3.4.5",
                "study_instance_uid": "1.2.3.4.6",
                "frame_uid": "1.2.3.4.7",
                "class_uid": "1.2.3.4.8",
                "instance_uid": "1.2.3.4.9",
                "dicom_file_name": "slice_0.dcm"
            },
            {
                "table_position": 10.75,
                "couch_pos": 15.45,
                "slice_number": 1,
                "series_uid": "1.2.3.4.5",
                "study_instance_uid": "1.2.3.4.6",
                "frame_uid": "1.2.3.4.7",
                "class_uid": "1.2.3.4.8",
                "instance_uid": "1.2.3.4.10",
                "dicom_file_name": "slice_1.dcm"
            }
        ]
    )
    
    assert image_set.series_uid == "1.2.3.4.5"
    assert image_set.study_uid == "1.2.3.4.6"
    assert image_set.series_number == 1
    assert image_set.acquisition_number == 2
    assert image_set.image_name == "Test Image"
    assert image_set.modality == "CT"
    assert image_set.x_dim == 512
    assert image_set.y_dim == 512
    assert image_set.z_dim == 101
    assert image_set.x_pixdim == 0.097656
    assert image_set.y_pixdim == 0.097656
    assert image_set.z_pixdim == 0.25
    assert len(image_set.image_info_list) == 2
    
    # Check first image info
    image_info_1 = image_set.image_info_list[0]
    assert image_info_1.table_position == 10.5
    assert image_info_1.slice_number == 0
    assert image_info_1.dicom_file_name == "slice_0.dcm"
    
    # Check second image info
    image_info_2 = image_set.image_info_list[1]
    assert image_info_2.table_position == 10.75
    assert image_info_2.slice_number == 1
    assert image_info_2.dicom_file_name == "slice_1.dcm"


def test_image_set_properties():
    """Test the ImageSet properties."""
    # Create an image set with image info
    image_set = ImageSet(
        series_uid="1.2.3.4.5",
        study_uid="1.2.3.4.6",
        image_name="Test Image",
        modality="CT",
        x_dim=512,
        y_dim=512,
        z_dim=101,
        x_pixdim=0.097656,
        y_pixdim=0.097656,
        z_pixdim=0.25,
        image_info_list=[
            {
                "table_position": 10.5,
                "couch_pos": 15.2,
                "slice_number": 0,
                "series_uid": "1.2.3.4.5",
                "study_instance_uid": "1.2.3.4.6",
                "frame_uid": "1.2.3.4.7",
                "class_uid": "1.2.3.4.8",
                "instance_uid": "1.2.3.4.9",
                "dicom_file_name": "slice_0.dcm"
            },
            {
                "table_position": 10.75,
                "couch_pos": 15.45,
                "slice_number": 1,
                "series_uid": "1.2.3.4.5",
                "study_instance_uid": "1.2.3.4.6",
                "frame_uid": "1.2.3.4.7",
                "class_uid": "1.2.3.4.8",
                "instance_uid": "1.2.3.4.10",
                "dicom_file_name": "slice_1.dcm"
            }
        ]
    )
    
    # Test the properties
    assert image_set.table_positions == [10.5, 10.75]
    assert image_set.couch_positions == [15.2, 15.45]
    assert image_set.slice_numbers == [0, 1]
    assert image_set.study_instance_uid == "1.2.3.4.6"
    assert image_set.frame_of_reference_uid == "1.2.3.4.7"
    assert image_set.class_uid == "1.2.3.4.8"
    assert image_set.instance_uids == ["1.2.3.4.9", "1.2.3.4.10"]
    assert image_set.dicom_file_names == ["slice_0.dcm", "slice_1.dcm"]
    
    # Test the methods
    assert image_set.get_image_dimensions() == (512, 512, 101)
    assert image_set.get_pixel_spacing() == (0.097656, 0.097656, 0.25)


def test_image_set_patient_relationship():
    """Test the relationship between Patient and ImageSet."""
    # Create a patient
    patient = Patient(
        patient_id=123,
        first_name="John",
        last_name="Doe"
    )
    
    # Create an image set
    image_set = ImageSet(
        series_uid="1.2.3.4.5",
        study_uid="1.2.3.4.6",
        image_name="Test Image",
        modality="CT"
    )
    
    # Associate the image set with the patient
    patient.image_set_list.append(image_set)
    
    # Check the relationship
    assert len(patient.image_set_list) == 1
    assert patient.image_set_list[0].series_uid == "1.2.3.4.5"
    assert patient.image_set_list[0].image_name == "Test Image"
    assert image_set.patient == patient
    assert image_set.patient_id == patient.id


def test_read_image_set_file():
    """Tests reading a valid ImageSet file."""
    image_set = ImageSetReader.read_header(Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/ImageSet_0')

    assert isinstance(image_set, ImageSet)
    assert image_set.series_uid == "1.2.840.113619.2.55.3.3535481354.000.3513513585.000"
    assert image_set.study_uid is None
    assert image_set.series_description == "HEAD"
    assert image_set.modality == "CT"
    assert image_set.x_dim == 512
    assert image_set.y_dim == 512
    assert image_set.z_dim == 101
    assert image_set.x_pixdim == 0.097656
    assert image_set.y_pixdim == 0.097656
    assert image_set.z_pixdim == 0.25

    assert len(image_set.image_info_list) > 2
    assert image_set.image_info_list[0].table_position == -8.75
    assert image_set.image_info_list[0].slice_number == 1
    assert image_set.image_info_list[0].dicom_file_name == "CT_1.2.840.113619.2.55.3.3535481354.111.3513513585.3.1.dcm"
    assert image_set.image_info_list[1].table_position == -8.5
    assert image_set.image_info_list[1].slice_number == 2
    assert image_set.image_info_list[1].dicom_file_name == "CT_1.2.840.113619.2.55.3.3535481354.111.3513513585.3.2.dcm"


def test_write_image_set_file(tmp_path):
    """Tests writing an ImageSet file."""
    image_set = ImageSet()
    with pytest.raises(NotImplementedError):
        ImageSetWriter.write(image_set, "/path/to/image_set")


def test_image_set_relationships_initialization():
    """Test that all ImageSet relationships are initialized correctly."""
    # Test initializing with a patient directly
    patient = Patient(
        patient_id=123,
        first_name="John",
        last_name="Doe"
    )
    
    image_set = ImageSet(
        series_uid="1.2.3.4.5",
        image_name="Test Image",
        modality="CT",
        patient=patient
    )
    
    # Verify patient relationship
    assert image_set.patient is patient
    assert image_set.patient_id == patient.id
    assert image_set in patient.image_set_list
    
    # Test initializing with a patient as a dictionary
    image_set2 = ImageSet(
        series_uid="1.2.3.4.6",
        image_name="Test Image 2",
        modality="MR",
        patient={
            "patient_id": 456,
            "first_name": "Jane",
            "last_name": "Smith"
        }
    )
    
    # Verify patient relationship
    assert image_set2.patient is not None
    assert image_set2.patient.patient_id == 456
    assert image_set2.patient.first_name == "Jane"
    assert image_set2.patient.last_name == "Smith"
    assert image_set2 in image_set2.patient.image_set_list
    
    # Test initializing with image_info_list
    image_set3 = ImageSet(
        series_uid="1.2.3.4.7",
        image_name="Test Image 3",
        modality="PT",
        image_info_list=[
            {
                "table_position": 10.5,
                "slice_number": 0,
                "instance_uid": "1.2.3.4.9"
            },
            {
                "table_position": 10.75,
                "slice_number": 1,
                "instance_uid": "1.2.3.4.10"
            }
        ]
    )
    
    # Verify image_info_list relationship
    assert len(image_set3.image_info_list) == 2
    assert image_set3.image_info_list[0].table_position == 10.5
    assert image_set3.image_info_list[0].slice_number == 0
    assert image_set3.image_info_list[0].instance_uid == "1.2.3.4.9"
    assert image_set3.image_info_list[0].image_set is image_set3
    
    assert image_set3.image_info_list[1].table_position == 10.75
    assert image_set3.image_info_list[1].slice_number == 1
    assert image_set3.image_info_list[1].instance_uid == "1.2.3.4.10"
    assert image_set3.image_info_list[1].image_set is image_set3
    
    # Test initializing with ImageInfoList (PascalCase)
    image_set4 = ImageSet(
        series_uid="1.2.3.4.8",
        image_name="Test Image 4",
        modality="CT",
        ImageInfoList=[
            {
                "table_position": 11.5,
                "slice_number": 0,
                "instance_uid": "1.2.3.4.11"
            },
            {
                "table_position": 11.75,
                "slice_number": 1,
                "instance_uid": "1.2.3.4.12"
            }
        ]
    )
    
    # Verify ImageInfoList relationship
    assert len(image_set4.image_info_list) == 2
    assert image_set4.image_info_list[0].table_position == 11.5
    assert image_set4.image_info_list[0].instance_uid == "1.2.3.4.11"
    assert image_set4.image_info_list[0].image_set is image_set4
    
    # Test initializing with both patient and image_info_list
    image_set5 = ImageSet(
        series_uid="1.2.3.4.9",
        image_name="Test Image 5",
        modality="CT",
        patient=patient,
        image_info_list=[
            {
                "table_position": 12.5,
                "slice_number": 0,
                "instance_uid": "1.2.3.4.13"
            }
        ]
    )
    
    # Verify all relationships
    assert image_set5.patient is patient
    assert image_set5 in patient.image_set_list
    assert len(image_set5.image_info_list) == 1
    assert image_set5.image_info_list[0].table_position == 12.5
    assert image_set5.image_info_list[0].image_set is image_set5


def test_image_set_repr():
    """Test the __repr__ method of the ImageSet class."""
    # Create an image set with known values
    image_set = ImageSet(
        ID=42,  # Setting ID directly for testing repr
        image_name="Test Image",
        modality="CT"
    )
    
    # Check the string representation
    expected_repr = "<ImageSet(id=42, name='Test Image', modality='CT')>"
    assert repr(image_set) == expected_repr
    
    # Test with different values
    image_set2 = ImageSet(
        ID=123,
        image_name="MRI Scan",
        modality="MR"
    )
    
    expected_repr2 = "<ImageSet(id=123, name='MRI Scan', modality='MR')>"
    assert repr(image_set2) == expected_repr2
