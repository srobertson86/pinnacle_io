"""
Tests for the PatientSetup model.
"""

import numpy as np
from pinnacle_io.models import (
    PatientSetup,
    Plan,
)
from pinnacle_io.utils.patient_enum import (
    PatientPositionEnum,
    PatientOrientationEnum,
    TableMotionEnum,
    PatientSetupEnum,
)


def test_patient_setup_initialization():
    """Test PatientSetup initialization with all fields."""
    pinnacle_to_dicom = np.array([[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    dicom_to_pinnacle = np.array([[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    image_orientation = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]    
    patient_setup = PatientSetup(
        position=PatientPositionEnum.Supine.value,
        orientation=PatientOrientationEnum.HeadFirst.value,
        table_motion= TableMotionEnum.Unknown.value,
        patient_setup=PatientSetupEnum.HFS.value,
        pinnacle_to_dicom_matrix=pinnacle_to_dicom.tolist(),
        dicom_to_pinnacle_matrix=dicom_to_pinnacle.tolist(),
        image_orientation_patient=image_orientation,
        patient_position_description="Head First Supine"
    )

    # Test all fields are set correctly
    assert patient_setup.position == PatientPositionEnum.Supine.value
    assert patient_setup.orientation == PatientOrientationEnum.HeadFirst.value
    assert patient_setup.table_motion == TableMotionEnum.Unknown.value
    assert patient_setup.patient_setup == PatientSetupEnum.HFS.value
    assert patient_setup.patient_position_description == "Head First Supine"
    
    # Test matrix conversions
    np.testing.assert_array_equal(
        patient_setup.pinnacle_to_dicom_matrix_array,
        pinnacle_to_dicom
    )
    np.testing.assert_array_equal(
        patient_setup.dicom_to_pinnacle_matrix_array,
        dicom_to_pinnacle
    )
    assert patient_setup.image_orientation_patient_array == image_orientation


def test_patient_setup_plan_relationship():
    """Test PatientSetup relationship with Plan."""
    plan = Plan(name="Plan1")    
    patient_setup = PatientSetup(
        position=PatientPositionEnum.Supine.value,
        orientation=PatientOrientationEnum.HeadFirst.value,
        plan=plan
    )
    
    # Verify plan relationship
    assert patient_setup.plan is plan
    assert patient_setup.plan_id == plan.id
    assert plan._patient_position is patient_setup


def test_patient_setup_enum_properties():
    """Test enum property getters for PatientSetup."""    
    patient_setup = PatientSetup(
        position=PatientPositionEnum.Supine.value,
        orientation=PatientOrientationEnum.HeadFirst.value,
        table_motion=TableMotionEnum.IntoScanner.value,
        patient_setup=PatientSetupEnum.HFS.value
    )

    assert patient_setup.position_enum == PatientPositionEnum.Supine
    assert patient_setup.orientation_enum == PatientOrientationEnum.HeadFirst
    assert patient_setup.table_motion_enum == TableMotionEnum.IntoScanner
    assert patient_setup.patient_setup_enum == PatientSetupEnum.HFS

    # Test unknown values
    patient_setup.position = "INVALID"
    patient_setup.orientation = "INVALID"
    patient_setup.table_motion = "INVALID"
    patient_setup.patient_setup = "INVALID"

    assert patient_setup.position_enum == PatientPositionEnum.Unknown
    assert patient_setup.orientation_enum == PatientOrientationEnum.Unknown
    assert patient_setup.table_motion_enum == TableMotionEnum.Unknown
    assert patient_setup.patient_setup_enum == PatientSetupEnum.Unknown


def test_coordinate_transformations():
    """Test coordinate transformation methods."""
    # Test HFS setup (default transformation matrices)
    patient_setup = PatientSetup(patient_setup=PatientSetupEnum.HFS.value)
    
    # Matrices are initialized by the PatientSetup constructor based on HFS setup

    # Test single point transformation
    pinnacle_point = [10.0, 20.0, 30.0]
    dicom_point = patient_setup.transform_point_pinnacle_to_dicom(pinnacle_point)
    assert dicom_point == [-10.0, -20.0, 30.0]

    # Transform back to pinnacle coordinates
    back_to_pinnacle = patient_setup.transform_point_dicom_to_pinnacle(dicom_point)
    assert back_to_pinnacle == [10.0, 20.0, 30.0]

    # Test contour transformation
    contour_points = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    dicom_contour = patient_setup.transform_contour_pinnacle_to_dicom(contour_points)
    assert dicom_contour == [[-1.0, -2.0, 3.0], [-4.0, -5.0, 6.0]]

    # Transform contour back to pinnacle coordinates
    back_to_pinnacle_contour = patient_setup.transform_contour_dicom_to_pinnacle(dicom_contour)
    assert back_to_pinnacle_contour == contour_points


def test_different_patient_setups():
    """Test transformation matrices for different patient setups."""
    test_cases = [
        (PatientSetupEnum.HFS, [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0]),  # Head First Supine
        (PatientSetupEnum.HFP, [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]),   # Head First Prone
        (PatientSetupEnum.FFS, [1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0]),  # Feet First Supine
        (PatientSetupEnum.FFP, [-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0])   # Feet First Prone
    ]

    for setup, x_row, y_row, z_row in test_cases:
        patient_setup = PatientSetup(patient_setup=setup.value)
        
        # Matrices are initialized by the PatientSetup constructor based on the setup enum

        # Check transformation matrix
        matrix_array = patient_setup.pinnacle_to_dicom_matrix_array
        np.testing.assert_array_equal(matrix_array[0], x_row)
        np.testing.assert_array_equal(matrix_array[1], y_row)
        np.testing.assert_array_equal(matrix_array[2], z_row)
        np.testing.assert_array_equal(matrix_array[3], [0, 0, 0, 1])


def test_invalid_matrix_handling():
    """Test handling of invalid transformation matrices."""
    patient_setup = PatientSetup()
    patient_setup.pinnacle_to_dicom_matrix = "not a valid json string"
    patient_setup.dicom_to_pinnacle_matrix = "not a valid json string"
    patient_setup.image_orientation_patient = "not a valid comma separated string"

    # Should return identity matrix for invalid transformations
    np.testing.assert_array_equal(
        patient_setup.pinnacle_to_dicom_matrix_array,
        np.eye(4)
    )
    np.testing.assert_array_equal(
        patient_setup.dicom_to_pinnacle_matrix_array,
        np.eye(4)
    )
    # Should return default orientation for invalid image orientation
    assert patient_setup.image_orientation_patient_array == [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]


def test_patient_setup_repr():
    """Test the __repr__ method of PatientSetup."""
    patient_setup = PatientSetup(
        patient_setup=PatientSetupEnum.HFS.value
    )
    
    expected_repr = f"<PatientSetup(id=None, setup='{PatientSetupEnum.HFS.value}')>"
    assert repr(patient_setup) == expected_repr
