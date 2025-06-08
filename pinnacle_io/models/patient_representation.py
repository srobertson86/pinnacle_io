"""
SQLAlchemy model for Pinnacle PatientRepresentation data.

This module provides the PatientRepresentation model for representing patient position and setup information.
"""

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from pinnacle_io.models.pinnacle_base import PinnacleBase


class PatientRepresentation(PinnacleBase):
    """
    Model representing patient representation details.

    This class stores patient representation information for a treatment trial.
    """

    __tablename__ = "PatientRepresentation"

    # Primary key is inherited from PinnacleBase
    patient_volume_name: Mapped[str] = Column("PatientVolumeName", String, nullable=True)
    ct_to_density_name: Mapped[str] = Column("CTToDensityName", String, nullable=True)
    ct_to_density_version: Mapped[str] = Column(
        "CTToDensityVersion", String, nullable=True
    )
    dm_table_name: Mapped[str] = Column("DMTableName", String, nullable=True)
    dm_table_version: Mapped[str] = Column("DMTableVersion", String, nullable=True)
    top_z_padding: Mapped[int] = Column("TopZPadding", Integer, nullable=True)
    bottom_z_padding: Mapped[int] = Column("BottomZPadding", Integer, nullable=True)
    high_res_z_spacing_for_variable: Mapped[float] = Column(
        "HighResZSpacingForVariable", Float, nullable=True
    )
    outside_patient_is_ct_number: Mapped[int] = Column(
        "OutsidePatientIsCTNumber", Integer, nullable=True
    )
    outside_patient_air_threshold: Mapped[float] = Column(
        "OutsidePatientAirThreshold", Float, nullable=True
    )
    ct_to_density_table_accepted: Mapped[int] = Column(
        "CTToDensityTableAccepted", Integer, nullable=True
    )
    ct_to_density_table_extended: Mapped[int] = Column(
        "CTToDensityTableExtended", Integer, nullable=True
    )
    ct_to_stopping_power_table_name: Mapped[str] = Column(
        "CTToStoppingPowerTableName", String, nullable=True
    )
    ct_to_stopping_power_version: Mapped[str] = Column(
        "CTToStoppingPowerVersion", String, nullable=True
    )
    ct_to_stopping_power_extended: Mapped[int] = Column(
        "CTToStoppingPowerExtended", Integer, nullable=True
    )
    ct_to_stopping_power_accepted: Mapped[int] = Column(
        "CTToStoppingPowerAccepted", Integer, nullable=True
    )

    # Foreign keys
    trial_id: Mapped[int] = Column(
        "TrialID", Integer, ForeignKey("Trial.ID"), nullable=True
    )

    # Relationships
    trial = relationship("Trial", back_populates="patient_representation")

    def __init__(self, **kwargs):
        """
        Initialize a PatientRepresentation instance.

        Args:
            **kwargs: Keyword arguments used to initialize PatientRepresentation attributes.

        Relationships:
            trial (Trial): The parent Trial to which this PatientRepresentation belongs (many-to-one).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<PatientRepresentation(id={self.id}, top_z_padding={self.top_z_padding}, bottom_z_padding={self.bottom_z_padding})>"
