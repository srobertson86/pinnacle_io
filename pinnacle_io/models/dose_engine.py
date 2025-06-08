"""
SQLAlchemy model for Pinnacle Dose Engine data.

This module provides the Dose Engine data models for representing dose engine configuration.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.beam import Beam


class DoseEngine(PinnacleBase):
    """
    Model representing a dose engine configuration.

    This class stores all dose engine-specific information needed for DICOM conversion,
    including type, convolution settings, and statistics tracking.
    """

    __tablename__ = "DoseEngine"

    # Primary key is inherited from PinnacleBase
    type_name: Mapped[Optional[str]] = Column("TypeName", String, nullable=True)
    convolve_homogeneous: Mapped[Optional[int]] = Column(
        "ConvolveHomogeneous", Integer, nullable=True
    )
    fluence_homogeneous: Mapped[Optional[int]] = Column(
        "FluenceHomogeneous", Integer, nullable=True
    )
    flat_water_phantom: Mapped[Optional[int]] = Column(
        "FlatWaterPhantom", Integer, nullable=True
    )
    flat_homogeneous: Mapped[Optional[int]] = Column(
        "FlatHomogeneous", Integer, nullable=True
    )
    electron_homogeneous: Mapped[Optional[int]] = Column(
        "ElectronHomogeneous", Integer, nullable=True
    )
    fluence_type: Mapped[Optional[str]] = Column("FluenceType", String, nullable=True)
    long_step_tuning_factor: Mapped[Optional[float]] = Column(
        "LongStepTuningFactor", Float, nullable=True
    )
    short_step_length: Mapped[Optional[float]] = Column(
        "ShortStepLength", Float, nullable=True
    )
    number_of_short_steps: Mapped[Optional[int]] = Column(
        "NumberOfShortSteps", Integer, nullable=True
    )
    split_fluence_field_size_cutoff: Mapped[Optional[int]] = Column(
        "SplitFluenceFieldSizeCutoff", Integer, nullable=True
    )
    azimuthal_bin_count: Mapped[Optional[int]] = Column(
        "AzimuthalBinCount", Integer, nullable=True
    )
    zenith_bin_count: Mapped[Optional[int]] = Column(
        "ZenithBinCount", Integer, nullable=True
    )
    cum_kernel_radial_bin_width: Mapped[Optional[float]] = Column(
        "CumKernelRadialBinWidth", Float, nullable=True
    )
    siddon_corner_cutoff: Mapped[Optional[float]] = Column(
        "SiddonCornerCutoff", Float, nullable=True
    )
    nrd_bin_width: Mapped[Optional[float]] = Column("NrdBinWidth", Float, nullable=True)
    allowable_dose_diff: Mapped[Optional[float]] = Column(
        "AllowableDoseDiff", Float, nullable=True
    )
    high_fluence_cutoff: Mapped[Optional[float]] = Column(
        "HighFluenceCutoff", Float, nullable=True
    )
    low_first_deriv_cutoff: Mapped[Optional[float]] = Column(
        "LowFirstDerivCutoff", Float, nullable=True
    )
    low_second_deriv_cutoff: Mapped[Optional[float]] = Column(
        "LowSecondDerivCutoff", Float, nullable=True
    )
    high_first_deriv_cutoff: Mapped[Optional[float]] = Column(
        "HighFirstDerivCutoff", Float, nullable=True
    )
    high_second_deriv_cutoff: Mapped[Optional[float]] = Column(
        "HighSecondDerivCutoff", Float, nullable=True
    )
    adaptive_levels: Mapped[Optional[int]] = Column(
        "AdaptiveLevels", Integer, nullable=True
    )
    energy_flatness_cutoff: Mapped[Optional[float]] = Column(
        "EnergyFlatnessCutoff", Float, nullable=True
    )
    energy_flatness_minimum_distance: Mapped[Optional[float]] = Column(
        "EnergyFlatnessMinimumDistance", Float, nullable=True
    )
    energy_flatness_scaling_distance: Mapped[Optional[float]] = Column(
        "EnergyFlatnessScalingDistance", Float, nullable=True
    )
    energy_flatness_power: Mapped[Optional[float]] = Column(
        "EnergyFlatnessPower", Float, nullable=True
    )
    restart_index: Mapped[Optional[int]] = Column(
        "RestartIndex", Integer, nullable=True
    )
    samples_per_batch: Mapped[Optional[int]] = Column(
        "SamplesPerBatch", Integer, nullable=True
    )
    number_of_histories_goal: Mapped[Optional[float]] = Column(
        "NumberOfHistoriesGoal", Float, nullable=True
    )
    uncertainty_goal: Mapped[Optional[float]] = Column(
        "UncertaintyGoal", Float, nullable=True
    )
    max_seconds: Mapped[Optional[float]] = Column("MaxSeconds", Float, nullable=True)
    completed_histories: Mapped[Optional[int]] = Column(
        "CompletedHistories", Integer, nullable=True
    )
    dose_uncertainty: Mapped[Optional[float]] = Column(
        "DoseUncertainty", Float, nullable=True
    )
    percent_done: Mapped[Optional[float]] = Column("PercentDone", Float, nullable=True)
    elapsed_seconds: Mapped[Optional[float]] = Column(
        "ElapsedSeconds", Float, nullable=True
    )
    elapsed_cpu_seconds: Mapped[Optional[float]] = Column(
        "ElapsedCpuSeconds", Float, nullable=True
    )
    cpu_percent_utilization: Mapped[Optional[float]] = Column(
        "CpuPercentUtilization", Float, nullable=True
    )
    print_batch_files: Mapped[Optional[int]] = Column(
        "PrintBatchFiles", Integer, nullable=True
    )
    print_data_file: Mapped[Optional[int]] = Column(
        "PrintDataFile", Integer, nullable=True
    )
    print_event_file: Mapped[Optional[int]] = Column(
        "PrintEventFile", Integer, nullable=True
    )
    print_track_file: Mapped[Optional[int]] = Column(
        "PrintTrackFile", Integer, nullable=True
    )
    statistics_outside_roi: Mapped[Optional[int]] = Column(
        "StatisticsOutsideRoi", Integer, nullable=True
    )

    # Parent relationship
    beam_id: Mapped[int] = Column("BeamID", Integer, ForeignKey("Beam.ID"))
    beam: Mapped["Beam"] = relationship("Beam", back_populates="dose_engine")

    def __init__(self, **kwargs):
        """
        Initialize a DoseEngine instance.

        Args:
            **kwargs: Keyword arguments used to initialize DoseEngine attributes.

        Relationships:
            beam (Beam): The parent Beam to which this DoseEngine belongs (many-to-one).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this dose engine.
        """
        return f"<DoseEngine(id={self.id}, beam='{self.beam.name if self.beam else 'None'}', type_name='{self.type_name}')>"
