"""
Tests for the ConfigRV and TolTable models.
"""

from pinnacle_io.models.machine_config import ConfigRV, TolTable
from pinnacle_io.models.machine import Machine

def test_configrv_repr():
    """Test the __repr__ method of the ConfigRV class."""
    config = ConfigRV(
        id=10,
        machine_id=2,
        enabled=1,
        left_jaw="X1",
        right_jaw="X2",
        top_jaw="Y2",
        bottom_jaw="Y1"
    )
    expected = "<ConfigRV(id=10, machine_id=2, enabled=1, left_jaw='X1', right_jaw='X2', top_jaw='Y2', bottom_jaw='Y1')>"
    assert repr(config) == expected


def test_configrv_initialization():
    """Test creating a ConfigRV with all fields."""
    config = ConfigRV(
        enabled=1,
        left_jaw="X1",
        right_jaw="X2",
        top_jaw="Y2",
        bottom_jaw="Y1",
        mlc_bank_swap="A",
        mlc_order_swap="B",
        elekta_relative_mlc_positions=0,
        machine_id=5
    )
    assert config.enabled == 1
    assert config.left_jaw == "X1"
    assert config.right_jaw == "X2"
    assert config.top_jaw == "Y2"
    assert config.bottom_jaw == "Y1"
    assert config.mlc_bank_swap == "A"
    assert config.mlc_order_swap == "B"
    assert config.elekta_relative_mlc_positions == 0
    assert config.machine_id == 5


def test_configrv_machine_relationship():
    """Test ConfigRV relationship with Machine."""
    machine = Machine()
    config = ConfigRV(machine=machine)
    machine.config_rv = config
    assert config.machine is machine
    assert machine.config_rv is config


def test_toltable_repr():
    """Test the __repr__ method of the TolTable class."""
    tol = TolTable(id=3, name="TOL1", number=99)
    expected = "<TolTable(id=3, name='TOL1', number=99)>"
    assert repr(tol) == expected


def test_toltable_initialization():
    """Test creating a TolTable with all fields."""
    tol = TolTable(name="TOL2", number=5, machine_id=8)
    assert tol.name == "TOL2"
    assert tol.number == 5
    assert tol.machine_id == 8


def test_toltable_machine_relationship():
    """Test TolTable relationship with Machine."""
    machine = Machine()
    tol = TolTable(machine=machine)
    assert tol.machine is machine
    assert tol in machine.tolerance_table_list
