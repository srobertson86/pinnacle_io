"""
Tests for the PhotonEnergy, ElectronEnergy and OutputFactor models.

This module specifically tests the polymorphic behavior of the machine energy classes,
including type discrimination, polymorphic loading, and relationship handling.
"""

from typing import List
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from pinnacle_io.models import (
    PhotonEnergy, ElectronEnergy, OutputFactor, Machine, MachineEnergy, PhysicsData
)


@pytest.fixture
def db_session():
    """Create an in-memory database session for testing."""
    engine = create_engine("sqlite:///:memory:")
    MachineEnergy.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def test_machine(db_session: Session) -> Machine:
    """Create a test machine with both photon and electron energies."""
    machine = Machine(name="Test Machine")
    
    # Add photon energies
    machine.photon_energy_list.extend([
        PhotonEnergy(name="6X", value=6.0),
        PhotonEnergy(name="10X", value=10.0)
    ])
    
    # Add electron energies
    machine.electron_energy_list.extend([
        ElectronEnergy(name="6E", value=6.0),
        ElectronEnergy(name="9E", value=9.0)
    ])
    
    db_session.add(machine)
    db_session.commit()
    return machine


def test_output_factor_repr():
    """Test the __repr__ method of the OutputFactor class."""
    output_factor = OutputFactor(
        id=42,
        dose_per_mu_at_calibration=1.0
    )

    expected_repr = "<OutputFactor(id=42, dose_per_mu_at_calibration=1.0)>"
    assert repr(output_factor) == expected_repr


def test_photon_energy_repr():
    """Test the __repr__ method of the PhotonEnergy class."""
    energy = PhotonEnergy(
        id=42,
        name="6X",
        value=6.0,
    )

    expected_repr = "<PhotonEnergy(id=42, name='6X', value=6.0)>"
    assert repr(energy) == expected_repr


def test_electron_energy_repr():
    """Test the __repr__ method of the ElectronEnergy class."""
    energy = ElectronEnergy(
        id=42,
        name="6E",
        value=6.0,
    )

    expected_repr = "<ElectronEnergy(id=42, name='6E', value=6.0)>"
    assert repr(energy) == expected_repr


def test_output_factor_initialization():
    """Test creating an OutputFactor with all fields."""
    output_factor = OutputFactor(
        reference_depth=10.0,
        source_to_calibration_point_distance=100.0,
        electron_ssd_tolerance=5.0,
        dose_per_mu_at_calibration=1.0,
        min_mlc_position_at_calibration=0.5,
        calculated_calibration_dose=100.0,
        computation_version="1.0",
        calculated_calibration_dose_valid=1
    )

    # Verify all fields are set correctly
    assert output_factor.reference_depth == 10.0
    assert output_factor.source_to_calibration_point_distance == 100.0
    assert output_factor.electron_ssd_tolerance == 5.0
    assert output_factor.dose_per_mu_at_calibration == 1.0
    assert output_factor.min_mlc_position_at_calibration == 0.5
    assert output_factor.calculated_calibration_dose == 100.0
    assert output_factor.computation_version == "1.0"
    assert output_factor.calculated_calibration_dose_valid == 1


def test_photon_energy_initialization():
    """Test creating a PhotonEnergy with all fields."""
    energy = PhotonEnergy(
        value=6.0,
        name="6X",
        scan_pattern_label="Pattern1",
        default_block_and_tray_factor=0.95,
        default_tray_factor=0.98,
        default_mlc_factor=0.99,
        initial_dose_rate_for_table=300.0,
        default_dose_rate=600.0,
        fluence_mode=1,
        fluence_mode_id="MODE1",
        high_dose_technique=0
    )

    # Verify all fields are set correctly
    assert energy.value == 6.0
    assert energy.name == "6X"
    assert energy.type == "photon"
    assert energy.scan_pattern_label == "Pattern1"
    assert energy.default_block_and_tray_factor == 0.95
    assert energy.default_tray_factor == 0.98
    assert energy.default_mlc_factor == 0.99
    assert energy.initial_dose_rate_for_table == 300.0
    assert energy.default_dose_rate == 600.0
    assert energy.fluence_mode == 1
    assert energy.fluence_mode_id == "MODE1"
    assert energy.high_dose_technique == 0


def test_electron_energy_initialization():
    """Test creating an ElectronEnergy with all fields."""
    energy = ElectronEnergy(
        value=6.0,
        name="6E",
        scan_pattern_label="Pattern1",
        default_block_and_tray_factor=0.95,
        default_tray_factor=0.98,
        default_mlc_factor=0.99,
        initial_dose_rate_for_table=300.0,
        default_dose_rate=600.0,
        fluence_mode=1,
        fluence_mode_id="MODE1",
        high_dose_technique=0
    )

    # Verify all fields are set correctly
    assert energy.value == 6.0
    assert energy.name == "6E"
    assert energy.type == "electron"
    assert energy.scan_pattern_label == "Pattern1"
    assert energy.default_block_and_tray_factor == 0.95
    assert energy.default_tray_factor == 0.98
    assert energy.default_mlc_factor == 0.99
    assert energy.initial_dose_rate_for_table == 300.0
    assert energy.default_dose_rate == 600.0
    assert energy.fluence_mode == 1
    assert energy.fluence_mode_id == "MODE1"
    assert energy.high_dose_technique == 0


def test_machine_energy_relationships():
    """Test PhotonEnergy and ElectronEnergy relationships with Machine and OutputFactor."""
    # Create a Machine
    machine = Machine(name="Test Machine")

    # Create a PhotonEnergy with relationship to machine
    photon_energy = PhotonEnergy(
        name="6X",
        value=6.0,
        machine=machine
    )

    # Create an ElectronEnergy with relationship to machine
    electron_energy = ElectronEnergy(
        name="6E",
        value=6.0,
        machine=machine
    )    # Create PhysicsData and OutputFactors with relationships to energies
    photon_physics = PhysicsData()
    photon_output = OutputFactor(
        dose_per_mu_at_calibration=1.0,
        physics_data=photon_physics
    )
    photon_energy.physics_data = photon_physics

    electron_physics = PhysicsData()
    electron_output = OutputFactor(
        dose_per_mu_at_calibration=1.0,
        physics_data=electron_physics
    )
    electron_energy.physics_data = electron_physics

    # Verify machine relationships
    assert photon_energy.machine is machine
    assert electron_energy.machine is machine
    assert photon_energy in machine.photon_energy_list
    assert electron_energy in machine.electron_energy_list

    # Verify physics data and output factor relationships
    assert photon_energy.physics_data is photon_physics
    assert electron_energy.physics_data is electron_physics
    assert photon_output.physics_data is photon_physics
    assert electron_output.physics_data is electron_physics
    assert photon_physics.machine_energy is photon_energy
    assert electron_physics.machine_energy is electron_energy


def test_polymorphic_type_setting():
    """Test that type discriminator is automatically set for each energy class."""
    photon = PhotonEnergy(name="6X", value=6.0)
    electron = ElectronEnergy(name="6E", value=6.0)

    assert photon.type == "photon"
    assert electron.type == "electron"


def test_polymorphic_query_all(db_session: Session, test_machine: Machine):
    """Test querying all energies returns both photon and electron types."""
    energies = db_session.query(MachineEnergy).all()
    
    assert len(energies) == 4
    photons = [e for e in energies if isinstance(e, PhotonEnergy)]
    electrons = [e for e in energies if isinstance(e, ElectronEnergy)]
    
    assert len(photons) == 2
    assert len(electrons) == 2
    
    # Verify correct instantiation of subclasses
    for photon in photons:
        assert isinstance(photon, PhotonEnergy)
        assert photon.type == "photon"
    
    for electron in electrons:
        assert isinstance(electron, ElectronEnergy)
        assert electron.type == "electron"


def test_polymorphic_query_specific(db_session: Session, test_machine: Machine):
    """Test querying specific energy types."""
    # Query only photon energies
    photons = db_session.query(PhotonEnergy).all()
    assert len(photons) == 2
    assert all(isinstance(e, PhotonEnergy) for e in photons)
    assert all(e.type == "photon" for e in photons)
    
    # Query only electron energies
    electrons = db_session.query(ElectronEnergy).all()
    assert len(electrons) == 2
    assert all(isinstance(e, ElectronEnergy) for e in electrons)
    assert all(e.type == "electron" for e in electrons)


def test_polymorphic_relationships(db_session: Session, test_machine: Machine):
    """Test that relationships handle polymorphic types correctly."""
    # Test Machine relationships
    assert len(test_machine.photon_energy_list) == 2
    assert len(test_machine.electron_energy_list) == 2
    assert all(isinstance(e, PhotonEnergy) for e in test_machine.photon_energy_list)
    assert all(isinstance(e, ElectronEnergy) for e in test_machine.electron_energy_list)

    # Add physics data and output factors and test relationships
    for energy in test_machine.photon_energy_list:
        physics_data = PhysicsData()
        output = OutputFactor(
            dose_per_mu_at_calibration=1.0,
            physics_data=physics_data
        )
        energy.physics_data = physics_data
        db_session.add(physics_data)
        db_session.add(output)
    
    db_session.commit()
    
    # Test that physics data and output factors maintain correct relationship to specific energy types
    photon_physics = db_session.query(PhysicsData).join(PhotonEnergy).all()
    assert len(photon_physics) == 2
    assert all(isinstance(pd.machine_energy, PhotonEnergy) for pd in photon_physics)
    assert all(pd.output_factor is not None for pd in photon_physics)


def test_polymorphic_query_filtering(db_session: Session, test_machine: Machine):
    """Test filtering queries with polymorphic classes."""
    # Filter PhotonEnergy by value
    high_energy_photons = (
        db_session.query(PhotonEnergy)
        .filter(PhotonEnergy.value > 6.0)
        .all()
    )
    assert len(high_energy_photons) == 1
    assert high_energy_photons[0].name == "10X"
    
    # Filter ElectronEnergy by name
    specific_electron = (
        db_session.query(ElectronEnergy)
        .filter(ElectronEnergy.name == "9E")
        .first()
    )
    assert specific_electron is not None
    assert specific_electron.value == 9.0


def test_polymorphic_inheritance_constraints(db_session: Session):
    """Test constraints and behaviors related to the polymorphic inheritance setup."""
    # Test that we can't query or filter by the base polymorphic_identity
    base_energies = (
        db_session.query(MachineEnergy)
        .filter(MachineEnergy.type == "machine_energy")
        .all()
    )
    assert len(base_energies) == 0

    # Test that both concrete types can be created and queried
    photon = PhotonEnergy(name="6X", value=6.0)
    electron = ElectronEnergy(name="6E", value=6.0)
    
    db_session.add(photon)
    db_session.add(electron)
    db_session.commit()

    # Verify type discriminator is set correctly
    assert photon.type == "photon"
    assert electron.type == "electron"

    # Test that we can query base class and get properly typed instances
    all_energies = db_session.query(MachineEnergy).order_by(MachineEnergy.value).all()
    assert len(all_energies) == 2
    assert isinstance(all_energies[0], (PhotonEnergy, ElectronEnergy))
    assert isinstance(all_energies[1], (PhotonEnergy, ElectronEnergy))

    # Test that type-specific relationships work correctly
    machine = Machine(name="Test Machine")
    photon.machine = machine
    electron.machine = machine
    db_session.add(machine)
    db_session.commit()

    # Verify energies appear in correct relationship collections
    assert photon in machine.photon_energy_list
    assert photon not in machine.electron_energy_list
    assert electron in machine.electron_energy_list
    assert electron not in machine.photon_energy_list

    # Test querying by type discriminator
    photons = db_session.query(MachineEnergy).filter(MachineEnergy.type == "photon").all()
    electrons = db_session.query(MachineEnergy).filter(MachineEnergy.type == "electron").all()
    
    assert len(photons) == 1 and isinstance(photons[0], PhotonEnergy)
    assert len(electrons) == 1 and isinstance(electrons[0], ElectronEnergy)


def test_physics_data_relationships(db_session: Session):
    """Test relationships between MachineEnergy, PhysicsData, and OutputFactor."""
    # Create a test machine and energy
    machine = Machine(name="Test Machine")
    energy = PhotonEnergy(name="6X", value=6.0, machine=machine)

    # Create PhysicsData and OutputFactor
    physics_data = PhysicsData()
    output_factor = OutputFactor(
        dose_per_mu_at_calibration=1.0,
        reference_depth=10.0,
        source_to_calibration_point_distance=100.0,
        physics_data=physics_data
    )
    energy.physics_data = physics_data

    db_session.add(machine)
    db_session.add(energy)
    db_session.add(physics_data)
    db_session.add(output_factor)
    db_session.commit()

    # Test bidirectional relationships
    assert energy.physics_data is physics_data
    assert physics_data.machine_energy is energy
    assert physics_data.output_factor is output_factor
    assert output_factor.physics_data is physics_data

    # Test cascading deletes
    db_session.delete(energy)
    db_session.commit()

    # Verify that PhysicsData and OutputFactor were also deleted
    assert db_session.query(PhysicsData).first() is None
    assert db_session.query(OutputFactor).first() is None


def test_physics_data_validation(db_session: Session):
    """Test validation and constraints for PhysicsData relationships."""
    energy = PhotonEnergy(name="6X", value=6.0)
    physics_data = PhysicsData()
    output_factor = OutputFactor(dose_per_mu_at_calibration=1.0)

    # Test setting up the relationships
    energy.physics_data = physics_data
    physics_data.output_factor = output_factor
    db_session.add(energy)
    db_session.commit()

    # Test uniqueness of relationships
    new_physics_data = PhysicsData()
    energy.physics_data = new_physics_data  # This should replace the old physics_data
    db_session.commit()

    # Verify old physics_data was replaced
    assert energy.physics_data is new_physics_data
    assert db_session.query(PhysicsData).count() == 1

    # Test cascade behavior
    db_session.delete(energy)
    db_session.commit()

    # Verify related objects are deleted
    assert db_session.query(PhysicsData).count() == 0
    assert db_session.query(OutputFactor).count() == 0
