"""
Tests for the Point model, reader, and writer.
"""
from pathlib import Path
import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session

from pinnacle_io.models import Point, Plan, Patient, Trial
from pinnacle_io.readers.point_reader import PointReader
from pinnacle_io.writers.point_writer import PointWriter
from typing import List


def test_point_initialization():
    """Test creating a Point directly with kwargs."""
    # Test with minimal data. Include one input not in the model to ensure it is ignored.
    point = Point(
        name="test_point",
        x_coord=10.5,
        y_coord=20.5,
        z_coord=30.5,
        x_rotation=0.0,
        y_rotation=0.0,
        z_rotation=0.0,
        radius=1.0,
        color="red",
        coord_sys="CT",
        coordinate_format="%6.2f",
        display_2d="Off",
        display_3d="Off",
        volume_name="TestVolume",
        poi_interpreted_type="MARKER",
        poi_display_on_other_volumes=1,
        is_locked=0,
        non_existent_field="This should be ignored"
    )
    
    assert point.name == "test_point"
    assert point.x_coord == 10.5
    assert point.y_coord == 20.5
    assert point.z_coord == 30.5
    assert point.coordinates == (10.5, 20.5, 30.5)
    assert point.radius == 1.0
    assert point.color == "red"
    assert point.coord_sys == "CT"
    assert point.coordinate_format == "%6.2f"
    assert point.display_2d == "Off"
    assert point.display_3d == "Off"
    assert point.volume_name == "TestVolume"
    assert point.poi_interpreted_type == "MARKER"
    assert point.poi_display_on_other_volumes == 1
    assert point.is_locked == 0
    assert not hasattr(point, "non_existent_field")


def test_point_list_operations():
    """Test working with a list of Point models."""
    # Create an empty list of points
    points: List[Point] = []
    
    # Test adding a point
    point = Point(
        name="test_point",
        x_coord=10.5,
        y_coord=20.5,
        z_coord=30.5,
    )
    points.append(point)
    
    assert len(points) == 1
    assert points[0].name == "test_point"
    
    # Test finding a point by name
    found_point = next((p for p in points if p.name == "test_point"), None)
    assert found_point is not None
    assert found_point.x_coord == 10.5
    
    # Test non-existent point
    not_found = next((p for p in points if p.name == "nonexistent"), None)
    assert not_found is None


def test_read_point_file():
    """Tests reading a valid Points file."""
    points = PointReader.read(Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/Plan_0')

    assert isinstance(points, list)
    assert all(isinstance(point, Point) for point in points)
    
    # Check point data
    assert len(points) == 1
    point = points[0]
    
    assert point.name == "iso"
    assert point.x_coord == -1.20199
    assert point.y_coord == 1.89459
    assert point.z_coord == 2.0
    assert point.radius == 1.0
    assert point.color == "red"
    assert point.coord_sys == "CT"
    assert point.coordinate_format == "%6.2f"
    assert point.display_2d == "Off"
    assert point.display_3d == "Off"
    assert point.volume_name == "LAST^FIRST^M"
    assert point.poi_interpreted_type == "MARKER"
    assert point.poi_display_on_other_volumes == 1
    assert point.is_locked == 0
    
    # Check version information
    assert point.write_version == "Pinnacle v16.0"
    assert point.create_version == "Pinnacle v16.0"
    assert point.login_name == "candor01"
    assert point.create_time_stamp.strftime('%Y-%m-%d %H:%M:%S') == "2020-01-01 10:00:00"
    assert point.write_time_stamp.strftime('%Y-%m-%d %H:%M:%S') == "2020-01-01 10:00:00"


def test_write_point_file():
    """Tests writing a Point file."""
    point = Point(name="test_point")
    
    with pytest.raises(NotImplementedError):
        PointWriter.write(point, "/path/to/point")




def test_point_repr():
    """Test the string representation of Point."""
    point = Point(name="test_point", x_coord=1.0, y_coord=2.0, z_coord=3.0)
    assert repr(point) == "<Point(id=None, name='test_point', coordinates=(1.0, 2.0, 3.0))>"


def test_point_init_with_plan():
    """Test initializing a Point with a Plan."""
    plan = Plan(plan_id=1, plan_name="Test Plan")
    point = Point(name="test_point", x_coord=1.0, y_coord=2.0, z_coord=3.0, plan=plan)
    
    assert point.plan == plan
    assert point.plan_id == plan.id
    assert point in plan.point_list


def test_point_init_with_plan_dict():
    """Test initializing a Point with a Plan dictionary."""
    plan_dict = {"plan_id": 1, "name": "Test Plan"}
    point = Point(name="test_point", x_coord=1.0, y_coord=2.0, z_coord=3.0, plan=plan_dict)
    
    assert point.plan.plan_id == 1
    assert point.plan.name == "Test Plan"
    assert point.plan_id == point.plan.id
    assert point in point.plan.point_list


def test_complete_relationship_chain():
    """Test the complete relationship chain from Patient to Point."""
    # Create a patient
    patient = Patient(patient_id=1, first_name="John", last_name="Doe")
    
    # Create a plan linked to the patient
    plan = Plan(plan_id=1, plan_name="Test Plan", patient=patient)
    
    # Create a trial linked to the plan
    trial = Trial(trial_id=1, trial_name="Test Trial", plan=plan)
    
    # Create a point linked to the plan
    point = Point(name="test_point", x_coord=1.0, y_coord=2.0, z_coord=3.0, plan=plan)
    
    # Verify relationships
    assert point.plan == plan
    assert point in plan.point_list
    assert plan.patient == patient
    assert plan in patient.plan_list
    assert trial in plan.trial_list
    assert trial.plan == plan
