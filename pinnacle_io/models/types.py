"""
Custom SQLAlchemy types and spatial coordinate classes for Pinnacle data models.

This module provides:
1. Custom SQLAlchemy types for database storage
2. A hierarchy of spatial coordinate types for 3D medical imaging data
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar, final
import math

from sqlalchemy import String, Text
from sqlalchemy.types import TypeDecorator


class JsonList(TypeDecorator):
    """
    SQLAlchemy type for storing Python lists as JSON strings in the database.
    
    This type handles automatic conversion between Python lists and JSON strings
    when reading from and writing to the database.
    
    Example:
        class MyModel(Base):
            __tablename__ = 'my_model'
            
            id = Column(Integer, primary_key=True)
            tags = Column(JsonList)  # Will be stored as JSON string
    """

    impl = String(Text().length)

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(Text())

    def process_bind_param(self, value: Optional[List[Any]], dialect) -> Optional[str]:
        """
        Convert Python list to JSON string for database storage.
        
        Args:
            value: The Python list to convert, or None.
            dialect: The DBAPI in use.
            
        Returns:
            JSON string representation of the list, or None if value is None.
        """
        if value is None:
            return None
        return str(value)

    def process_result_value(self, value: Optional[str], dialect) -> Optional[List[Any]]:
        """
        Convert JSON string from database back to Python list.
        
        Args:
            value: The JSON string from the database, or None.
            dialect: The DBAPI in use.
            
        Returns:
            Python list, or None if value is None or empty.
        """
        if not value:
            return None
        try:
            return eval(value) if value else None
        except (ValueError, SyntaxError):
            return None


# Type variables for generic base class
T = TypeVar('T', int, float, covariant=True)


class SpatialBase(ABC, Generic[T]):
    """
    Abstract base class for 3D spatial coordinates.
    
    This class provides common functionality for all spatial coordinate types
    while allowing type-specific implementations for different use cases.
    """
    __slots__ = ('_x', '_y', '_z')
    
    def __init__(self, x: T, y: T, z: T) -> None:
        """Initialize with x, y, z components."""
        self._x = self._validate_component('x', x)
        self._y = self._validate_component('y', y)
        self._z = self._validate_component('z', z)
    
    @abstractmethod
    def _validate_component(self, name: str, value: T) -> T:
        """Validate a component value. Must be implemented by subclasses."""
        pass
    
    @property
    def x(self) -> T:
        """X component of the coordinate."""
        return self._x
    
    @property
    def y(self) -> T:
        """Y component of the coordinate."""
        return self._y
    
    @property
    def z(self) -> T:
        """Z component of the coordinate."""
        return self._z
    
    def to_dict(self) -> Dict[str, T]:
        """Convert to a dictionary with x, y, z keys."""
        return {'x': self.x, 'y': self.y, 'z': self.z}
    
    def to_list(self) -> List[T]:
        """Convert to a list [x, y, z]."""
        return [self.x, self.y, self.z]
    
    @classmethod
    def from_dict(cls, data: Dict[str, T]) -> 'SpatialBase[T]':
        """Create from a dictionary with x, y, z keys."""
        return cls(
            x=data.get('x', 0),  # type: ignore
            y=data.get('y', 0),  # type: ignore
            z=data.get('z', 0)   # type: ignore
        )
    
    def __eq__(self, other: object) -> bool:
        """Test equality with another coordinate."""
        if not isinstance(other, SpatialBase):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __repr__(self) -> str:
        """String representation of the coordinate."""
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})"


@final
class VoxelSize(SpatialBase[float]):
    """
    Represents the physical size of a voxel in millimeters.
    
    All components must be positive floating-point numbers.
    """
    
    def _validate_component(self, name: str, value: float) -> float:
        """Validate that the component is a positive number."""
        if value is None:
            return 0.0  # Default to 0 if value is None
        val = float(value)
        if val < 0:
            raise ValueError(f"{name} must be non-negative, got {val}")
        return val
    
    def volume(self) -> float:
        """Calculate the volume of a voxel with these dimensions."""
        return self.x * self.y * self.z


@final
class VolumeSize(SpatialBase[float]):
    """
    Represents the physical dimensions of a volume in millimeters.
    
    All components must be non-negative floating-point numbers.
    """
    
    def _validate_component(self, name: str, value: float) -> float:
        """Validate that the component is a non-negative number."""
        val = float(value)
        if val < 0:
            raise ValueError(f"{name} must be non-negative, got {val}")
        return val
    
    def volume(self) -> float:
        """Calculate the total volume."""
        return self.x * self.y * self.z


@final
class Coordinate(SpatialBase[float]):
    """
    Represents a physical point in 3D space in millimeters.
    
    No constraints on component values.
    """
    
    def _validate_component(self, name: str, value: float) -> float:
        """Convert to float with no additional validation."""
        return float(value)
    
    def distance_to(self, other: 'Coordinate') -> float:
        """Calculate Euclidean distance to another coordinate."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
        
    def __add__(self, other: 'Coordinate') -> 'Coordinate':
        """Add two coordinates component-wise."""
        if not isinstance(other, Coordinate):
            return NotImplemented
        return Coordinate(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z
        )
        
    def __mul__(self, scalar: float) -> 'Coordinate':
        """Multiply coordinate by a scalar."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Coordinate(
            x=self.x * scalar,
            y=self.y * scalar,
            z=self.z * scalar
        )
        
    __rmul__ = __mul__  # Allow scalar * coordinate


@final
class Index(SpatialBase[int]):
    """
    Represents discrete array indices for voxel access.
    
    All components must be non-negative integers.
    """
    
    def _validate_component(self, name: str, value: int) -> int:
        """Validate that the component is a non-negative integer."""
        val = int(value)
        if val < 0:
            raise ValueError(f"{name} must be non-negative, got {val}")
        return val
    
    def to_continuous(self) -> 'ContinuousIndex':
        """Convert to a ContinuousIndex."""
        return ContinuousIndex(float(self.x), float(self.y), float(self.z))


@final
class ContinuousIndex(SpatialBase[float]):
    """
    Represents precise sub-voxel positions in array space.
    
    No constraints on component values.
    """
    
    def _validate_component(self, name: str, value: float) -> float:
        """Convert to float with no additional validation."""
        return float(value)
    
    def to_index(self) -> Index:
        """Convert to the nearest Index (rounding down)."""
        return Index(int(self.x), int(self.y), int(self.z))
    
    def round(self) -> 'ContinuousIndex':
        """Return a new ContinuousIndex with rounded components."""
        return ContinuousIndex(round(self.x), round(self.y), round(self.z))


@final
class Dimension(SpatialBase[int]):
    """
    Represents the number of voxels in each dimension of a 3D array.
    
    All components must be positive integers.
    """
    
    def _validate_component(self, name: str, value: int) -> int:
        """Validate that the component is a positive integer."""
        val = int(value)
        if val <= 0:
            raise ValueError(f"{name} must be positive, got {val}")
        return val
    
    def num_voxels(self) -> int:
        """Calculate the total number of voxels."""
        return self.x * self.y * self.z
    
    def to_volume_size(self, voxel_size: VoxelSize) -> VolumeSize:
        """Convert to physical size using the given voxel dimensions."""
        return VolumeSize(
            x=self.x * voxel_size.x,
            y=self.y * voxel_size.y,
            z=self.z * voxel_size.z
        )
    
    def contains(self, index: Index) -> bool:
        """Check if the given index is within these dimensions."""
        return (0 <= index.x < self.x and 
                0 <= index.y < self.y and 
                0 <= index.z < self.z)
