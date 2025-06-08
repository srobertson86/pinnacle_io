"""
Unit tests for the Trial model.
"""
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session

from pathlib import Path
import pytest

from pinnacle_io.models import Trial, Plan, Patient, Beam, PatientSetup
from pinnacle_io.utils.patient_enum import PatientSetupEnum
from pinnacle_io.readers.trial_reader import TrialReader 
from pinnacle_io.writers.trial_writer import TrialWriter


def test_init_with_kwargs():
    """Test initializing a Trial with keyword arguments."""
    trial = Trial(trial_id=1, trial_name="Test Trial")
    assert trial.trial_id == 1
    assert trial.name == "Test Trial"


def test_init_with_plan():
    """Test initializing a Trial with a Plan."""
    plan = Plan(plan_id=1, plan_name="Test Plan")
    trial = Trial(plan=plan, trial_id=1, trial_name="Test Trial")
    
    assert trial.plan == plan
    assert trial.plan_id == plan.id
    assert trial in plan.trial_list


def test_init_with_plan_dict():
    """Test initializing a Trial with a Plan dictionary."""
    plan_dict = {"plan_id": 1, "plan_name": "Test Plan"}
    trial = Trial(plan=plan_dict, trial_id=1, trial_name="Test Trial")
    
    assert trial.plan.plan_id == 1
    assert trial.plan.name == "Test Plan"
    assert trial.plan_id == trial.plan.id
    assert trial in trial.plan.trial_list


def test_init_with_beams():
    """Test initializing a Trial with Beams."""
    beam1 = Beam(beam_number=1, name="Beam 1")
    beam2 = Beam(beam_number=2, name="Beam 2")
    trial = Trial(trial_id=1, trial_name="Test Trial", beam_list=[beam1, beam2])
    
    assert len(trial.beam_list) == 2
    assert trial.beam_list[0].beam_number == 1
    assert trial.beam_list[1].beam_number == 2
    assert trial.beam_list[0].trial == trial
    assert trial.beam_list[1].trial == trial


def test_init_with_beam_list_kwarg():
    """Test initializing a Trial with BeamList keyword argument."""
    beam_dict1 = {"beam_number": 1, "name": "Beam 1"}
    beam_dict2 = {"beam_number": 2, "name": "Beam 2"}
    trial = Trial(trial_id=1, trial_name="Test Trial", BeamList=[beam_dict1, beam_dict2])
    
    assert len(trial.beam_list) == 2
    assert trial.beam_list[0].beam_number == 1
    assert trial.beam_list[1].beam_number == 2
    assert trial.beam_list[0].trial == trial
    assert trial.beam_list[1].trial == trial


def test_get_beam_by_number():
    """Test getting a beam by its number."""
    beam1 = Beam(beam_number=1, name="Beam 1")
    beam2 = Beam(beam_number=2, name="Beam 2")
    trial = Trial(trial_id=1, trial_name="Test Trial", beam_list=[beam1, beam2])
    
    assert trial.get_beam_by_number(1) == beam1
    assert trial.get_beam_by_number(2) == beam2
    assert trial.get_beam_by_number(3) is None


def test_get_beam_by_name():
    """Test getting a beam by its name."""
    # Create a trial first
    trial = Trial(trial_id=1, name="Test Trial")
    
    # Create beams and add them to the trial
    beam1 = Beam(beam_number=1, name="Beam 1", trial=trial)
    beam2 = Beam(beam_number=2, name="Beam 2", trial=trial)
    
    assert trial.get_beam_by_name("Beam 1") == beam1
    assert trial.get_beam_by_name("Beam 2") == beam2
    assert trial.get_beam_by_name("Beam 3") is None


def test_patient_position():
    """Test getting patient position."""
    plan = Plan(plan_id=1, plan_name="Test Plan")
    trial = Trial(trial_id=1, name="Test Trial", plan=plan)
    patient_setup = PatientSetup(patient_setup=PatientSetupEnum.HFS.value, plan=plan)
    
    # Make sure the patient_setup property is set on the PatientSetup instance
    assert patient_setup.patient_setup_enum == PatientSetupEnum.HFS
    
    # Now test the property on the trial
    assert trial.plan.patient_position == PatientSetupEnum.HFS


def test_complete_relationship_chain():
    """Test the complete relationship chain from Patient to Trial."""
    # Create a patient
    patient = Patient(patient_id=1, first_name="John", last_name="Doe")
    
    # Create a plan linked to the patient
    plan = Plan(plan_id=1, plan_name="Test Plan", patient=patient)
    
    # Create a trial linked to the plan
    trial = Trial(trial_id=1, trial_name="Test Trial", plan=plan)
    
    # Create beams linked to the trial
    beam1 = Beam(beam_number=1, name="Beam 1", trial=trial)
    beam2 = Beam(beam_number=2, name="Beam 2", trial=trial)
    
    # Verify relationships
    assert trial.plan == plan
    assert trial in plan.trial_list
    assert plan.patient == patient
    assert plan in patient.plan_list
    assert beam1 in trial.beam_list
    assert beam2 in trial.beam_list
    assert beam1.trial == trial
    assert beam2.trial == trial


def test_read_trial_file():
    """Tests reading a valid Trial file."""
    plan_path = Path(__file__).parent / 'test_data/01/Institution_1/Mount_0/Patient_1/Plan_0'
    trials = TrialReader.read(plan_path)

    # Verify we got trials back
    assert len(trials) > 0
    trial = trials[0]  # Get first trial
    
    # Basic trial properties
    assert isinstance(trial, Trial)
    assert trial.name == "Trial_1"
    
    # Check beam list
    assert len(trial.beam_list) == 2
    beam = trial.beam_list[0]
    assert beam.name == "02 Lao Brain"
    assert beam.modality == "Photons"
    assert beam.machine_energy_name == "6X"
    
    # Check prescription
    assert len(trial.prescription_list) == 1
    prescription = trial.prescription_list[0]
    assert prescription.name == "Brain"
    assert prescription.prescription_dose == 250
    assert prescription.number_of_fractions == 12
    assert prescription.prescription_point == "iso"

    # Check dose grid settings
    assert trial.dose_grid.voxel_size.x == 0.3
    assert trial.dose_grid.voxel_size.y == 0.3
    assert trial.dose_grid.voxel_size.z == 0.3
    assert trial.dose_grid.dimension.x == 93  
    assert trial.dose_grid.dimension.y == 110
    assert trial.dose_grid.dimension.z == 89


def test_write_trial_file(tmp_path):
    """Tests writing a Trial file."""
    # Create a minimal trial
    trial = Trial()
    with pytest.raises(NotImplementedError):
        TrialWriter.write([trial], tmp_path / "Patient_1/Plan_0/plan.Trial")
        