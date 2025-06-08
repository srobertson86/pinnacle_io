"""
Tests for the Plan model, reader, and writer.
"""
from pathlib import Path
import pytest

from pinnacle_io.models import Patient, Plan, ImageSet
from pinnacle_io.readers.plan_reader import PlanReader
from pinnacle_io.writers.plan_writer import PlanWriter
from pinnacle_io.utils.patient_enum import PatientSetupEnum


def test_plan_initialization():
    """Test creating a Plan directly with kwargs."""
    # Test with minimal data. Include one input not in the model to ensure it is ignored.
    plan = Plan(
        plan_id=123,
        plan_name="Test Plan",
        tool_type="Pinnacle^3",
        comment="Test comment",
        physicist="Dr. Smith",
        dosimetrist="John Doe",
        primary_ct_image_set_id=0,
        primary_image_type="Images",
        pinnacle_version_description="16.2",
        is_new_plan_prefix=True,
        plan_is_locked=False,
        ok_for_syntegra_in_launchpad=False,
        fusion_id_array="",
        non_existent_field="This should be ignored"
    )
    
    assert plan.plan_id == 123
    assert plan.name == "Test Plan"
    assert plan.tool_type == "Pinnacle^3"
    assert plan.comment == "Test comment"
    assert plan.physicist == "Dr. Smith"
    assert plan.dosimetrist == "John Doe"
    assert plan.primary_ct_image_set_id == 0
    assert plan.primary_image_type == "Images"
    assert plan.pinnacle_version_description == "16.2"
    assert plan.is_new_plan_prefix is True
    assert plan.plan_is_locked is False
    assert plan.ok_for_syntegra_in_launchpad is False
    assert plan.fusion_id_array == ""
    assert not hasattr(plan, "non_existent_field")
    assert plan.plan_folder == "Plan_123"


def test_plan_methods():
    """Test Plan methods."""
    plan = Plan(
        plan_id=1,
        plan_name="Test Plan",
    )
    
    # Test plan_folder property
    assert plan.plan_folder == "Plan_1"
    
    # Test string representation
    assert repr(plan) == f"<Plan(id={plan.id}, plan_id={plan.plan_id}, name='{plan.name}')>"


def test_read_plan_file():
    """Tests reading a valid Plan file."""
    # The PlanReader reads from a Patient file, not directly from a Plan file
    test_data_dir = Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1'
    plans = PlanReader.read(str(test_data_dir))

    assert isinstance(plans, list)
    assert len(plans) > 0
    
    plan = plans[0]
    assert isinstance(plan, Plan)
    
    # Check basic plan properties
    assert plan.plan_id == 0
    assert plan.name == "BRAIN"
    assert plan.tool_type == "Pinnacle^3"
    assert plan.comment == ""
    assert plan.physicist == "MAX WELLDOSE PHD"
    assert plan.dosimetrist == "DOSEY CALC CMD"
    assert plan.primary_ct_image_set_id == 0
    assert plan.primary_image_type == "Images"
    assert plan.pinnacle_version_description == "Pinnacle 16.0"
    assert plan.is_new_plan_prefix == 1
    assert plan.plan_is_locked == 1
    assert plan.ok_for_syntegra_in_launchpad == 0
    # assert plan.fusion_id_array == [] # TODO: Not yet implemented
    
    # Check version information
    assert plan.write_version == "Launch Pad: 16.2"
    assert plan.create_version == "Launch Pad: 16.0"
    assert plan.login_name == "candor01"
    assert plan.create_time_stamp.strftime("%Y-%m-%d %H:%M:%S") == "2020-01-01 10:00:00"
    assert plan.write_time_stamp.strftime("%Y-%m-%d %H:%M:%S") == "2020-01-01 10:00:00"
    assert plan.last_modified_time_stamp.strftime("%Y-%m-%d %H:%M:%S") == "2020-01-01 10:00:00"

    # Check relationships
    assert hasattr(plan, 'trial_list')
    assert isinstance(plan.trial_list, list)
    assert len(plan.trial_list) == 0
    
    # Check patient position
    assert hasattr(plan, 'patient_position')
    assert plan.patient_position == PatientSetupEnum.HFS


def test_plan_relationships():
    """Test Plan relationships."""
    plan = Plan(
        plan_id=1,
        plan_name="Test Plan",
    )
    
    # Test relationships are accessible
    assert hasattr(plan, 'patient')
    assert hasattr(plan, 'trial_list')
    assert hasattr(plan, 'roi_list')
    assert hasattr(plan, 'point_list')
    
    # Test that relationships are initially empty
    assert plan.trial_list == []
    assert plan.roi_list == []
    assert plan.point_list == []


def test_write_plan_file():
    """Tests writing a Plan file."""
    plan = Plan(
        plan_id=1,
        plan_name="Test Plan",
    )
    
    with pytest.raises(NotImplementedError):
        PlanWriter.write(plan, "/path/to/plan")


def test_plan_relationships_initialization():
    """Test that all Plan relationships are initialized correctly."""
    # Test initializing with a patient directly
    patient = Patient(
        patient_id=123,
        first_name="John",
        last_name="Doe"
    )
    
    plan = Plan(
        plan_id=1,
        plan_name="Test Plan",
        patient=patient
    )
    
    # Verify patient relationship
    assert plan.patient is patient
    assert plan.patient_id == patient.id
    assert plan in patient.plan_list
    
    # Test initializing with a patient as a dictionary
    plan2 = Plan(
        plan_id=2,
        plan_name="Test Plan 2",
        patient={
            "patient_id": 456,
            "first_name": "Jane",
            "last_name": "Smith"
        }
    )
    
    # Verify patient relationship
    assert plan2.patient is not None
    assert plan2.patient.patient_id == 456
    assert plan2.patient.first_name == "Jane"
    assert plan2.patient.last_name == "Smith"
    assert plan2 in plan2.patient.plan_list
    
    # Test initializing with trials
    plan3 = Plan(
        plan_id=3,
        plan_name="Test Plan 3",
        trial_list=[
            {
                "trial_id": 1,
                "trial_name": "Trial 1"
            },
            {
                "trial_id": 2,
                "trial_name": "Trial 2"
            }
        ]
    )
    
    # Verify trials relationship
    assert len(plan3.trial_list) == 2
    assert plan3.trial_list[0].trial_id == 1
    assert plan3.trial_list[0].name == "Trial 1"
    assert plan3.trial_list[0].plan is plan3
    assert plan3.trial_list[1].trial_id == 2
    assert plan3.trial_list[1].name == "Trial 2"
    assert plan3.trial_list[1].plan is plan3
    
    # Test initializing with TrialList (PascalCase)
    plan4 = Plan(
        plan_id=4,
        plan_name="Test Plan 4",
        TrialList=[
            {
                "trial_id": 3,
                "trial_name": "Trial 3"
            }
        ]
    )
    
    # Verify TrialList relationship
    assert len(plan4.trial_list) == 1
    assert plan4.trial_list[0].trial_id == 3
    assert plan4.trial_list[0].name == "Trial 3"
    assert plan4.trial_list[0].plan is plan4
    
    # Test initializing with ROIs
    plan5 = Plan(
        plan_id=5,
        plan_name="Test Plan 5",
        roi_list=[
            {
                "roi_number": 1,
                "name": "PTV"
            },
            {
                "roi_number": 2,
                "name": "OAR"
            }
        ]
    )
    
    # Verify ROIs relationship
    assert len(plan5.roi_list) == 2
    assert plan5.roi_list[0].roi_number == 1
    assert plan5.roi_list[0].name == "PTV"
    assert plan5.roi_list[0].plan is plan5
    assert plan5.roi_list[1].roi_number == 2
    assert plan5.roi_list[1].name == "OAR"
    assert plan5.roi_list[1].plan is plan5
    
    # Test initializing with ROIList (PascalCase)
    plan6 = Plan(
        plan_id=6,
        plan_name="Test Plan 6",
        ROIList=[
            {
                "roi_number": 3,
                "name": "BODY"
            }
        ]
    )
    
    # Verify ROIList relationship
    assert len(plan6.roi_list) == 1
    assert plan6.roi_list[0].roi_number == 3
    assert plan6.roi_list[0].name == "BODY"
    assert plan6.roi_list[0].plan is plan6
    
    # Test initializing with points
    plan7 = Plan(
        plan_id=7,
        plan_name="Test Plan 7",
        point_list=[
            {
                "name": "ISO",
                "x_coord": 10.0,
                "y_coord": 20.0,
                "z_coord": 30.0
            },
            {
                "name": "REF",
                "x_coord": 15.0,
                "y_coord": 25.0,
                "z_coord": 35.0
            }
        ]
    )
    
    # Verify points relationship
    assert len(plan7.point_list) == 2
    assert plan7.point_list[0].name == "ISO"
    assert plan7.point_list[0].x_coord == 10.0
    assert plan7.point_list[0].y_coord == 20.0
    assert plan7.point_list[0].z_coord == 30.0
    assert plan7.point_list[0].plan is plan7
    assert plan7.point_list[1].name == "REF"
    assert plan7.point_list[1].x_coord == 15.0
    assert plan7.point_list[1].y_coord == 25.0
    assert plan7.point_list[1].z_coord == 35.0
    assert plan7.point_list[1].plan is plan7
    
    # Test initializing with PointList (PascalCase)
    plan8 = Plan(
        plan_id=8,
        plan_name="Test Plan 8",
        PointList=[
            {
                "name": "MARK",
                "x_coord": 5.0,
                "y_coord": 10.0,
                "z_coord": 15.0
            }
        ]
    )
    
    # Verify PointList relationship
    assert len(plan8.point_list) == 1
    assert plan8.point_list[0].name == "MARK"
    assert plan8.point_list[0].x_coord == 5.0
    assert plan8.point_list[0].y_coord == 10.0
    assert plan8.point_list[0].z_coord == 15.0
    assert plan8.point_list[0].plan is plan8
    
    # Test initializing with all relationships
    complete_plan = Plan(
        plan_id=9,
        plan_name="Complete Plan",
        patient=patient,
        trial_list=[
            {"trial_id": 4, "trial_name": "Complete Trial"}
        ],
        roi_list=[
            {"roi_number": 4, "name": "Complete ROI"}
        ],
        point_list=[
            {"name": "Complete Point", "x_coord": 1.0, "y_coord": 2.0, "z_coord": 3.0}
        ]
    )
    
    # Verify all relationships
    assert complete_plan.patient is patient
    assert complete_plan in patient.plan_list
    assert len(complete_plan.trial_list) == 1
    assert complete_plan.trial_list[0].name == "Complete Trial"
    assert complete_plan.trial_list[0].plan is complete_plan
    assert len(complete_plan.roi_list) == 1
    assert complete_plan.roi_list[0].name == "Complete ROI"
    assert complete_plan.roi_list[0].plan is complete_plan
    assert len(complete_plan.point_list) == 1
    assert complete_plan.point_list[0].name == "Complete Point"
    assert complete_plan.point_list[0].plan is complete_plan


def test_plan_image_set_relationship():
    """Test the relationship between Plan and ImageSet."""
    # Create an image set
    image_set = ImageSet(
        series_uid="1.2.3.4.5",
        image_name="Test CT",
        modality="CT"
    )
    
    # Create a plan that references this image set
    plan = Plan(
        plan_id=10,
        plan_name="Test Plan with ImageSet",
        primary_ct_image_set=image_set
    )
    
    # Verify the relationship from Plan to ImageSet
    assert plan.primary_ct_image_set is image_set
    assert plan.primary_ct_image_set_id == image_set.id
    
    # Verify the relationship from ImageSet to Plan
    assert plan in image_set.plan_list
    assert len(image_set.plan_list) == 1