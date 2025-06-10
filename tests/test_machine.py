"""
Tests for the Machine model, reader, and writer.
"""

from pathlib import Path
import pytest

from pinnacle_io.models import (
    Machine,
    CouchAngle,
    GantryAngle,
    CollimatorAngle,
    ConfigRV,
    MultiLeaf,
    MLCLeafPair,
    ElectronApplicator,
    TolTable,
    MachineEnergy,
    PhotonEnergy,
    ElectronEnergy,
    OutputFactor,
    PhysicsData,
)
from pinnacle_io.readers.machine_reader import MachineReader
from pinnacle_io.writers.machine_writer import MachineWriter


def test_machine_energy_initialization():
    """Test creating a MachineEnergy directly with kwargs."""
    energy = MachineEnergy(
        modality="photon",
        value=6.0,
        id=0,
        name="6X",
        scan_pattern_label="",
        default_block_and_tray_factor=1.0,
        default_tray_factor=1.0,
        default_mlc_factor=1.0,
        initial_dose_rate_for_table=600.0,
        default_dose_rate=600.0,
        fluence_mode=0,
        fluence_mode_id="",
        high_dose_technique=0,
        non_existent_field="This should be ignored",
    )

    assert energy.value == 6.0
    assert energy.id == 0
    assert energy.name == "6X"
    assert energy.scan_pattern_label == ""
    assert energy.default_dose_rate == 600.0
    assert not hasattr(energy, "non_existent_field")


def test_output_factor_initialization():
    """Test creating an OutputFactor directly with kwargs."""
    output_factor = OutputFactor(
        reference_depth=10.0,
        source_to_calibration_point_distance=100.0,
        electron_ssd_tolerance=0.1,
        dose_per_mu_at_calibration=0.8074,
        min_mlc_position_at_calibration=0.0,
        calculated_calibration_dose=1.0,
        computation_version="Pinnacle v16.0",
        calculated_calibration_dose_valid=1,
        non_existent_field="This should be ignored",
    )

    assert output_factor.reference_depth == 10.0
    assert output_factor.source_to_calibration_point_distance == 100.0
    assert output_factor.dose_per_mu_at_calibration == 0.8074
    assert output_factor.calculated_calibration_dose_valid == 1
    assert not hasattr(output_factor, "non_existent_field")


def test_machine_initialization():
    """Test creating a Machine directly with kwargs."""
    # Test with minimal data. Include one input not in the model to ensure it is ignored.
    machine = Machine(
        name="Test Machine",
        machine_type="Varian Clinac-2100",
        version_timestamp="2023-01-01 12:00:00",
        version_description="Test machine",
        commissioned_by="Test User",
        commission_version="Pinnacle v16.0",
        login_name="testuser",
        institution="Test Institution",
        commissioned_for_photons=1,
        commissioned_for_electrons=1,
        commissioned_for_mc_electrons=0,
        commissioned_for_stereo=0,
        commissioned_for_protons=0,
        read_write_machine=1,
        is_simulator=0,
        has_fixed_jaw=0,
        sad=100.0,
        non_existent_field="This should be ignored",
        couch_angle={
            "name": "",
            "twelve_o_clock_angle": 0.0,
            "minimum_angle": 265.0,
            "maximum_angle": 95.0,
        },
        gantry_angle={
            "name": "",
            "twelve_o_clock_angle": 0.0,
            "minimum_angle": 180.0,
            "maximum_angle": 179.9,
        },
        collimator_angle={
            "name": "",
            "twelve_o_clock_angle": 180.0,
            "minimum_angle": 195.0,
            "maximum_angle": 165.0,
        },
        config_rv={
            "enabled": 1,
            "left_jaw": "X1",
            "right_jaw": "X2",
            "top_jaw": "Y1",
            "bottom_jaw": "Y2",
        },
        multi_leaf={
            "left_bank_name": "B",
            "right_bank_name": "A",
            "leaf_x_base_position": 60.0,
            "leaf_pair_list": [
                {
                    "mlc_leaf_pair": {
                        "y_center_position": -19.5,
                        "width": 1.0,
                        "min_tip_position": -20.0,
                        "max_tip_position": 20.0,
                    }
                }
            ],
        },
        electron_applicator_list=[
            {
                "name": "10x10",
                "width": 10.0,
                "length": 10.0,
                "manufacturer_code": "10X10",
            }
        ],
        tolerance_table_list=[
            {
                "name": "1 Default",
                "number": 1,
            }
        ],
        photon_energy_list=[
            {
                "value": 6.0,
                "id": 0,
                "name": "6X",
                "physics_data": {
                    "output_factor": {
                        "reference_depth": 10.0,
                        "dose_per_mu_at_calibration": 0.8074,
                    }
                },
            }
        ],
        electron_energy_list=[
            {
                "value": 6.0,
                "id": 0,
                "name": "6E",
                "physics_data": {
                    "output_factor": {
                        "reference_depth": 1.4,
                        "dose_per_mu_at_calibration": 1.001,
                    }
                },
            }
        ],
    )

    # Test basic attributes
    assert machine.name == "Test Machine"
    assert machine.machine_type == "Varian Clinac-2100"
    assert machine.commissioned_for_photons == 1
    assert machine.sad == 100.0
    assert not hasattr(machine, "non_existent_field")

    # Test relationships
    assert isinstance(machine.couch_angle, CouchAngle)
    assert machine.couch_angle.minimum_angle == 265.0
    assert machine.couch_angle.maximum_angle == 95.0

    assert isinstance(machine.gantry_angle, GantryAngle)
    assert machine.gantry_angle.minimum_angle == 180.0
    assert machine.gantry_angle.maximum_angle == 179.9

    assert isinstance(machine.collimator_angle, CollimatorAngle)
    assert machine.collimator_angle.minimum_angle == 195.0
    assert machine.collimator_angle.maximum_angle == 165.0

    assert isinstance(machine.config_rv, ConfigRV)
    assert machine.config_rv.left_jaw == "X1"
    assert machine.config_rv.right_jaw == "X2"

    assert isinstance(machine.multi_leaf, MultiLeaf)
    assert machine.multi_leaf.left_bank_name == "B"
    assert machine.multi_leaf.leaf_x_base_position == 60.0

    assert len(machine.electron_applicator_list) == 1
    assert isinstance(machine.electron_applicator_list[0], ElectronApplicator)
    assert machine.electron_applicator_list[0].name == "10x10"

    assert len(machine.tolerance_table_list) == 1
    assert isinstance(machine.tolerance_table_list[0], TolTable)
    assert machine.tolerance_table_list[0].name == "1 Default"

    assert len(machine.photon_energy_list) == 1
    assert isinstance(machine.photon_energy_list[0], PhotonEnergy)
    assert machine.photon_energy_list[0].name == "6X"
    assert isinstance(machine.photon_energy_list[0].physics_data, PhysicsData)
    assert isinstance(machine.photon_energy_list[0].physics_data.output_factor, OutputFactor)
    assert machine.photon_energy_list[0].physics_data.output_factor.dose_per_mu_at_calibration == 0.8074

    assert len(machine.electron_energy_list) == 1
    assert isinstance(machine.electron_energy_list[0], ElectronEnergy)
    assert machine.electron_energy_list[0].name == "6E"
    assert isinstance(machine.electron_energy_list[0].physics_data, PhysicsData)
    assert isinstance(machine.electron_energy_list[0].physics_data.output_factor, OutputFactor)
    assert machine.electron_energy_list[0].physics_data.output_factor.dose_per_mu_at_calibration == 1.001


def test_read_machine_file():
    """Tests reading a valid Machine file."""
    machine_list = MachineReader.read(
        Path(__file__).parent / "test_data/01/Institution_1/Mount_0/Patient_1/Plan_0"
    )

    assert isinstance(machine_list, list)
    assert len(machine_list) == 1
    machine = machine_list[0]
    assert isinstance(machine, Machine)
    assert machine.name == "Clinac iX"
    assert machine.machine_type == "Varian Clinac-2100"
    assert machine.commissioned_for_photons == 1
    assert machine.commissioned_for_electrons == 1
    assert machine.sad == 100.0

    # Test angle configurations
    assert machine.couch_angle.minimum_angle == 265.0
    assert machine.couch_angle.maximum_angle == 95.0
    assert machine.gantry_angle.minimum_angle == 180.0
    assert machine.gantry_angle.maximum_angle == 179.9
    assert machine.collimator_angle.minimum_angle == 195.0
    assert machine.collimator_angle.maximum_angle == 165.0

    # Test ConfigRV
    assert machine.config_rv.enabled == 1
    assert machine.config_rv.left_jaw == "X1"
    assert machine.config_rv.right_jaw == "X2"

    # Test MultiLeaf
    assert machine.multi_leaf is not None
    assert machine.multi_leaf.left_bank_name == "B"
    assert machine.multi_leaf.right_bank_name == "A"

    # Test LeafPairList and MLCLeafPairs
    assert machine.multi_leaf.leaf_pair_list is not None
    assert len(machine.multi_leaf.leaf_pair_list) > 0
    assert isinstance(machine.multi_leaf.leaf_pair_list[0], MLCLeafPair)

    # Test Electron Applicators
    assert len(machine.electron_applicator_list) > 0
    assert isinstance(machine.electron_applicator_list[0], ElectronApplicator)

    # Test Tolerance Tables
    assert len(machine.tolerance_table_list) > 0
    assert isinstance(machine.tolerance_table_list[0], TolTable)

    # Test Photon Energies
    assert len(machine.photon_energy_list) > 0
    energy = machine.photon_energy_list[0]
    assert isinstance(energy, MachineEnergy)
    assert energy.physics_data is not None
    assert isinstance(energy.physics_data, PhysicsData)
    assert energy.physics_data.output_factor is not None
    assert isinstance(energy.physics_data.output_factor, OutputFactor)


def test_machine_writer_not_implemented():
    """Test that the MachineWriter raises NotImplementedError."""
    machine = Machine(name="Test Machine")
    with pytest.raises(NotImplementedError):
        MachineWriter.write(machine, "/tmp/test_machine")


def test_machine_optional_fields():
    """Test Machine initialization with None/empty optional fields."""
    machine = Machine(
        name="Test Optional Fields",
        machine_type=None,  # Optional field as None
        version_timestamp="",  # Optional field as empty string
        commissioned_for_photons=1
    )
    
    assert machine.name == "Test Optional Fields"
    assert machine.machine_type is None
    assert machine.version_timestamp == ""
    assert machine.commissioned_for_photons == 1


def test_machine_relationships_empty():
    """Test Machine behavior with missing relationship objects."""
    machine = Machine(
        name="No Relationships",
        machine_type="Test"
    )
    
    # Test that lists are empty but not None
    assert machine.electron_applicator_list == []
    assert machine.tolerance_table_list == []
    assert machine.photon_energy_list == []
    assert machine.electron_energy_list == []
    
    # Test that one-to-one relationships are None
    assert machine.couch_angle is None
    assert machine.gantry_angle is None
    assert machine.collimator_angle is None
    assert machine.config_rv is None
    assert machine.multi_leaf is None


def test_electron_applicator_initialization():
    """Test creating an ElectronApplicator directly with all fields."""
    applicator = ElectronApplicator(
        name="15x15",
        width=15.0,
        length=15.0,
        manufacturer_code="15X15",
        source_to_cutout_distance=95.0,
        cutout_thickness=1.5,
        cutout_material="Cerrobend",
        cutout_mass_density=9.4,
        cutout_is_divergent=1,
        cutout_is_rectangular=1,
        cutout_half_x_outside=7.5,
        cutout_half_y_outside=7.5,
        non_existent_field="This should be ignored"
    )

    # Test basic attributes
    assert applicator.name == "15x15"
    assert applicator.width == 15.0
    assert applicator.length == 15.0
    assert applicator.manufacturer_code == "15X15"
    
    # Test cutout-specific attributes
    assert applicator.source_to_cutout_distance == 95.0
    assert applicator.cutout_thickness == 1.5
    assert applicator.cutout_material == "Cerrobend"
    assert applicator.cutout_mass_density == 9.4
    assert applicator.cutout_is_divergent == 1
    assert applicator.cutout_is_rectangular == 1
    assert applicator.cutout_half_x_outside == 7.5
    assert applicator.cutout_half_y_outside == 7.5
    
    # Test that non-existent fields are not added
    assert not hasattr(applicator, "non_existent_field")


def test_read_electron_applicator_data():
    """Tests reading ElectronApplicator data from a Machine file."""
    machine_list = MachineReader.read(
        Path(__file__).parent / "test_data/01/Institution_1/Mount_0/Patient_1/Plan_0"
    )

    machine = machine_list[0]
    assert len(machine.electron_applicator_list) > 0

    # Get the first applicator for detailed testing
    applicator = machine.electron_applicator_list[0]
    assert isinstance(applicator, ElectronApplicator)
    assert applicator.name is not None
    assert isinstance(applicator.width, (float, type(None)))
    assert isinstance(applicator.length, (float, type(None)))
    assert isinstance(applicator.manufacturer_code, (str, type(None)))

    # Test cutout properties if they exist
    if applicator.cutout_material is not None:
        assert isinstance(applicator.cutout_material, str)
    if applicator.cutout_mass_density is not None:
        assert isinstance(applicator.cutout_mass_density, float)
    if applicator.cutout_is_divergent is not None:
        assert isinstance(applicator.cutout_is_divergent, int)
    if applicator.cutout_is_rectangular is not None:
        assert isinstance(applicator.cutout_is_rectangular, int)


def test_machine_sqlalchemy_standards_compliance():
    """Test that Machine model follows SQLAlchemy standards and best practices."""
    # Test relationship naming follows _list convention
    machine = Machine(name="Standards Test Machine")

    # Verify list relationships follow _list convention
    assert hasattr(machine, 'electron_applicator_list')
    assert hasattr(machine, 'tolerance_table_list')
    assert hasattr(machine, 'photon_energy_list')
    assert hasattr(machine, 'electron_energy_list')

    # Verify single relationships don't have _list suffix
    assert hasattr(machine, 'couch_angle')
    assert hasattr(machine, 'gantry_angle')
    assert hasattr(machine, 'collimator_angle')
    assert hasattr(machine, 'config_rv')
    assert hasattr(machine, 'multi_leaf')

    # Test that relationships are properly typed
    from typing import get_type_hints
    hints = get_type_hints(Machine)

    # Check that list relationships are typed as List[...]
    assert 'List' in str(hints.get('electron_applicator_list', ''))
    assert 'List' in str(hints.get('tolerance_table_list', ''))
    assert 'List' in str(hints.get('photon_energy_list', ''))
    assert 'List' in str(hints.get('electron_energy_list', ''))

    # Test that optional fields are properly typed
    assert 'Optional' in str(hints.get('machine_type', ''))
    assert 'Optional' in str(hints.get('version_timestamp', ''))

    # Test inheritance from correct base class
    from pinnacle_io.models.versioned_base import VersionedBase
    assert issubclass(Machine, VersionedBase)

    # Test that ElectronApplicator inherits from correct base class
    from pinnacle_io.models.pinnacle_base import PinnacleBase
    assert issubclass(ElectronApplicator, PinnacleBase)


def test_machine_documentation_completeness():
    """Test that Machine and ElectronApplicator have comprehensive documentation."""
    # Test Machine class docstring
    machine_doc = Machine.__doc__
    assert machine_doc is not None
    assert len(machine_doc) > 500  # Should be detailed like Beam class
    assert "Attributes:" in machine_doc
    assert "Relationships:" in machine_doc
    assert "Example:" in machine_doc

    # Test ElectronApplicator class docstring
    applicator_doc = ElectronApplicator.__doc__
    assert applicator_doc is not None
    assert len(applicator_doc) > 300  # Should be detailed
    assert "Attributes:" in applicator_doc
    assert "Relationships:" in applicator_doc
    assert "Example:" in applicator_doc

    # Test __init__ method documentation
    machine_init_doc = Machine.__init__.__doc__
    assert machine_init_doc is not None
    assert "Args:" in machine_init_doc
    assert "Relationship Parameters:" in machine_init_doc
    assert "Example:" in machine_init_doc


def test_machine_cascade_behaviors():
    """Test that Machine relationships have appropriate cascade behaviors."""
    # Create a machine with relationships
    machine = Machine(
        name="Cascade Test Machine",
        electron_applicator_list=[
            {"name": "Test Applicator", "width": 10.0, "length": 10.0}
        ],
        tolerance_table_list=[
            {"name": "Test Table", "number": 1}
        ]
    )

    # Verify relationships are created
    assert len(machine.electron_applicator_list) == 1
    assert len(machine.tolerance_table_list) == 1

    # Verify the child objects have proper parent references
    assert machine.electron_applicator_list[0].machine is machine
    assert machine.tolerance_table_list[0].machine is machine
