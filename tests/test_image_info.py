"""
Tests for the ImageInfo model, reader, and writer.
"""
from pathlib import Path
import pytest

from pinnacle_io.models import ImageInfo, ImageSet
from pinnacle_io.readers.image_set_reader import ImageSetReader


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


def test_image_info_relationships():
    """Test the relationships between ImageInfo and ImageSet."""
    # Create an image set
    image_set = ImageSet(
        series_uid="1.2.3.4.5",
        study_uid="1.2.3.4.6",
        image_name="Test Image",
        modality="CT"
    )
    
    # Create an image info and associate it with the image set
    image_info = ImageInfo(
        table_position=10.5,
        slice_number=5,
        instance_uid="1.2.3.4.9",
        dicom_file_name="slice_5.dcm",
        image_set=image_set
    )
    
    # Check the relationship
    assert image_info in image_set.image_info_list
    assert image_info.image_set == image_set
    assert image_info.image_set_id == image_set.id


def test_image_info_relationships_initialization():
    """Test that all ImageInfo relationships are initialized correctly."""
    # Test initializing with an image_set directly
    image_set = ImageSet(
        series_uid="1.2.3.4.5",
        image_name="Test Image",
        modality="CT"
    )
    
    image_info = ImageInfo(
        table_position=10.5,
        slice_number=0,
        instance_uid="1.2.3.4.9",
        image_set=image_set
    )
    
    # Verify image_set relationship
    assert image_info.image_set is image_set
    assert image_info.image_set_id == image_set.id
    assert image_info in image_set.image_info_list
    
    # Test initializing with an image_set as a dictionary
    image_info2 = ImageInfo(
        table_position=11.5,
        slice_number=1,
        instance_uid="1.2.3.4.10",
        image_set={
            "series_uid": "1.2.3.4.6",
            "image_name": "Test Image 2",
            "modality": "MR"
        }
    )
    
    # Verify image_set relationship
    assert image_info2.image_set is not None
    assert image_info2.image_set.series_uid == "1.2.3.4.6"
    assert image_info2.image_set.image_name == "Test Image 2"
    assert image_info2.image_set.modality == "MR"
    assert image_info2 in image_info2.image_set.image_info_list
    
    # Test initializing with ImageSet (PascalCase)
    image_info3 = ImageInfo(
        table_position=12.5,
        slice_number=2,
        instance_uid="1.2.3.4.11",
        ImageSet=image_set
    )
    
    # Verify ImageSet relationship
    assert image_info3.image_set is image_set
    assert image_info3.image_set_id == image_set.id
    assert image_info3 in image_set.image_info_list


def test_image_info_dictionary_initialization():
    """Test initializing ImageInfo with a dictionary for image_set."""
    # Test with image_set as a dictionary
    image_info = ImageInfo(
        table_position=10.5,
        slice_number=5,
        instance_uid="1.2.3.4.9",
        dicom_file_name="slice_5.dcm",
        image_set={
            "series_uid": "1.2.3.4.5",
            "study_uid": "1.2.3.4.6",
            "image_name": "Test Image",
            "modality": "CT"
        }
    )
    
    assert image_info.image_set is not None
    assert image_info.image_set.series_uid == "1.2.3.4.5"
    assert image_info.image_set.study_uid == "1.2.3.4.6"
    assert image_info.image_set.image_name == "Test Image"
    assert image_info.image_set.modality == "CT"
    assert image_info in image_info.image_set.image_info_list


def test_read_image_info_from_file():
    """Tests reading ImageInfo as part of an ImageSet file."""
    image_set = ImageSetReader.read_header(Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/ImageSet_0')
    
    # Check that we have image info objects
    assert len(image_set.image_info_list) > 0
    image_info = image_set.image_info_list[0]
    
    # Verify first image info properties
    assert isinstance(image_info, ImageInfo)
    assert image_info.table_position == -8.75
    assert image_info.slice_number == 1
    assert image_info.dicom_file_name == "CT_1.2.840.113619.2.55.3.3535481354.111.3513513585.3.1.dcm"
    assert image_info.image_set == image_set


def test_write_image_info():
    """Test writing ImageInfo (should raise NotImplementedError as it's part of ImageSet)."""
    image_info = ImageInfo(
        table_position=10.5,
        slice_number=5,
        instance_uid="1.2.3.4.9",
        dicom_file_name="slice_5.dcm"
    )
    
    with pytest.raises(AttributeError):
        image_info.write("/path/to/image_info")


def test_image_info_repr():
    """Test the __repr__ method of the ImageInfo class."""
    # Create an image info with known values
    image_info = ImageInfo(
        ID=42,  # Setting ID directly for testing repr
        table_position=10.5,
        slice_number=5,
        instance_uid="1.2.3.4.9",
        dicom_file_name="slice_5.dcm"
    )

    expected_repr = "<ImageInfo(id=42, slice_number=5, table_position=10.5)>"
    assert repr(image_info) == expected_repr
    
    # Test with different values
    image_info2 = ImageInfo(
        ID=123,
        table_position=-15.75,
        slice_number=10,
        instance_uid="1.2.3.4.10",
        dicom_file_name="slice_10.dcm"
    )
    
    expected_repr2 = "<ImageInfo(id=123, slice_number=10, table_position=-15.75)>"
    assert repr(image_info2) == expected_repr2


def test_image_info_optional_fields():
    """Test that ImageInfo handles optional fields correctly."""
    # Create with minimal required fields
    image_info = ImageInfo(
        table_position=10.5,
        slice_number=5
    )
    
    assert image_info.table_position == 10.5
    assert image_info.slice_number == 5
    assert image_info.couch_pos is None
    assert image_info.series_uid is None
    assert image_info.study_instance_uid is None
    assert image_info.frame_uid is None
    assert image_info.class_uid is None
    assert image_info.instance_uid is None
    assert image_info.dicom_file_name is None
    assert image_info.image_set is None
