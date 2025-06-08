import pytest
import numpy as np
from pinnacle_io.models.mlc import MLCLeafPositions, MLCLeafPair, MultiLeaf
from pinnacle_io.models.control_point import ControlPoint
from pinnacle_io.models.machine import Machine

@pytest.fixture
def mlc_leaf_positions():
    arr = np.ones((60, 2), dtype=np.float32)
    return MLCLeafPositions(points=arr, number_of_dimensions=2, number_of_points=60)

@pytest.fixture
def multi_leaf():
    return MultiLeaf(machine_id=1, left_bank_name="L", right_bank_name="R")

@pytest.fixture
def mlc_leaf_pair(multi_leaf):
    return MLCLeafPair(
        y_center_position=1.0,
        negate_leaf_coordinate=0,
        width=0.5,
        min_tip_position=-2.0,
        max_tip_position=2.0,
        side_leakage_width=0.1,
        tip_leakage_width=0.1,
        multi_leaf=multi_leaf
    )

def test_mlc_leaf_positions_init_and_repr(mlc_leaf_positions):
    assert mlc_leaf_positions.number_of_dimensions == 2
    assert mlc_leaf_positions.number_of_points == 60
    assert mlc_leaf_positions.points.shape == (60, 2)
    r = repr(mlc_leaf_positions)
    assert "MLCLeafPositions" in r
    assert "points=60" in r

def test_mlc_leaf_positions_points_setter_getter():
    arr = np.ones((60, 2), dtype=np.float32)
    mlc = MLCLeafPositions(points=arr)
    # Should be able to get the same array back (within float tolerance)
    np.testing.assert_allclose(mlc.points, arr)
    # Test None
    mlc.points = None
    assert mlc.points is None
    assert mlc._points_data is None
    assert mlc.number_of_dimensions == 0
    assert mlc.number_of_points == 0

def test_mlc_leaf_positions_points_invalid_shape():
    arr = np.ones((10, 2), dtype=np.float32)
    with pytest.raises(ValueError):
        MLCLeafPositions(points=arr)
    arr2 = np.ones((60, 3), dtype=np.float32)
    with pytest.raises(ValueError):
        MLCLeafPositions(points=arr2)

def test_mlc_leaf_positions_points_invalid_type():
    with pytest.raises(TypeError):
        MLCLeafPositions(points="not an array")

def test_mlc_leaf_positions_deserialize_edge_case():
    # Simulate deserialization with wrong number_of_dimensions
    arr = np.ones((60, 2), dtype=np.float32)
    mlc = MLCLeafPositions(points=arr)
    mlc._points = None
    mlc.number_of_dimensions = 3  # Should warn and force to 2
    _ = mlc.points  # Should not raise

def test_mlc_leaf_pair_init_and_repr(mlc_leaf_pair):
    assert mlc_leaf_pair.width == 0.5
    assert mlc_leaf_pair.multi_leaf is not None
    r = repr(mlc_leaf_pair)
    assert "MLCLeafPair" in r
    assert "width=0.5" in r

def test_multileaf_init_and_repr(multi_leaf):
    assert multi_leaf.left_bank_name == "L"
    assert multi_leaf.right_bank_name == "R"
    r = repr(multi_leaf)
    assert "MultiLeaf" in r
    assert "machine_id=1" in r

def test_multileaf_relationships():
    machine = Machine(id=1, name="TestMachine")
    multi_leaf = MultiLeaf(machine=machine)
    machine.multi_leaf = multi_leaf
    assert multi_leaf.machine is machine
    assert machine.multi_leaf is multi_leaf
    # Test leaf_pair_list relationship
    leaf_pair = MLCLeafPair(multi_leaf=multi_leaf)
    multi_leaf.leaf_pair_list.append(leaf_pair)
    assert leaf_pair.multi_leaf is multi_leaf
    assert leaf_pair in multi_leaf.leaf_pair_list

def test_mlcleafpositions_control_point_relationship():
    cp = ControlPoint(id=1)
    mlc = MLCLeafPositions(control_point=cp)
    cp._mlc_leaf_positions = mlc
    assert mlc.control_point is cp
    assert cp._mlc_leaf_positions is mlc
