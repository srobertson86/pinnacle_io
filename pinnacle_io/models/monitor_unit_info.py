"""
SQLAlchemy model for Pinnacle MonitorUnitInfo data.

This module provides comprehensive models for representing monitor unit calculation
information and dosimetric parameters in the Pinnacle treatment planning system.
The MonitorUnitInfo model stores all the detailed calculations and factors used
to determine the monitor units required for accurate dose delivery.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.beam import Beam


class MonitorUnitInfo(PinnacleBase):
    """
    Model representing monitor unit calculation information for treatment beams.

    This class stores comprehensive dosimetric information and calculation parameters
    used to determine the monitor units (MU) required for accurate dose delivery.
    Monitor units are the fundamental units used by linear accelerators to control
    radiation output, and their accurate calculation is critical for patient safety
    and treatment efficacy.

    The MonitorUnitInfo model contains all the factors, measurements, and geometric
    parameters that influence the monitor unit calculation, including output factors,
    transmission factors, field geometry, and prescription point characteristics.
    This information is essential for dose verification and quality assurance.

    Attributes:
        id (int): Primary key inherited from PinnacleBase
        prescription_dose (float): Prescribed dose at the prescription point in cGy
        source_to_prescription_point_distance (float): Distance from source to prescription point in cm
        total_transmission_fraction (float): Total transmission factor for all beam modifiers
        transmission_description (str): Description of transmission factors applied
        prescription_point_depth (float): Depth of prescription point in phantom in cm
        prescription_point_rad_depth (float): Radiological depth to prescription point in g/cm²
        depth_to_actual_point (float): Physical depth to actual calculation point in cm
        ssd_to_actual_point (float): Source-to-surface distance to actual point in cm
        rad_depth_to_actual_point (float): Radiological depth to actual point in g/cm²
        prescription_point_rad_depth_valid (int): Flag indicating radiological depth validity (1=valid, 0=invalid)
        prescription_point_off_axis_distance (float): Off-axis distance of prescription point in cm
        unblocked_field_area_at_sad (float): Unblocked field area at source-axis distance in cm²
        unblocked_field_perimeter_at_sad (float): Unblocked field perimeter at SAD in cm
        blocked_field_area_at_sad (float): Blocked field area at source-axis distance in cm²
        intersect_field_area_at_sad (float): Intersection field area at SAD in cm²
        normalized_dose (float): Normalized dose value in cGy
        off_axis_ratio (float): Off-axis ratio correction factor
        collimator_output_factor (float): Collimator-specific output factor
        relative_output_factor (float): Relative output factor for field size
        phantom_output_factor (float): Phantom scatter factor
        of_measurement_depth (float): Depth at which output factors were measured in cm
        output_factor_info (str): Additional information about output factor measurements
        beam_id (int): Foreign key to the parent Beam

    Relationships:
        beam (Beam): The parent beam that owns this monitor unit information (many-to-one)

    Dosimetric Calculations:
        The monitor unit calculation typically follows the formula:
        MU = (Prescribed Dose × Factors) / (Dose Rate × Output Factors)

        Where factors include:
        - Transmission factors (wedges, blocks, compensators)
        - Off-axis corrections
        - Depth corrections
        - Field size corrections

    Example:
        >>> mu_info = MonitorUnitInfo(
        ...     prescription_dose=200.0,
        ...     source_to_prescription_point_distance=100.0,
        ...     total_transmission_fraction=0.95,
        ...     normalized_dose=100.0,
        ...     collimator_output_factor=1.02,
        ...     relative_output_factor=1.0
        ... )
    """

    __tablename__ = "MonitorUnitInfo"

    # Primary key is inherited from PinnacleBase
    prescription_dose: Mapped[Optional[float]] = Column("PrescriptionDose", Float, nullable=True)
    source_to_prescription_point_distance: Mapped[Optional[float]] = Column(
        "SourceToPrescriptionPointDistance", Float, nullable=True
    )
    total_transmission_fraction: Mapped[Optional[float]] = Column(
        "TotalTransmissionFraction", Float, nullable=True
    )
    transmission_description: Mapped[Optional[str]] = Column(
        "TransmissionDescription", String, nullable=True
    )
    prescription_point_depth: Mapped[Optional[float]] = Column(
        "PrescriptionPointDepth", Float, nullable=True
    )
    prescription_point_rad_depth: Mapped[Optional[float]] = Column(
        "PrescriptionPointRadDepth", Float, nullable=True
    )
    depth_to_actual_point: Mapped[Optional[float]] = Column(
        "DepthToActualPoint", Float, nullable=True
    )
    ssd_to_actual_point: Mapped[Optional[float]] = Column("SsdToActualPoint", Float, nullable=True)
    rad_depth_to_actual_point: Mapped[Optional[float]] = Column(
        "RadDepthToActualPoint", Float, nullable=True
    )
    prescription_point_rad_depth_valid: Mapped[Optional[int]] = Column(
        "PrescriptionPointRadDepthValid", Integer, nullable=True
    )
    prescription_point_off_axis_distance: Mapped[Optional[float]] = Column(
        "PrescriptionPointOffAxisDistance", Float, nullable=True
    )
    unblocked_field_area_at_sad: Mapped[Optional[float]] = Column(
        "UnblockedFieldAreaAtSad", Float, nullable=True
    )
    unblocked_field_perimeter_at_sad: Mapped[Optional[float]] = Column(
        "UnblockedFieldPerimeterAtSad", Float, nullable=True
    )
    blocked_field_area_at_sad: Mapped[Optional[float]] = Column(
        "BlockedFieldAreaAtSad", Float, nullable=True
    )
    intersect_field_area_at_sad: Mapped[Optional[float]] = Column(
        "IntersectFieldAreaAtSad", Float, nullable=True
    )
    normalized_dose: Mapped[Optional[float]] = Column("NormalizedDose", Float, nullable=True)
    off_axis_ratio: Mapped[Optional[float]] = Column("OffAxisRatio", Float, nullable=True)
    collimator_output_factor: Mapped[Optional[float]] = Column(
        "CollimatorOutputFactor", Float, nullable=True
    )
    relative_output_factor: Mapped[Optional[float]] = Column(
        "RelativeOutputFactor", Float, nullable=True
    )
    phantom_output_factor: Mapped[Optional[float]] = Column(
        "PhantomOutputFactor", Float, nullable=True
    )
    of_measurement_depth: Mapped[Optional[float]] = Column(
        "OfMeasurementDepth", Float, nullable=True
    )
    output_factor_info: Mapped[Optional[str]] = Column("OutputFactorInfo", String, nullable=True)

    # Parent relationship
    beam_id: Mapped[int] = Column("BeamID", Integer, ForeignKey("Beam.ID"))
    beam: Mapped["Beam"] = relationship(
        "Beam",
        back_populates="monitor_unit_info",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __init__(self, **kwargs):
        """
        Initialize a MonitorUnitInfo instance.

        This constructor handles initialization of all monitor unit calculation
        attributes and relationships. It supports both direct attribute assignment
        and nested relationship creation for the parent beam.

        Args:
            **kwargs: Keyword arguments used to initialize MonitorUnitInfo attributes.
                Can include any of the dosimetric calculation attributes as well as
                relationship data for the parent beam.

        Dosimetric Parameters:
            prescription_dose (float): Prescribed dose in cGy
            source_to_prescription_point_distance (float): Distance in cm
            total_transmission_fraction (float): Transmission factor (0.0-1.0)
            normalized_dose (float): Normalized dose value in cGy
            collimator_output_factor (float): Output factor for collimator setting
            relative_output_factor (float): Field size dependent output factor
            phantom_output_factor (float): Phantom scatter factor

        Relationship Parameters:
            beam (dict or Beam): Parent beam configuration data

        Example:
            >>> mu_info = MonitorUnitInfo(
            ...     prescription_dose=200.0,
            ...     normalized_dose=100.0,
            ...     total_transmission_fraction=0.95,
            ...     collimator_output_factor=1.02,
            ...     beam_id=1
            ... )
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """Return a string representation of this monitor unit info."""
        return f"<MonitorUnitInfo(id={self.id}, prescription_dose={self.prescription_dose}, normalized_dose={self.normalized_dose})>"
