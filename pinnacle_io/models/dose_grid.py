"""
SQLAlchemy model for Pinnacle DoseGrid data.

This module provides the DoseGrid model for representing dose grid details in the Pinnacle
treatment planning system. The dose grid defines the 3D volume where dose is calculated.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase
from pinnacle_io.models.types import VoxelSize, Coordinate, Dimension

if TYPE_CHECKING:
    from pinnacle_io.models.dose import Dose
    from pinnacle_io.models.trial import Trial


class DoseGrid(PinnacleBase):
    """
    Model representing a dose grid in the Pinnacle treatment planning system.

    This class stores information about the 3D grid where dose is calculated, including:
    - Voxel dimensions and grid spacing
    - Grid dimensions in number of voxels
    - Origin position in DICOM coordinates
    - Volume rotation deltas for non-axial orientations
    - Display and summation settings

    The dose grid is associated with a parent Trial and may have multiple Dose objects
    associated with it, representing different dose calculations on the same grid.

    Attributes:
        id (int): Primary key (inherited from PinnacleBase)
        voxel_size_x (Optional[float]): Voxel size in X direction (mm)
        voxel_size_y (Optional[float]): Voxel size in Y direction (mm)
        voxel_size_z (Optional[float]): Voxel size in Z direction (mm)
        dimension_x (Optional[int]): Number of voxels in X direction
        dimension_y (Optional[int]): Number of voxels in Y direction
        dimension_z (Optional[int]): Number of voxels in Z direction
        origin_x (Optional[float]): X coordinate of grid origin (mm)
        origin_y (Optional[float]): Y coordinate of grid origin (mm)
        origin_z (Optional[float]): Z coordinate of grid origin (mm)
        vol_rot_delta_x (Optional[float]): X rotation delta for non-axial orientations (radians)
        vol_rot_delta_y (Optional[float]): Y rotation delta for non-axial orientations (radians)
        vol_rot_delta_z (Optional[float]): Z rotation delta for non-axial orientations (radians)
        display_2d (Optional[int]): Flag indicating if 2D display is enabled
        dose_summation_type (Optional[int]): Type of dose summation

    Relationships:
        trial (Trial): The parent Trial to which this DoseGrid belongs (many-to-one).
                      Back-populates to Trial.dose_grid.
        dose_list (List[Dose]): List of Dose objects associated with this grid (one-to-many).
                              Back-populates to Dose.dose_grid.
    """

    __tablename__ = "DoseGrid"

    # Primary key is inherited from PinnacleBase
    voxel_size_x: Mapped[Optional[float]] = Column("VoxelSizeX", Float, nullable=True)
    voxel_size_y: Mapped[Optional[float]] = Column("VoxelSizeY", Float, nullable=True)
    voxel_size_z: Mapped[Optional[float]] = Column("VoxelSizeZ", Float, nullable=True)
    
    dimension_x: Mapped[Optional[int]] = Column("DimensionX", Integer, nullable=True)
    dimension_y: Mapped[Optional[int]] = Column("DimensionY", Integer, nullable=True)
    dimension_z: Mapped[Optional[int]] = Column("DimensionZ", Integer, nullable=True)
    
    origin_x: Mapped[Optional[float]] = Column("OriginX", Float, nullable=True)
    origin_y: Mapped[Optional[float]] = Column("OriginY", Float, nullable=True)
    origin_z: Mapped[Optional[float]] = Column("OriginZ", Float, nullable=True)
    
    vol_rot_delta_x: Mapped[Optional[float]] = Column(
        "VolRotDeltaX", Float, nullable=True, doc="X rotation delta in radians"
    )
    vol_rot_delta_y: Mapped[Optional[float]] = Column(
        "VolRotDeltaY", Float, nullable=True, doc="Y rotation delta in radians"
    )
    vol_rot_delta_z: Mapped[Optional[float]] = Column(
        "VolRotDeltaZ", Float, nullable=True, doc="Z rotation delta in radians"
    )
    
    display_2d: Mapped[Optional[int]] = Column(
        "Display2D", 
        Integer, 
        nullable=True, 
        doc="Flag indicating if 2D display is enabled (1) or disabled (0)"
    )
    dose_summation_type: Mapped[Optional[int]] = Column(
        "DoseSummationType", 
        Integer, 
        nullable=True,
        doc="Type of dose summation (e.g., 0=plan, 1=fraction, 2=beam, etc.)"
    )
    
    # Parent relationship with back-population to Trial.dose_grid
    trial_id: Mapped[int] = Column(
        "TrialID", 
        Integer, 
        ForeignKey("Trial.ID"),
        nullable=False,
        doc="Foreign key to the parent Trial"
    )
    trial: Mapped["Trial"] = relationship(
        "Trial", 
        back_populates="dose_grid",
        doc="The parent Trial to which this DoseGrid belongs"
    )

    # Child relationship with Dose objects
    dose_list: Mapped[List["Dose"]] = relationship(
        "Dose", 
        back_populates="dose_grid", 
        cascade="all, delete-orphan",
        lazy="selectin",
        doc="List of Dose objects associated with this grid"
    )

    def _extract_xyz(
        self, 
        entity: Any,
        default_x: Optional[Union[float, int]] = None, 
        default_y: Optional[Union[float, int]] = None, 
        default_z: Optional[Union[float, int]] = None
    ) -> Dict[str, Optional[Union[float, int]]]:
        """
        Extract X, Y, Z components from a spatial entity.

        This helper method handles multiple input formats for spatial data:
        - Objects with x, y, z attributes (e.g., VoxelSize, Coordinate, Dimension)
        - Dictionaries with 'x', 'y', 'z' keys (case insensitive)
        - None values (returns defaults)

        Args:
            entity: The entity to extract components from. Can be:
                   - A VoxelSize, Dimension, or Coordinate object
                   - A dict with 'x', 'y', 'z' keys (case insensitive)
                   - None (returns default values)
            default_x: Default value for X if not found in entity
            default_y: Default value for Y if not found in entity
            default_z: Default value for Z if not found in entity

        Returns:
            Dict[str, Optional[Union[float, int]]]: 
                Dictionary with 'x', 'y', 'z' keys and their values
                (types match the input types where possible)

        Example:
            >>> grid = DoseGrid()
            >>> # From VoxelSize object
            >>> vs = VoxelSize(1.0, 2.0, 3.0)
            >>> grid._extract_xyz(vs)
            {'x': 1.0, 'y': 2.0, 'z': 3.0}
            
            >>> # From dictionary
            >>> grid._extract_xyz({'x': 1, 'y': 2, 'z': 3})
            {'x': 1, 'y': 2, 'z': 3}
            
            >>> # With defaults
            >>> grid._extract_xyz(None, default_x=0, default_y=0, default_z=0)
            {'x': 0, 'y': 0, 'z': 0}
        """
        if entity is None:
            return {"x": default_x, "y": default_y, "z": default_z}

        if hasattr(entity, "x") and hasattr(entity, "y") and hasattr(entity, "z"):
            # Handle spatial type objects (VoxelSize, Dimension, Coordinate)
            return {"x": entity.x, "y": entity.y, "z": entity.z}

        if isinstance(entity, dict):
            # Handle dict with x, y, z keys (case insensitive)
            x = entity.get("x", entity.get("X", default_x))
            y = entity.get("y", entity.get("Y", default_y))
            z = entity.get("z", entity.get("Z", default_z))
            return {"x": x, "y": y, "z": z}

        # Return defaults for unsupported types
        return {"x": default_x, "y": default_y, "z": default_z}

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a DoseGrid instance with the given parameters.

        This constructor handles initialization of the dose grid with support for both
        individual component values (e.g., voxel_size_x, voxel_size_y, voxel_size_z)
        and composite objects (e.g., voxel_size=VoxelSize(1,1,1)).

        Args:
            **kwargs: Keyword arguments corresponding to model attributes.
                Supported keyword arguments include all column names as attributes and:
                - voxel_size: VoxelSize object or dict with x,y,z values
                - dimension: Dimension object or dict with x,y,z values
                - origin: Coordinate object or dict with x,y,z values
                - vol_rot_delta: Coordinate object or dict with x,y,z values
                - trial: The parent Trial object
                - dose_list: List of Dose objects

        Example:
            >>> # Initialize with individual values
            >>> grid1 = DoseGrid(
            ...     voxel_size_x=2.5, voxel_size_y=2.5, voxel_size_z=3.0,
            ...     dimension_x=128, dimension_y=128, dimension_z=64,
            ...     origin_x=-160.0, origin_y=-160.0, origin_z=0.0
            ... )
            >>>
            >>> # Initialize with composite objects
            >>> from pinnacle_io.models.types import VoxelSize, Dimension, Coordinate
            >>> grid2 = DoseGrid(
            ...     voxel_size=VoxelSize(2.5, 2.5, 3.0),
            ...     dimension=Dimension(128, 128, 64),
            ...     origin=Coordinate(-160.0, -160.0, 0.0)
            ... )
        """
        # Check for both snake_case and PascalCase keys for spatial properties
        for name1, name2 in [
            ("voxel_size", "VoxelSize"),
            ("dimension", "Dimension"),
            ("origin", "Origin"),
            ("vol_rot_delta", "VolRotDelta"),
        ]:
            # Extract values from both naming conventions
            value1 = self._extract_xyz(kwargs.pop(name1, None))
            value2 = self._extract_xyz(kwargs.pop(name2, None))
            
            # Process x, y, z components
            for i in ["x", "y", "z"]:
                # Try to find the key in both snake_case and PascalCase
                keys = [f"{name1}_{i}", f"{name2}{i.upper()}"]
                value = next((kwargs[key] for key in keys if key in kwargs), None)

                # If an individual value is not found, use the value from the spatial object
                if value is None:
                    kwargs[keys[0]] = value1[i] if value1[i] is not None else value2[i]

        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this dose grid.

        Returns:
            str: A string representation in the format:
                <DoseGrid(id=X, trial='trial_name', dimension=(XxYxZ))>
        """
        trial_name = getattr(getattr(self, 'trial', ''), 'name', '')
        dim_str = (
            f"({self.dimension_x}, {self.dimension_y}, {self.dimension_z})"
            if None not in (self.dimension_x, self.dimension_y, self.dimension_z)
            else "(0, 0, 0)"
        )
        return f"<DoseGrid(id={self.id}, trial='{trial_name}', dimension={dim_str})>"

    @property
    def voxel_size(self) -> Optional[VoxelSize]:
        """
        Get the voxel size as a VoxelSize object.

        Returns:
            Optional[VoxelSize]: VoxelSize object with x, y, z dimensions in mm,
                               or None if any dimension is not set.
        """
        if None in (self.voxel_size_x, self.voxel_size_y, self.voxel_size_z):
            return None
        return VoxelSize(self.voxel_size_x, self.voxel_size_y, self.voxel_size_z)

    @voxel_size.setter
    def voxel_size(self, value: Union[VoxelSize, Dict[str, float], None]) -> None:
        """
        Set the voxel size from a VoxelSize object, dict, or other compatible object.

        Args:
            value: The value to set. Can be:
                  - A VoxelSize object (recommended for type safety)
                  - A dict with 'x', 'y', 'z' keys (case insensitive)
                  - An object with x, y, z attributes
                  - None (sets all dimensions to None)

        Raises:
            TypeError: If the input type is not supported.
            ValueError: If the dictionary is missing required keys or contains invalid values.

        Example:
            >>> grid = DoseGrid()
            >>> # Using VoxelSize object (recommended)
            >>> grid.voxel_size = VoxelSize(1.0, 1.0, 2.0)
            >>> 
            >>> # Using dictionary
            >>> grid.voxel_size = {'x': 1.0, 'y': 1.0, 'z': 2.0}
            >>>
            >>> # Using None to clear
            >>> grid.voxel_size = None
        """
        if value is None:
            self.voxel_size_x = self.voxel_size_y = self.voxel_size_z = None
            return
            
        try:
            if isinstance(value, VoxelSize):
                vs = value
            elif hasattr(value, "x") and hasattr(value, "y") and hasattr(value, "z"):
                # Handle any object with x, y, z attributes
                vs = VoxelSize(float(value.x), float(value.y), float(value.z))
            elif isinstance(value, dict):
                # Handle dict with x, y, z keys (case insensitive)
                x = float(value.get("x", value.get("X", 0.0)))
                y = float(value.get("y", value.get("Y", 0.0)))
                z = float(value.get("z", value.get("Z", 0.0)))
                vs = VoxelSize(x, y, z)
            else:
                raise TypeError(
                    f"Expected VoxelSize, dict, or object with x,y,z attributes, got {type(value).__name__}"
                )
            
            # Only assign if validation passed
            self.voxel_size_x, self.voxel_size_y, self.voxel_size_z = vs.x, vs.y, vs.z
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid voxel size value: {e}") from e

    @property
    def dimension(self) -> Optional[Dimension]:
        """
        Get the grid dimensions as a Dimension object.

        Returns:
            Optional[Dimension]: Dimension object with x, y, z sizes in voxels,
                              or None if any dimension is not set.
        """
        if None in (self.dimension_x, self.dimension_y, self.dimension_z):
            return None
        return Dimension(self.dimension_x, self.dimension_y, self.dimension_z)
    
    @dimension.setter
    def dimension(self, value: Union[Dimension, Dict[str, int], None]) -> None:
        """
        Set the grid dimensions from a Dimension object, dict, or other compatible object.

        Args:
            value: The value to set. Can be:
                  - A Dimension object (recommended for type safety)
                  - A dict with 'x', 'y', 'z' keys (case insensitive)
                  - An object with x, y, z attributes
                  - None (sets all dimensions to None)

        Raises:
            ValueError: If the input cannot be converted to valid dimensions.

        Example:
            >>> grid = DoseGrid()
            >>> # Using Dimension object (recommended)
            >>> grid.dimension = Dimension(128, 128, 64)
            >>> 
            >>> # Using dictionary
            >>> grid.dimension = {'x': 128, 'y': 128, 'z': 64}
            >>>
            >>> # Using None to clear
            >>> grid.dimension = None
        """
        if value is None:
            self.dimension_x = self.dimension_y = self.dimension_z = None
            return
            
        try:
            if isinstance(value, Dimension):
                dim = value
            elif hasattr(value, "x") and hasattr(value, "y") and hasattr(value, "z"):
                # Handle any object with x, y, z attributes
                dim = Dimension(int(value.x), int(value.y), int(value.z))
            elif isinstance(value, dict):
                # Handle dict with x, y, z keys (case insensitive)
                x = int(value.get("x", value.get("X", 0)))
                y = int(value.get("y", value.get("Y", 0)))
                z = int(value.get("z", value.get("Z", 0)))
                dim = Dimension(x, y, z)
            else:
                raise TypeError(
                    f"Expected Dimension, dict, or object with x,y,z attributes, got {type(value).__name__}"
                )
            
            # Only assign if validation passed
            self.dimension_x, self.dimension_y, self.dimension_z = dim.x, dim.y, dim.z
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid dimension value: {e}") from e

    @property
    def origin(self) -> Optional[Coordinate]:
        """
        Get the grid origin as a Coordinate object.

        Returns:
            Optional[Coordinate]: Coordinate object with x, y, z position in mm,
                               or None if any coordinate is not set.
        """
        if None in (self.origin_x, self.origin_y, self.origin_z):
            return None
        return Coordinate(self.origin_x, self.origin_y, self.origin_z)
    
    @origin.setter
    def origin(self, value: Union[Coordinate, Dict[str, float], None]) -> None:
        """
        Set the grid origin from a Coordinate object or dict.

        Args:
            value: The value to set. Can be:
                  - A Coordinate object
                  - A dict with 'x', 'y', 'z' keys (case insensitive)
                  - An object with x, y, z attributes
                  - None (sets all coordinates to None)
        """
        if value is None:
            self.origin_x = self.origin_y = self.origin_z = None
        elif hasattr(value, "x") and hasattr(value, "y") and hasattr(value, "z"):
            self.origin_x, self.origin_y, self.origin_z = value.x, value.y, value.z
        elif isinstance(value, dict):
            self.origin_x = value.get("x", value.get("X"))
            self.origin_y = value.get("y", value.get("Y"))
            self.origin_z = value.get("z", value.get("Z"))

    @property
    def vol_rot_delta(self) -> Optional[Coordinate]:
        """
        Get the volume rotation deltas as a Coordinate object.

        Returns:
            Optional[Coordinate]: Coordinate object with x, y, z rotation deltas in radians,
                               or None if any delta is not set.
        """
        if None in (self.vol_rot_delta_x, self.vol_rot_delta_y, self.vol_rot_delta_z):
            return None
        return Coordinate(
            self.vol_rot_delta_x, 
            self.vol_rot_delta_y, 
            self.vol_rot_delta_z
        )
    
    @vol_rot_delta.setter
    def vol_rot_delta(self, value: Union[Coordinate, Dict[str, float], None]) -> None:
        """
        Set the volume rotation deltas from a Coordinate object or dict.

        Args:
            value: The value to set. Can be:
                  - A Coordinate object
                  - A dict with 'x', 'y', 'z' keys (case insensitive)
                  - An object with x, y, z attributes
                  - None (sets all deltas to None)
        """
        if value is None:
            self.vol_rot_delta_x = self.vol_rot_delta_y = self.vol_rot_delta_z = None
        elif hasattr(value, "x") and hasattr(value, "y") and hasattr(value, "z"):
            self.vol_rot_delta_x = value.x
            self.vol_rot_delta_y = value.y
            self.vol_rot_delta_z = value.z
        elif isinstance(value, dict):
            self.vol_rot_delta_x = value.get("x", value.get("X"))
            self.vol_rot_delta_y = value.get("y", value.get("Y"))
            self.vol_rot_delta_z = value.get("z", value.get("Z"))
    
    def get_grid_extent(self) -> Optional[Tuple[float, float, float]]:
        """
        Calculate the physical extent of the grid in millimeters.

        Returns:
            Optional[Tuple[float, float, float]]: A tuple of (width, height, depth) in mm,
                                               or None if any dimension is not set.
        """
        if None in (self.dimension_x, self.dimension_y, self.dimension_z,
                   self.voxel_size_x, self.voxel_size_y, self.voxel_size_z):
            return None
            
        return (
            self.dimension_x * self.voxel_size_x,
            self.dimension_y * self.voxel_size_y,
            self.dimension_z * self.voxel_size_z
        )
    
    def get_voxel_volume(self) -> Optional[float]:
        """
        Calculate the volume of a single voxel in cubic millimeters.

        Returns:
            Optional[float]: Voxel volume in mm³, or None if any voxel dimension is not set.
        """
        if None in (self.voxel_size_x, self.voxel_size_y, self.voxel_size_z):
            return None
            
        return self.voxel_size_x * self.voxel_size_y * self.voxel_size_z
    
    def get_total_volume(self) -> Optional[float]:
        """
        Calculate the total volume of the grid in cubic millimeters.

        Returns:
            Optional[float]: Total volume in mm³, or None if any dimension is not set.
        """
        extent = self.get_grid_extent()
        return extent[0] * extent[1] * extent[2] if extent else None
