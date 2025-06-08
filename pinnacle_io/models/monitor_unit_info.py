"""
SQLAlchemy model for Pinnacle MonitorUnitInfo data.

This module provides the MonitorUnitInfo data models for representing monitor unit information.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.beam import Beam


class MonitorUnitInfo(PinnacleBase):
    """
    Model representing monitor unit information.
    """

    __tablename__ = "MonitorUnitInfo"

    # Primary key is inherited from PinnacleBase
    prescription_dose: Mapped[float] = Column("PrescriptionDose", Float, nullable=True)
    source_to_prescription_point_distance: Mapped[float] = Column(
        "SourceToPrescriptionPointDistance", Float, nullable=True
    )
    total_transmission_fraction: Mapped[float] = Column(
        "TotalTransmissionFraction", Float, nullable=True
    )
    transmission_description: Mapped[str] = Column(
        "TransmissionDescription", String, nullable=True
    )
    prescription_point_depth: Mapped[float] = Column(
        "PrescriptionPointDepth", Float, nullable=True
    )
    prescription_point_rad_depth: Mapped[float] = Column(
        "PrescriptionPointRadDepth", Float, nullable=True
    )
    depth_to_actual_point: Mapped[float] = Column(
        "DepthToActualPoint", Float, nullable=True
    )
    ssd_to_actual_point: Mapped[float] = Column("SsdToActualPoint", Float, nullable=True)
    rad_depth_to_actual_point: Mapped[float] = Column(
        "RadDepthToActualPoint", Float, nullable=True
    )
    prescription_point_rad_depth_valid: Mapped[int] = Column(
        "PrescriptionPointRadDepthValid", Integer, nullable=True
    )
    prescription_point_off_axis_distance: Mapped[float] = Column(
        "PrescriptionPointOffAxisDistance", Float, nullable=True
    )
    unblocked_field_area_at_sad: Mapped[float] = Column(
        "UnblockedFieldAreaAtSad", Float, nullable=True
    )
    unblocked_field_perimeter_at_sad: Mapped[float] = Column(
        "UnblockedFieldPerimeterAtSad", Float, nullable=True
    )
    blocked_field_area_at_sad: Mapped[float] = Column(
        "BlockedFieldAreaAtSad", Float, nullable=True
    )
    intersect_field_area_at_sad: Mapped[float] = Column(
        "IntersectFieldAreaAtSad", Float, nullable=True
    )
    normalized_dose: Mapped[float] = Column("NormalizedDose", Float, nullable=True)
    off_axis_ratio: Mapped[float] = Column("OffAxisRatio", Float, nullable=True)
    collimator_output_factor: Mapped[float] = Column(
        "CollimatorOutputFactor", Float, nullable=True
    )
    relative_output_factor: Mapped[float] = Column(
        "RelativeOutputFactor", Float, nullable=True
    )
    phantom_output_factor: Mapped[float] = Column(
        "PhantomOutputFactor", Float, nullable=True
    )
    of_measurement_depth: Mapped[float] = Column(
        "OfMeasurementDepth", Float, nullable=True
    )
    output_factor_info: Mapped[str] = Column("OutputFactorInfo", String, nullable=True)

    # Parent relationship
    beam_id: Mapped[int] = Column("BeamID", Integer, ForeignKey("Beam.ID"))
    beam: Mapped["Beam"] = relationship("Beam", back_populates="monitor_unit_info")

    def __init__(self, **kwargs):
        """Initialize a MonitorUnitInfo instance.
        Args:
            **kwargs: Keyword arguments used to initialize MonitorUnitInfo attributes.

        Relationships:
            beam (Beam): The parent Beam to which this MonitorUnitInfo belongs (many-to-one).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """Return a string representation of this monitor unit info."""
        return f"<MonitorUnitInfo(id={self.id}, prescription_dose={self.prescription_dose}, normalized_dose={self.normalized_dose})>"
