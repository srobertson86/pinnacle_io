"""
SQLAlchemy model for Pinnacle DoseGrid data.

This module provides the DoseGrid model for representing dose grid details.
"""

from typing import List, TYPE_CHECKING, Optional

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from pinnacle_io.models.pinnacle_base import PinnacleBase
from pinnacle_io.models.types import VoxelSize, Coordinate, Dimension

if TYPE_CHECKING:
    from pinnacle_io.models.dose import Dose


class DoseGrid(PinnacleBase):
    """
    Model representing a dose grid.

    This class stores information about the dose grid, including voxel size, dimensions,
    origin, and rotation delta.
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
        "VolRotDeltaX", Float, nullable=True
    )
    vol_rot_delta_y: Mapped[Optional[float]] = Column(
        "VolRotDeltaY", Float, nullable=True
    )
    vol_rot_delta_z: Mapped[Optional[float]] = Column(
        "VolRotDeltaZ", Float, nullable=True
    )
    display_2d: Mapped[Optional[int]] = Column("Display2D", Integer, nullable=True)
    dose_summation_type: Mapped[Optional[int]] = Column(
        "DoseSummationType", Integer, nullable=True
    )
    # Parent relationship
    trial_id: Mapped[int] = Column("TrialID", Integer, ForeignKey("Trial.ID"))
    trial = relationship("Trial", back_populates="dose_grid")

    # Child relationship
    dose_list: Mapped[List["Dose"]] = relationship(
        "Dose", back_populates="dose_grid", cascade="all, delete-orphan"
    )

    def _extract_xyz(self, entity, default_x=None, default_y=None, default_z=None):
        """
        Extract X, Y, Z components from a spatial entity.

        Args:
            entity: The entity to extract components from. Can be:
                   - An object with x, y, z attributes (e.g., VoxelSize, Coordinate, etc.)
                   - A dictionary with 'x', 'y', 'z' keys (case insensitive)
            default_x: Default value for X if not found in entity
            default_y: Default value for Y if not found in entity
            default_z: Default value for Z if not found in entity

        Returns:
            dict: {'x': x, 'y': y, 'z': z}
        """
        if entity is None:
            return {"x": default_x, "y": default_y, "z": default_z}

        if hasattr(entity, "x") and hasattr(entity, "y") and hasattr(entity, "z"):
            # Handle spatial type objects
            return {"x": entity.x, "y": entity.y, "z": entity.z}

        elif isinstance(entity, dict):
            x = entity.pop("x", entity.pop("X", default_x))
            y = entity.pop("y", entity.pop("Y", default_y))
            z = entity.pop("z", entity.pop("Z", default_z))
            return {"x": x, "y": y, "z": z}

        else:
            # Return defaults for unsupported types
            return {"x": default_x, "y": default_y, "z": default_z}

    def __init__(self, **kwargs):
        """
        Initialize a DoseGrid instance.

        Args:
            **kwargs: Keyword arguments used to initialize DoseGrid attributes.

        Relationships:
            trial (Trial): The parent Trial to which this DoseGrid belongs (many-to-one).
            dose_list (List[Dose]): The associated DoseList (one-to-many).
        """
        # Check for both snake_case and PascalCase keys
        for name1, name2 in [
            ("voxel_size", "VoxelSize"),
            ("dimension", "Dimension"),
            ("origin", "Origin"),
            ("vol_rot_delta", "VolRotDelta"),
        ]:
            value1 = self._extract_xyz(kwargs.pop(name1, None))
            value2 = self._extract_xyz(kwargs.pop(name2, None))
            for i in ["x", "y", "z"]:
                # Try to find the key in both snake_case and PascalCase (e.g., voxel_size_x and VoxelSizeX)
                keys = [f"{name1}_{i.lower()}", f"{name2}{i.upper()}"]
                value = next((kwargs[key] for key in keys if key in kwargs), None)

                # If an individual value (e.g., voxel_size_x) is not found, use the value from the spatial type object
                if value is None:
                    kwargs[keys[0]] = value1[i] if value1[i] is not None else value2[i]

        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this dose grid.
        """
        trial = (
            self.trial.name if hasattr(self.trial, "name") and self.trial else "None"
        )
        dim = (
            f"Dimension({self.dimension_x}, {self.dimension_y}, {self.dimension_z})"
            if self.dimension_x is not None
            else "None"
        )
        return f"<DoseGrid(id={self.id}, trial='{trial}', dimension={dim})>"

    @property
    def voxel_size(self) -> VoxelSize:
        """Get the voxel size as a VoxelSize object."""
        if None in (self.voxel_size_x, self.voxel_size_y, self.voxel_size_z):
            return None
        return VoxelSize(self.voxel_size_x, self.voxel_size_y, self.voxel_size_z)

    @voxel_size.setter
    def voxel_size(self, value):
        """Set the voxel size from a VoxelSize object, dict, or other compatible object."""
        if value is None:
            self.voxel_size_x = self.voxel_size_y = self.voxel_size_z = None
        elif isinstance(value, VoxelSize):
            self.voxel_size_x, self.voxel_size_y, self.voxel_size_z = (
                value.x,
                value.y,
                value.z,
            )
        elif hasattr(value, "x") and hasattr(value, "y") and hasattr(value, "z"):
            # Handle any object with x, y, z attributes (backward compatibility)
            self.voxel_size_x, self.voxel_size_y, self.voxel_size_z = (
                value.x,
                value.y,
                value.z,
            )
        elif isinstance(value, dict):
            # Handle dict with x, y, z keys (case insensitive)
            x_key = next((k for k in ["x", "X", "voxel_size_x"] if k in value), None)
            y_key = next((k for k in ["y", "Y", "voxel_size_y"] if k in value), None)
            z_key = next((k for k in ["z", "Z", "voxel_size_z"] if k in value), None)

            if x_key is not None and y_key is not None and z_key is not None:
                self.voxel_size_x = value[x_key]
                self.voxel_size_y = value[y_key]
                self.voxel_size_z = value[z_key]

    @property
    def dimension(self) -> Dimension:
        """Get the dimension as a Dimension object."""
        if None in (self.dimension_x, self.dimension_y, self.dimension_z):
            return None
        return Dimension(self.dimension_x, self.dimension_y, self.dimension_z)

    @property
    def origin(self) -> Coordinate:
        """Get the origin as a Coordinate object."""
        if None in (self.origin_x, self.origin_y, self.origin_z):
            return None
        return Coordinate(self.origin_x, self.origin_y, self.origin_z)

    @property
    def vol_rot_delta(self) -> Coordinate:
        """Get the volume rotation delta as a Coordinate object."""
        if None in (self.vol_rot_delta_x, self.vol_rot_delta_y, self.vol_rot_delta_z):
            return None
        return Coordinate(
            self.vol_rot_delta_x, self.vol_rot_delta_y, self.vol_rot_delta_z
        )
