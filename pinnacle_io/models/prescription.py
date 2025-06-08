"""
SQLAlchemy model for Pinnacle Prescription data.

This module provides the Prescription model for representing treatment prescription details.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.trial import Trial


class Prescription(PinnacleBase):
    """
    Model representing a treatment prescription.

    This class stores prescription information for a treatment trial.
    """

    __tablename__ = "Prescription"

    # Primary key is inherited from PinnacleBase
    name: Mapped[str] = Column("Name", String, nullable=True)
    requested_monitor_units_per_fraction: Mapped[int] = Column(
        "RequestedMonitorUnitsPerFraction", Integer, nullable=True
    )
    prescription_dose: Mapped[float] = Column("PrescriptionDose", Float, nullable=True)
    prescription_percent: Mapped[int] = Column(
        "PrescriptionPercent", Integer, nullable=True
    )
    number_of_fractions: Mapped[int] = Column("NumberOfFractions", Integer, nullable=True)
    prescription_point: Mapped[str] = Column("PrescriptionPoint", String, nullable=True)
    method: Mapped[str] = Column("Method", String, nullable=True)
    normalization_method: Mapped[str] = Column(
        "NormalizationMethod", String, nullable=True
    )
    prescription_period: Mapped[str] = Column("PrescriptionPeriod", String, nullable=True)
    weights_proportional_to: Mapped[str] = Column(
        "WeightsProportionalTo", String, nullable=True
    )
    dose_uncertainty: Mapped[int] = Column("DoseUncertainty", Integer, nullable=True)
    prescription_uncertainty: Mapped[int] = Column(
        "PrescriptionUncertainty", Integer, nullable=True
    )
    dose_uncertainty_valid: Mapped[int] = Column(
        "DoseUncertaintyValid", Integer, nullable=True
    )
    prescrip_uncertainty_valid: Mapped[int] = Column(
        "PrescripUncertaintyValid", Integer, nullable=True
    )
    color: Mapped[str] = Column("Color", String, nullable=True)

    # Parent relationship
    trial_id: Mapped[int] = Column("TrialID", Integer, ForeignKey("Trial.ID"))
    trial: Mapped["Trial"] = relationship("Trial", back_populates="prescription_list")

    def __init__(self, **kwargs):
        """Initialize a Prescription instance.

        Args:
            **kwargs: Keyword arguments used to initialize Point attributes.

        Relationships:
            trial (Trial): The parent Trial to which this Prescription belongs (many-to-one).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<Prescription(id={self.id}, name='{self.name}', prescription_dose={self.prescription_dose}, number_of_fractions={self.number_of_fractions})>"
