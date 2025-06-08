"""
Point model for Pinnacle IO.

This module provides the Point data model for representing Pinnacle treatment plans.
"""

from typing import Optional, Tuple  # , TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.versioned_base import VersionedBase

# if TYPE_CHECKING:
#     from pinnacle_io.models.plan import Plan


class Point(VersionedBase):
    """
    Model representing a point in a Pinnacle treatment plan.

    This class stores point information needed for DICOM conversion.
    In Pinnacle, a Plan is a container that can have multiple Trials.
    """

    __tablename__ = "Point"

    # Point-specific information
    name: Mapped[str] = Column("Name", String, nullable=True)
    x_coord: Mapped[float] = Column("XCoord", Float, nullable=True)
    y_coord: Mapped[float] = Column("YCoord", Float, nullable=True)
    z_coord: Mapped[float] = Column("ZCoord", Float, nullable=True)
    x_rotation: Mapped[float] = Column("XRotation", Float, nullable=True)
    y_rotation: Mapped[float] = Column("YRotation", Float, nullable=True)
    z_rotation: Mapped[float] = Column("ZRotation", Float, nullable=True)
    radius: Mapped[float] = Column("Radius", Float, nullable=True)
    color: Mapped[str] = Column("Color", String, nullable=True)
    coord_sys: Mapped[str] = Column("CoordSys", String, nullable=True)
    coordinate_format: Mapped[str] = Column("CoordinateFormat", String, nullable=True)
    display_2d: Mapped[str] = Column("Display2d", String, nullable=True)
    display_3d: Mapped[str] = Column("Display3d", String, nullable=True)
    volume_name: Mapped[str] = Column("VolumeName", String, nullable=True)
    poi_interpreted_type: Mapped[str] = Column("PoiInterpretedType", String, nullable=True)
    poi_display_on_other_volumes: Mapped[int] = Column(
        "PoiDisplayOnOtherVolumes", Integer, nullable=True
    )
    is_locked: Mapped[int] = Column("IsLocked", Integer, nullable=True)

    # Parent relationship
    plan_id: Mapped[Optional[int]] = Column(
        "PlanID", Integer, ForeignKey("Plan.ID"), nullable=True
    )
    plan = relationship("Plan", back_populates="point_list")

    def __init__(self, **kwargs):
        """Initialize a Point instance.

        Args:
            **kwargs: Keyword arguments used to initialize Point attributes.

        Relationships:
            plan (Plan): The parent Plan to which this Point belongs (many-to-one).
        """
        super().__init__(**kwargs)

    @property
    def coordinates(self) -> Tuple[float, float, float]:
        """Return the coordinates of the point as a tuple (x_coord, y_coord, z_coord)."""
        return (self.x_coord, self.y_coord, self.z_coord)

    def __repr__(self) -> str:
        return (
            f"<Point(id={self.id}, name='{self.name}', coordinates={self.coordinates})>"
        )
