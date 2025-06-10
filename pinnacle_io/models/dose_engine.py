"""
SQLAlchemy model for Pinnacle Dose Engine data.

This module provides the Dose Engine data models for representing dose engine configuration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Dict

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship, Session

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.beam import Beam


class DoseEngine(PinnacleBase):
    """
    Model representing a dose engine configuration in the Pinnacle treatment planning system.

    This class stores all dose engine-specific information needed for DICOM conversion,
    including type, convolution settings, and statistics tracking. Each DoseEngine instance
    is associated with exactly one Beam.

    Attributes:
        id (int): Primary key (inherited from PinnacleBase)
        type_name (Optional[str]): Type of the dose engine
        convolve_homogeneous (Optional[int]): Flag for homogeneous convolution
        fluence_homogeneous (Optional[int]): Flag for homogeneous fluence
        flat_water_phantom (Optional[int]): Flag for flat water phantom
        flat_homogeneous (Optional[int]): Flag for flat homogeneous
        electron_homogeneous (Optional[int]): Flag for electron homogeneous
        fluence_type (Optional[str]): Type of fluence calculation
        long_step_tuning_factor (Optional[float]): Tuning factor for long steps
        short_step_length (Optional[float]): Length of short steps
        number_of_short_steps (Optional[int]): Count of short steps
        split_fluence_field_size_cutoff (Optional[int]): Field size cutoff for split fluence
        azimuthal_bin_count (Optional[int]): Number of azimuthal bins
        zenith_bin_count (Optional[int]): Number of zenith bins
        cum_kernel_radial_bin_width (Optional[float]): Radial bin width for cumulative kernel
        siddon_corner_cutoff (Optional[float]): Cutoff for Siddon corner detection
        nrd_bin_width (Optional[float]): NRD bin width
        allowable_dose_diff (Optional[float]): Allowed dose difference
        high_fluence_cutoff (Optional[float]): High fluence cutoff value
        low_first_deriv_cutoff (Optional[float]): Low first derivative cutoff
        low_second_deriv_cutoff (Optional[float]): Low second derivative cutoff
        high_first_deriv_cutoff (Optional[float]): High first derivative cutoff
        high_second_deriv_cutoff (Optional[float]): High second derivative cutoff
        adaptive_levels (Optional[int]): Number of adaptive levels
        energy_flatness_cutoff (Optional[float]): Energy flatness cutoff
        energy_flatness_minimum_distance (Optional[float]): Minimum distance for energy flatness
        energy_flatness_scaling_distance (Optional[float]): Scaling distance for energy flatness
        energy_flatness_power (Optional[float]): Power for energy flatness calculation
        restart_index (Optional[int]): Index for restarting calculations
        samples_per_batch (Optional[int]): Number of samples per batch
        number_of_histories_goal (Optional[float]): Target number of histories
        uncertainty_goal (Optional[float]): Target uncertainty level
        max_seconds (Optional[float]): Maximum calculation time in seconds
        completed_histories (Optional[int]): Number of completed histories
        dose_uncertainty (Optional[float]): Current dose uncertainty
        percent_done (Optional[float]): Completion percentage
        elapsed_seconds (Optional[float]): Elapsed time in seconds
        elapsed_cpu_seconds (Optional[float]): CPU time used in seconds
        cpu_percent_utilization (Optional[float]): CPU utilization percentage
        print_batch_files (Optional[int]): Flag for printing batch files
        print_data_file (Optional[int]): Flag for printing data files
        print_event_file (Optional[int]): Flag for printing event files
        print_track_file (Optional[int]): Flag for printing track files
        statistics_outside_roi (Optional[int]): Flag for including statistics outside ROI
        
    Relationships:
        beam (Beam): The parent Beam to which this DoseEngine belongs (many-to-one).
                     Back-populates to Beam.dose_engine.
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

    # Parent relationship with back-population to Beam.dose_engine
    beam_id: Mapped[int] = Column("BeamID", Integer, ForeignKey("Beam.ID"), nullable=False)
    beam: Mapped["Beam"] = relationship(
        "Beam", 
        back_populates="dose_engine",
        single_parent=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a DoseEngine instance with the given parameters.

        Args:
            **kwargs: Keyword arguments corresponding to model attributes.
                Supported keyword arguments include all column names as attributes and:
                - beam (Beam): The parent Beam to which this DoseEngine belongs.
        """
        # Initialize parent class with all keyword arguments
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this dose engine.

        Returns:
            str: A string representation in the format:
                <DoseEngine(id=X, beam='beam_name', type_name='type')>
        """
        beam_name = getattr(getattr(self, 'beam', ''), 'name', '')
        return (
            f"<DoseEngine(id={self.id}, "
            f"beam='{beam_name}', "
            f"type_name='{self.type_name}')>"
        )
    