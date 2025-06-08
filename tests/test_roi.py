"""
Tests for the ROI model, reader, and writer.
"""
from pathlib import Path
from typing import List
import pytest
import numpy as np
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session

from pinnacle_io.models import ROI, Curve, Plan, Patient, Trial
from pinnacle_io.readers.roi_reader import ROIReader
from pinnacle_io.writers.roi_writer import ROIWriter


def test_curve_initialization():
    """Test creating a Curve directly with kwargs."""
    # Test with minimal data
    points = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    curve = Curve(
        points=points,
        contour_geometric_type="CLOSED_PLANAR",
        flags=131092,
        block_size=32,
        num_points=2,
        curve_number=1,
        slice_index=5,
        z_position=3.0,
        non_existent_field="This should be ignored"
    )
    
    assert np.array_equal(curve.points, points)
    assert curve.contour_geometric_type == "CLOSED_PLANAR"
    assert curve.flags == 131092
    assert curve.block_size == 32
    assert curve.num_points == 2
    assert curve.curve_number == 1
    assert curve.slice_index == 5
    assert curve.z_position == 3.0
    assert curve.point_count == 2
    assert not hasattr(curve, "non_existent_field")
    assert np.array_equal(curve.get_curve_data(), [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])


def test_roi_initialization():
    """Test creating an ROI directly with kwargs."""
    # Test with minimal data
    roi = ROI(
        roi_number=1,
        name="TestROI",
        volume_name="TestVolume",
        stats_volume_name="TestVolume",
        roi_description="Test ROI",
        roi_generation_algorithm="AUTOMATIC",
        roi_type="STRUCTURE",
        structure_type="ORGAN",
        author="TestUser",
        organ_name="TestOrgan",
        flags=135168,
        roi_interpreted_type="ORGAN",
        color="red",
        box_size=5.0,
        line_2d_width=2,
        line_3d_width=1,
        paint_brush_radius=0.4,
        paint_allow_curve_closing=True,
        curve_min_area=0.1,
        curve_overlap_min=88.0,
        lower_threshold=800.0,
        upper_threshold=4096.0,
        radius=0.0,
        density=0.0,
        density_units="g/cm^3",
        override_data=True,
        override_order=1,
        override_material=False,
        material=None,
        invert_density_loading=False,
        volume=0.95,
        pixel_min=0.0,
        pixel_max=4071.0,
        pixel_mean=750.62,
        pixel_std=1072.4,
        bev_drr_outline=False,
        display_on_other_vols=True,
        is_linked=False,
        non_existent_field="This should be ignored"
    )
    
    # Test ROI properties
    assert roi.roi_number == 1
    assert roi.name == "TestROI"
    assert roi.volume_name == "TestVolume"
    assert roi.stats_volume_name == "TestVolume"
    assert roi.roi_description == "Test ROI"
    assert roi.roi_generation_algorithm == "AUTOMATIC"
    assert roi.roi_type == "STRUCTURE"
    assert roi.structure_type == "ORGAN"
    assert roi.author == "TestUser"
    assert roi.organ_name == "TestOrgan"
    assert roi.flags == 135168
    assert roi.roi_interpreted_type == "ORGAN"
    assert roi.color == "red"
    assert roi.box_size == 5.0
    assert roi.line_2d_width == 2
    assert roi.line_3d_width == 1
    assert roi.paint_brush_radius == 0.4
    assert roi.paint_allow_curve_closing is True
    assert roi.curve_min_area == 0.1
    assert roi.curve_overlap_min == 88.0
    assert roi.lower_threshold == 800.0
    assert roi.upper_threshold == 4096.0
    assert roi.radius == 0.0
    assert roi.density == 0.0
    assert roi.density_units == "g/cm^3"
    assert roi.override_data is True
    assert roi.override_order == 1
    assert roi.override_material is False
    assert roi.material is None
    assert roi.invert_density_loading is False
    assert roi.volume == 0.95
    assert roi.pixel_min == 0.0
    assert roi.pixel_max == 4071.0
    assert roi.pixel_mean == 750.62
    assert roi.pixel_std == 1072.4
    assert roi.bev_drr_outline is False
    assert roi.display_on_other_vols is True
    assert roi.is_linked is False
    assert not hasattr(roi, "non_existent_field")


def test_roi_list_operations():
    """Test working with a list of ROIs."""
    # Create a list to hold ROIs
    rois: List[ROI] = []
    
    # Test adding an ROI
    roi1 = ROI(name="TestROI1", roi_number=1)
    rois.append(roi1)
    
    assert len(rois) == 1
    assert rois[0].name == "TestROI1"
    
    # Test finding ROI by number
    found_roi = next((r for r in rois if r.roi_number == 1), None)
    assert found_roi is not None
    assert found_roi.name == "TestROI1"
    
    # Test finding ROI by name
    found_roi = next((r for r in rois if r.name == "TestROI1"), None)
    assert found_roi is not None
    assert found_roi.roi_number == 1
    
    # Test non-existent ROI
    found_roi = next((r for r in rois if r.roi_number == 2), None)
    assert found_roi is None
    
    found_roi = next((r for r in rois if r.name == "Nonexistent"), None)
    assert found_roi is None


def test_read_roi_file():
    """Tests reading a valid ROI file."""
    rois = ROIReader.read(
        Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/Plan_0'
    )
    
    assert isinstance(rois, list)
    assert all(isinstance(roi, ROI) for roi in rois)
    assert len(rois) > 0
    
    # Test the first ROI
    roi = rois[0]
    assert roi.name == "bb"
    assert roi.volume_name == "LAST^FIRST^M"
    assert roi.stats_volume_name == "LAST^FIRST^M"
    assert roi.flags == 135168
    assert roi.roi_interpreted_type == "ORGAN"
    assert roi.color == "red"
    assert roi.box_size == 5.0
    assert roi.line_2d_width == 2
    assert roi.line_3d_width == 1
    assert roi.paint_brush_radius == 0.4
    assert roi.paint_allow_curve_closing is True
    assert roi.curve_min_area == 0.1
    assert roi.curve_overlap_min == 88.0
    assert roi.lower_threshold == 800.0
    assert roi.upper_threshold == 4096.0
    assert roi.radius == 0.0
    assert roi.density == 0.0
    assert roi.density_units == "g/cm^3"
    assert roi.override_data is True
    assert roi.override_order == 1
    assert roi.override_material is False
    assert roi.material is None
    assert roi.invert_density_loading is False
    assert roi.volume == 0.953669
    assert roi.pixel_min == 0.0
    assert roi.pixel_max == 4071.0
    assert roi.pixel_mean == 750.617
    assert roi.pixel_std == 1072.4
    assert roi.bev_drr_outline is False
    assert roi.display_on_other_vols is True
    assert roi.is_linked is False
    
    # Test curves in the first ROI
    assert len(roi.curve_list) > 0
    curve = roi.curve_list[0]
    assert curve.flags == 131092
    assert curve.block_size == 32
    assert curve.num_points == 25
    assert curve.curve_number == 0
    assert curve.point_count == 25
    assert len(curve.points) == 25
    assert len(curve.get_curve_data()) == 75  # 25 points * 3 coordinates


def test_write_roi_file():
    """Tests writing an ROI file."""
    roi = ROI(name="TestROI")
    
    with pytest.raises(NotImplementedError):
        ROIWriter.write(roi, "/path/to/roi")


def test_curve_repr():
    """Test the string representation of Curve."""
    # Initialize with points_json to avoid JSON parsing error
    curve = Curve(curve_number=1, num_points=0, points_json="[]")
    assert repr(curve) == "<Curve(id=None, curve_number=1, point_count=0)>"
    

def test_roi_repr():
    """Test the string representation of ROI."""
    roi = ROI(name="TestROI", roi_number=1)
    assert repr(roi) == "<ROI(id=None, number=1, name='TestROI')>"


def test_roi_init_with_plan():
    """Test initializing an ROI with a Plan."""
    plan = Plan(plan_id=1, plan_name="Test Plan")
    roi = ROI(name="TestROI", roi_number=1, plan=plan)
    
    assert roi.plan == plan
    assert roi.plan_id == plan.id
    assert roi in plan.roi_list


def test_roi_init_with_plan_dict():
    """Test initializing an ROI with a Plan dictionary."""
    plan_dict = {"plan_id": 1, "plan_name": "Test Plan"}
    roi = ROI(name="TestROI", roi_number=1, plan=plan_dict)
    
    assert roi.plan.plan_id == 1
    assert roi.plan.name == "Test Plan"
    assert roi.plan_id == roi.plan.id
    assert roi in roi.plan.roi_list


def test_roi_init_with_curves():
    """Test initializing an ROI with Curves."""
    curve1 = Curve(points=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], curve_number=1)
    curve2 = Curve(points=[[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]], curve_number=2)
    roi = ROI(name="TestROI", roi_number=1, curve_list=[curve1, curve2])
    
    assert len(roi.curve_list) == 2
    assert roi.curve_list[0].curve_number == 1
    assert roi.curve_list[1].curve_number == 2
    assert roi.curve_list[0].roi == roi
    assert roi.curve_list[1].roi == roi


def test_roi_init_with_curve_list_kwarg():
    """Test initializing an ROI with CurveList keyword argument."""
    curve_dict1 = {"points": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "curve_number": 1}
    curve_dict2 = {"points": [[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]], "curve_number": 2}
    roi = ROI(name="TestROI", roi_number=1, CurveList=[curve_dict1, curve_dict2])
    
    assert len(roi.curve_list) == 2
    assert roi.curve_list[0].curve_number == 1
    assert roi.curve_list[1].curve_number == 2
    assert roi.curve_list[0].roi == roi
    assert roi.curve_list[1].roi == roi


def test_complete_relationship_chain():
    """Test the complete relationship chain from Patient to ROI."""
    # Create a patient
    patient = Patient(patient_id=1, first_name="John", last_name="Doe")
    
    # Create a plan linked to the patient
    plan = Plan(plan_id=1, plan_name="Test Plan", patient=patient)
    
    # Create a trial linked to the plan
    trial = Trial(trial_id=1, trial_name="Test Trial", plan=plan)
    
    # Create an ROI linked to the plan
    roi = ROI(name="TestROI", roi_number=1, plan=plan)
    
    # Create curves linked to the ROI
    curve1 = Curve(points=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], curve_number=1, roi=roi)
    curve2 = Curve(points=[[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]], curve_number=2, roi=roi)
    
    # Verify relationships
    assert roi.plan == plan
    assert roi in plan.roi_list
    assert plan.patient == patient
    assert plan in patient.plan_list
    assert trial in plan.trial_list
    assert trial.plan == plan
    assert curve1 in roi.curve_list
    assert curve2 in roi.curve_list
    assert curve1.roi == roi
    assert curve2.roi == roi
