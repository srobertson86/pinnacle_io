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


def test_mlc_sqlalchemy_standards_compliance():
    """Test that MLC models follow SQLAlchemy standards and best practices."""
    # Test relationship naming follows _list convention
    multi_leaf = MultiLeaf(left_bank_name="Test")

    # Verify list relationships follow _list convention
    assert hasattr(multi_leaf, 'leaf_pair_list')

    # Verify single relationships don't have _list suffix
    assert hasattr(multi_leaf, 'machine')

    # Test that relationships are properly typed by checking annotations
    # Check MultiLeaf type annotations
    multi_leaf_annotations = MultiLeaf.__annotations__
    assert 'leaf_pair_list' in multi_leaf_annotations
    assert 'List' in str(multi_leaf_annotations.get('leaf_pair_list', ''))
    assert 'Optional' in str(multi_leaf_annotations.get('left_bank_name', ''))
    assert 'Optional' in str(multi_leaf_annotations.get('vendor', ''))

    # Check MLCLeafPair type annotations
    leaf_pair_annotations = MLCLeafPair.__annotations__
    assert 'Optional' in str(leaf_pair_annotations.get('width', ''))
    assert 'Optional' in str(leaf_pair_annotations.get('y_center_position', ''))

    # Check MLCLeafPositions type annotations
    positions_annotations = MLCLeafPositions.__annotations__
    assert 'Optional' in str(positions_annotations.get('number_of_dimensions', ''))
    assert 'Optional' in str(positions_annotations.get('control_point', ''))

    # Test inheritance from correct base class
    from pinnacle_io.models.pinnacle_base import PinnacleBase
    assert issubclass(MultiLeaf, PinnacleBase)
    assert issubclass(MLCLeafPair, PinnacleBase)
    assert issubclass(MLCLeafPositions, PinnacleBase)


def test_mlc_documentation_completeness():
    """Test that MLC models have comprehensive documentation."""
    # Test MultiLeaf class docstring
    multi_leaf_doc = MultiLeaf.__doc__
    assert multi_leaf_doc is not None
    assert len(multi_leaf_doc) > 1000  # Should be detailed like Beam class
    assert "Attributes:" in multi_leaf_doc
    assert "Relationships:" in multi_leaf_doc
    assert "Example:" in multi_leaf_doc

    # Test MLCLeafPair class docstring
    leaf_pair_doc = MLCLeafPair.__doc__
    assert leaf_pair_doc is not None
    assert len(leaf_pair_doc) > 500  # Should be detailed
    assert "Attributes:" in leaf_pair_doc
    assert "Relationships:" in leaf_pair_doc
    assert "Example:" in leaf_pair_doc

    # Test MLCLeafPositions class docstring
    positions_doc = MLCLeafPositions.__doc__
    assert positions_doc is not None
    assert len(positions_doc) > 800  # Should be detailed
    assert "Attributes:" in positions_doc
    assert "Relationships:" in positions_doc
    assert "Example:" in positions_doc

    # Test __init__ method documentation
    multi_leaf_init_doc = MultiLeaf.__init__.__doc__
    assert multi_leaf_init_doc is not None
    assert "Args:" in multi_leaf_init_doc
    assert "Relationship Parameters:" in multi_leaf_init_doc
    assert "Example:" in multi_leaf_init_doc


def test_mlc_cascade_behaviors():
    """Test that MLC relationships have appropriate cascade behaviors."""
    # Create a MultiLeaf with leaf pairs
    multi_leaf = MultiLeaf(
        left_bank_name="B",
        right_bank_name="A",
        leaf_pair_list=[
            {"y_center_position": -19.5, "width": 1.0},
            {"y_center_position": -18.5, "width": 1.0}
        ]
    )

    # Verify relationships are created
    assert len(multi_leaf.leaf_pair_list) == 2

    # Verify the child objects have proper parent references
    assert multi_leaf.leaf_pair_list[0].multi_leaf is multi_leaf
    assert multi_leaf.leaf_pair_list[1].multi_leaf is multi_leaf


def test_mlc_lazy_loading_configuration():
    """Test that MLC relationships have optimal lazy loading strategies."""
    # Create instances to check relationship configurations
    multi_leaf = MultiLeaf(left_bank_name="Test")
    leaf_pair = MLCLeafPair(width=1.0)
    positions = MLCLeafPositions(number_of_dimensions=2)

    # Check that relationships exist and are properly configured
    # (The actual lazy loading behavior would be tested in integration tests)
    assert hasattr(multi_leaf, 'machine')
    assert hasattr(multi_leaf, 'leaf_pair_list')
    assert hasattr(leaf_pair, 'multi_leaf')
    assert hasattr(positions, 'control_point')
