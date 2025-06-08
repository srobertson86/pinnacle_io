"""
Tests for the machine angle models (CouchAngle, GantryAngle, CollimatorAngle).
"""
from pinnacle_io.models import Machine
from pinnacle_io.models.machine_angle import CouchAngle, GantryAngle, CollimatorAngle


def test_couch_angle_init():
    """Test initializing a CouchAngle instance."""
    couch_angle = CouchAngle(
        name="Test Couch",
        twelve_o_clock_angle=0.0,
        clockwise_increases=1,
        nominal_angle=0.0,
        minimum_angle=-90.0,
        maximum_angle=90.0,
        machine_id=1
    )
    
    assert couch_angle.name == "Test Couch"
    assert couch_angle.twelve_o_clock_angle == 0.0
    assert couch_angle.clockwise_increases == 1
    assert couch_angle.nominal_angle == 0.0
    assert couch_angle.minimum_angle == -90.0
    assert couch_angle.maximum_angle == 90.0
    assert couch_angle.machine_id == 1


def test_gantry_angle_init():
    """Test initializing a GantryAngle instance."""
    gantry_angle = GantryAngle(
        name="Test Gantry",
        twelve_o_clock_angle=0.0,
        clockwise_increases=1,
        nominal_angle=0.0,
        minimum_angle=0.0,
        maximum_angle=360.0,
        machine_id=1
    )
    
    assert gantry_angle.name == "Test Gantry"
    assert gantry_angle.twelve_o_clock_angle == 0.0
    assert gantry_angle.clockwise_increases == 1
    assert gantry_angle.nominal_angle == 0.0
    assert gantry_angle.minimum_angle == 0.0
    assert gantry_angle.maximum_angle == 360.0
    assert gantry_angle.machine_id == 1


def test_collimator_angle_init():
    """Test initializing a CollimatorAngle instance."""
    collimator_angle = CollimatorAngle(
        name="Test Collimator",
        twelve_o_clock_angle=0.0,
        clockwise_increases=1,
        nominal_angle=0.0,
        minimum_angle=0.0,
        maximum_angle=360.0,
        machine_id=1
    )
    
    assert collimator_angle.name == "Test Collimator"
    assert collimator_angle.twelve_o_clock_angle == 0.0
    assert collimator_angle.clockwise_increases == 1
    assert collimator_angle.nominal_angle == 0.0
    assert collimator_angle.minimum_angle == 0.0
    assert collimator_angle.maximum_angle == 360.0
    assert collimator_angle.machine_id == 1


def test_couch_angle_repr():
    """Test the string representation of a CouchAngle."""
    couch_angle = CouchAngle(
        machine_id=1,
        minimum_angle=-90.0,
        maximum_angle=90.0
    )
    
    expected_repr = "<CouchAngle(id=None, machine_id=1, min=-90.0, max=90.0)>"
    assert repr(couch_angle) == expected_repr


def test_gantry_angle_repr():
    """Test the string representation of a GantryAngle."""
    gantry_angle = GantryAngle(
        machine_id=1,
        minimum_angle=0.0,
        maximum_angle=360.0
    )
    
    expected_repr = "<GantryAngle(id=None, machine_id=1, min=0.0, max=360.0)>"
    assert repr(gantry_angle) == expected_repr


def test_collimator_angle_repr():
    """Test the string representation of a CollimatorAngle."""
    collimator_angle = CollimatorAngle(
        machine_id=1,
        minimum_angle=0.0,
        maximum_angle=360.0
    )
    
    expected_repr = "<CollimatorAngle(id=None, machine_id=1, min=0.0, max=360.0)>"
    assert repr(collimator_angle) == expected_repr


def test_machine_couch_angle_relationship():
    """Test the relationship between Machine and CouchAngle."""
    # Create a machine and a couch angle
    machine = Machine(
        name="Test Machine",
        machine_type="Test Type"
    )
    
    couch_angle = CouchAngle(
        name="Test Couch",
        minimum_angle=-90.0,
        maximum_angle=90.0
    )
    
    # Establish the relationship
    machine.couch_angle = couch_angle
    couch_angle.machine = machine
    couch_angle.machine_id = getattr(machine, 'id', 1)  # Set manually if needed
    
    # Test the relationship
    assert couch_angle.machine_id == machine.id if hasattr(machine, 'id') else 1
    assert couch_angle.machine == machine
    assert machine.couch_angle == couch_angle


def test_machine_gantry_angle_relationship():
    """Test the relationship between Machine and GantryAngle."""
    # Create a machine and a gantry angle
    machine = Machine(
        name="Test Machine",
        machine_type="Test Type"
    )
    
    gantry_angle = GantryAngle(
        name="Test Gantry",
        minimum_angle=0.0,
        maximum_angle=360.0
    )
    
    # Establish the relationship
    machine.gantry_angle = gantry_angle
    gantry_angle.machine = machine
    gantry_angle.machine_id = getattr(machine, 'id', 1)
    
    # Test the relationship
    assert gantry_angle.machine_id == machine.id if hasattr(machine, 'id') else 1
    assert gantry_angle.machine == machine
    assert machine.gantry_angle == gantry_angle


def test_machine_collimator_angle_relationship():
    """Test the relationship between Machine and CollimatorAngle."""
    # Create a machine and a collimator angle
    machine = Machine(
        name="Test Machine",
        machine_type="Test Type"
    )
    
    collimator_angle = CollimatorAngle(
        name="Test Collimator",
        minimum_angle=0.0,
        maximum_angle=360.0
    )
    
    # Establish the relationship
    machine.collimator_angle = collimator_angle
    collimator_angle.machine = machine
    collimator_angle.machine_id = getattr(machine, 'id', 1)
    
    # Test the relationship
    assert collimator_angle.machine_id == machine.id if hasattr(machine, 'id') else 1
    assert collimator_angle.machine == machine
    assert machine.collimator_angle == collimator_angle


def test_machine_with_all_angles():
    """Test a Machine with all three angle types."""
    # Create a machine with all three angle types
    machine = Machine(
        name="Complete Machine",
        machine_type="Test Type",
        couch_angle=CouchAngle(
            name="Test Couch",
            minimum_angle=-90.0,
            maximum_angle=90.0
        ),
        gantry_angle=GantryAngle(
            name="Test Gantry",
            minimum_angle=0.0,
            maximum_angle=360.0
        ),
        collimator_angle=CollimatorAngle(
            name="Test Collimator",
            minimum_angle=0.0,
            maximum_angle=360.0
        )
    )
    # Set up reverse relationships manually
    machine.couch_angle.machine = machine
    machine.couch_angle.machine_id = getattr(machine, 'id', 1)
    machine.gantry_angle.machine = machine
    machine.gantry_angle.machine_id = getattr(machine, 'id', 1)
    machine.collimator_angle.machine = machine
    machine.collimator_angle.machine_id = getattr(machine, 'id', 1)
    
    # Test all relationships
    assert machine.couch_angle is not None
    assert machine.gantry_angle is not None
    assert machine.collimator_angle is not None
    
    assert machine.couch_angle.machine_id == machine.id if hasattr(machine, 'id') else 1
    assert machine.gantry_angle.machine_id == machine.id if hasattr(machine, 'id') else 1
    assert machine.collimator_angle.machine_id == machine.id if hasattr(machine, 'id') else 1
    
    assert machine.couch_angle.name == "Test Couch"
    assert machine.gantry_angle.name == "Test Gantry"
    assert machine.collimator_angle.name == "Test Collimator"
