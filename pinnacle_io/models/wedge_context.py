"""
WedgeContext model for Pinnacle IO.

This module provides the WedgeContext data models for representing beam configuration.
"""

from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.control_point import ControlPoint


class WedgeContext(PinnacleBase):
    """
    Model representing a wedge.

    This class stores all wedge-specific information needed for DICOM conversion.
    """

    __tablename__ = "WedgeContext"

    # Required fields (commented out in original)
    wedge_id: Mapped[str] = Column("WedgeID", String)
    wedge_number: Mapped[int] = Column("WedgeNumber", Integer)
    wedge_angle: Mapped[float] = Column("WedgeAngle", Float)  # in degrees

    # Optional fields with nullable=True
    wedge_type: Mapped[str] = Column("WedgeType", String, nullable=True)  # STANDARD, DYNAMIC, etc.
    wedge_orientation: Mapped[str] = Column("WedgeOrientation", String, nullable=True)  # X, Y
    wedge_position: Mapped[str] = Column("WedgePosition", String, nullable=True)  # IN, OUT

    # Physical properties
    material: Mapped[str] = Column("Material", String, nullable=True)
    source_to_wedge_distance: Mapped[Optional[float]] = Column("SourceToWedgeDistance", Float, nullable=True)  # in mm

    wedge_name: Mapped[str] = Column("WedgeName", String, nullable=True)
    orientation: Mapped[str] = Column("Orientation", String, nullable=True)
    offset_origin: Mapped[str] = Column("OffsetOrigin", String, nullable=True)
    offset_distance: Mapped[float] = Column("OffsetDistance", Float, nullable=True)
    angle: Mapped[str] = Column("Angle", String, nullable=True)
    min_deliverable_mu: Mapped[int] = Column("MinDeliverableMU", Integer, nullable=True)
    max_deliverable_mu: Mapped[float] = Column("MaxDeliverableMU", Float, nullable=True)

    # Parent relationship
    control_point_id: Mapped[Optional[int]] = Column(
        "ControlPointID", Integer, ForeignKey("ControlPoint.ID"), nullable=True
    )
    control_point: Mapped[Optional["ControlPoint"]] = relationship(
        "ControlPoint", back_populates="wedge_context"
    )

    def __init__(self, **kwargs):
        """
        Initialize a WedgeContext instance.

        Args:
            **kwargs: Keyword arguments used to initialize WedgeContext attributes.

        Relationships:
            control_point (ControlPoint): The parent ControlPoint to which this WedgeContext belongs (many-to-one).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<WedgeContext(id={self.id}, name='{self.wedge_name}', angle='{self.angle}', orientation='{self.orientation}')>"
