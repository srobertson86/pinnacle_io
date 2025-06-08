"""
SQLAlchemy model for Pinnacle Compensator data.

This module provides the Compensator data models for representing beam compensator configuration.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Integer, ForeignKey, Float, LargeBinary
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.beam import Beam


class Compensator(PinnacleBase):
    """
    Model representing a beam compensator.

    This class stores all compensator-specific information needed for DICOM conversion,
    including export settings, dimensions, and materials.
    """

    __tablename__ = "Compensator"

    # Primary key is inherited from PinnacleBase
    name: Mapped[str] = Column("Name", String, nullable=True)
    export_name: Mapped[str] = Column("ExportName", String, nullable=True)
    tray_number: Mapped[str] = Column("TrayNumber", String, nullable=True)
    export_format: Mapped[str] = Column("ExportFormat", String, nullable=True)
    is_valid: Mapped[int] = Column("IsValid", Integer, nullable=True)
    generated_automatically: Mapped[int] = Column(
        "GeneratedAutomatically", Integer, nullable=True
    )
    proton_source_to_compensator_distance: Mapped[float] = Column(
        "ProtonSourceToCompensatorDistance", Float, nullable=True
    )
    scale_width_height: Mapped[int] = Column("ScaleWidthHeight", Integer, nullable=True)
    width: Mapped[float] = Column("Width", Float, nullable=True)
    height: Mapped[float] = Column("Height", Float, nullable=True)
    resolution_x: Mapped[float] = Column("ResolutionX", Float, nullable=True)
    resolution_y: Mapped[float] = Column("ResolutionY", Float, nullable=True)
    display_resolution: Mapped[float] = Column(
        "DisplayResolution", Float, nullable=True
    )
    compensator_hangs_down: Mapped[int] = Column(
        "CompensatorHangsDown", Integer, nullable=True
    )
    include_poly_base: Mapped[int] = Column("IncludePolyBase", Integer, nullable=True)
    max_iterations: Mapped[int] = Column("MaxIterations", Integer, nullable=True)
    min_allowable_thickness: Mapped[float] = Column(
        "MinAllowableThickness", Float, nullable=True
    )
    max_allowable_thickness: Mapped[float] = Column(
        "MaxAllowableThickness", Float, nullable=True
    )
    round_data: Mapped[int] = Column("RoundData", Integer, nullable=True)
    rounding_value: Mapped[float] = Column("RoundingValue", Float, nullable=True)
    cutoff_homogeneity: Mapped[float] = Column(
        "CutoffHomogeneity", Float, nullable=True
    )
    start_optimization_with_current: Mapped[int] = Column(
        "StartOptimizationWithCurrent", Integer, nullable=True
    )
    actual_homogeneity: Mapped[float] = Column(
        "ActualHomogeneity", Float, nullable=True
    )
    output_factor: Mapped[float] = Column("OutputFactor", Float, nullable=True)
    density: Mapped[float] = Column("Density", Float, nullable=True)
    edge_of_field_border: Mapped[float] = Column(
        "EdgeOfFieldBorder", Float, nullable=True
    )
    initial_thickness: Mapped[float] = Column("InitialThickness", Float, nullable=True)
    milling_x_scaler: Mapped[float] = Column("MillingXScaler", Float, nullable=True)
    milling_y_scaler: Mapped[float] = Column("MillingYScaler", Float, nullable=True)
    milling_z_scaler: Mapped[float] = Column("MillingZScaler", Float, nullable=True)
    milling_thickness: Mapped[float] = Column("MillingThickness", Float, nullable=True)
    positive_milled: Mapped[float] = Column("PositiveMilled", Float, nullable=True)
    optimize_to_min_dose_first_iteration: Mapped[int] = Column(
        "OptimizeToMinDoseFirstIteration", Integer, nullable=True
    )
    resample_using_linear_interpolation: Mapped[int] = Column(
        "ResampleUsingLinearInterpolation", Integer, nullable=True
    )
    fill_outside_mode: Mapped[str] = Column("FillOutsideMode", String, nullable=True)
    fill_outside_thickness: Mapped[float] = Column(
        "FillOutsideThickness", Float, nullable=True
    )
    dose_comp_mode: Mapped[str] = Column("DoseCompMode", String, nullable=True)
    type: Mapped[str] = Column("Type", String, nullable=True)
    plane_depth: Mapped[float] = Column("PlaneDepth", Float, nullable=True)
    array_object_name: Mapped[str] = Column("ArrayObjectName", String, nullable=True)
    center_at_zero: Mapped[int] = Column("CenterAtZero", Integer, nullable=True)
    thickness: Mapped[bytes] = Column(
        "Thickness", LargeBinary, nullable=True
    )  # Store array as binary
    dose_min: Mapped[float] = Column("DoseMin", Float, nullable=True)
    dose_max: Mapped[float] = Column("DoseMax", Float, nullable=True)
    dose_mean: Mapped[float] = Column("DoseMean", Float, nullable=True)
    dose_std_dev: Mapped[float] = Column("DoseStdDev", Float, nullable=True)
    wet_x_dim: Mapped[int] = Column("WetXDim", Integer, nullable=True)
    wet_y_dim: Mapped[int] = Column("WetYDim", Integer, nullable=True)

    # Parent relationship
    beam_id: Mapped[int] = Column("BeamID", Integer, ForeignKey("Beam.ID"))
    beam: Mapped["Beam"] = relationship("Beam", back_populates="compensator")

    def __init__(self, **kwargs):
        """
        Initialize a Compensator instance with optional keyword arguments.

        Args:
            **kwargs: Keyword arguments used to initialize Compensator attributes.

        Relationships:
            beam (Beam): The parent Beam to which this compensator belongs (many-to-one).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this compensator.
        """
        return f"<Compensator(id={self.id}, name='{self.name}')>"
