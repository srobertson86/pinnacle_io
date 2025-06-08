"""
SQLAlchemy model for Pinnacle Trial data.

This module provides the Trial model for representing treatment trial details.
"""

from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from pinnacle_io.models.versioned_base import VersionedBase

if TYPE_CHECKING:
    from pinnacle_io.models.beam import Beam
    from pinnacle_io.models.dose import Dose, MaxDosePoint
    from pinnacle_io.models.dose_grid import DoseGrid

    # from pinnacle_io.models.patient_setup import PatientSetup
    from pinnacle_io.models.plan import Plan
    from pinnacle_io.models.patient_setup import PatientRepresentation
    from pinnacle_io.models.prescription import Prescription


class Trial(VersionedBase):
    """
    Model representing a treatment trial.

    This class stores all trial-specific information needed for DICOM conversion,
    including beams, prescriptions, and approval status. Note that a DICOM plan
    actually corresponds to a Pinnacle Trial, and that a single Pinnacle plan
    can contain multiple trials.
    """

    __tablename__ = "Trial"

    # Primary key is inherited from VersionedBase
    trial_id: Mapped[int] = Column("TrialID", Integer, nullable=True)
    name: Mapped[str] = Column("TrialName", String, nullable=True)
    dose_start_slice: Mapped[int] = Column("DoseStartSlice", Integer, nullable=True)
    dose_end_slice: Mapped[int] = Column("DoseEndSlice", Integer, nullable=True)
    scenario_dose_grid_res: Mapped[float] = Column(
        "ScenarioDoseGridRes", Float, nullable=True
    )
    scenario_dose_grid_dim_x: Mapped[int] = Column(
        "ScenarioDoseGridDimX", Integer, nullable=True
    )
    scenario_dose_grid_dim_y: Mapped[int] = Column(
        "ScenarioDoseGridDimY", Integer, nullable=True
    )
    scenario_dose_grid_dim_z: Mapped[int] = Column(
        "ScenarioDoseGridDimZ", Integer, nullable=True
    )
    suppress_dose_grid_summing: Mapped[int] = Column(
        "SuppressDoseGridSumming", Integer, nullable=True
    )
    trial_used_for_dose_display_only: Mapped[int] = Column(
        "TrialUsedForDoseDisplayOnly", Integer, nullable=True
    )
    record_dose_data: Mapped[str] = Column("RecordDoseData", String, nullable=True)
    fluence_grid_resolution: Mapped[float] = Column(
        "FluenceGridResolution", Float, nullable=True
    )
    fluence_grid_matches_dose_grid: Mapped[int] = Column(
        "FluenceGridMatchesDoseGrid", Integer, nullable=True
    )
    source_to_film_distance: Mapped[float] = Column(
        "SourceToFilmDistance", Float, nullable=True
    )
    screen_to_printer_zoom_factor: Mapped[float] = Column(
        "ScreenToPrinterZoomFactor", Float, nullable=True
    )
    mc_max_seconds: Mapped[int] = Column("MCMaxSeconds", Integer, nullable=True)
    mc_global_uncertainty_type: Mapped[str] = Column(
        "MCGlobalUncertaintyType", String, nullable=True
    )
    mc_statistics_threshold: Mapped[int] = Column(
        "MCStatisticsThreshold", Integer, nullable=True
    )
    mc_uncertainty_goal: Mapped[int] = Column("MCUncertaintyGoal", Integer, nullable=True)
    remove_couch_from_scan: Mapped[int] = Column(
        "RemoveCouchFromScan", Integer, nullable=True
    )
    couch_removal_y_coordinate: Mapped[float] = Column(
        "CouchRemovalYCoordinate", Float, nullable=True
    )
    display_2d_couch_position: Mapped[int] = Column(
        "Display2DCouchPosition", Integer, nullable=True
    )
    display_3d_couch_position: Mapped[int] = Column(
        "Display3DCouchPosition", Integer, nullable=True
    )
    couch_display_color: Mapped[str] = Column("CouchDisplayColor", String, nullable=True)
    recompute_density: Mapped[int] = Column("RecomputeDensity", Integer, nullable=True)
    physics_plan: Mapped[int] = Column("PhysicsPlan", Integer, nullable=True)
    compute_relative_dose: Mapped[int] = Column(
        "ComputeRelativeDose", Integer, nullable=True
    )
    relative_dose_norm_point_name: Mapped[str] = Column(
        "RelativeDoseNormPointName", String, nullable=True
    )
    relative_dose_norm_value: Mapped[float] = Column(
        "RelativeDoseNormValue", Float, nullable=True
    )
    relative_dose_norm_valid: Mapped[int] = Column(
        "RelativeDoseNormValid", Integer, nullable=True
    )
    relative_dose_reference_field_name: Mapped[str] = Column(
        "RelativeDoseReferenceFieldName", String, nullable=True
    )
    last_relative_dose_reference_field: Mapped[str] = Column(
        "LastRelativeDoseReferenceField", String, nullable=True
    )
    relative_dose_computation_status: Mapped[str] = Column(
        "RelativeDoseComputationStatus", String, nullable=True
    )
    isodose_norm_point_name: Mapped[str] = Column(
        "IsodoseNormPointName", String, nullable=True
    )
    use_actual_patient_for_irreg: Mapped[int] = Column(
        "UseActualPatientForIrreg", Integer, nullable=True
    )
    print_subbeams: Mapped[int] = Column("PrintSubbeams", Integer, nullable=True)
    print_pois: Mapped[int] = Column("PrintPOIs", Integer, nullable=True)
    print_rois: Mapped[int] = Column("PrintROIs", Integer, nullable=True)
    print_brachy_by_catheter: Mapped[int] = Column(
        "PrintBrachyByCatheter", Integer, nullable=True
    )
    print_brachy_by_group: Mapped[int] = Column(
        "PrintBrachyByGroup", Integer, nullable=True
    )
    print_mlc: Mapped[int] = Column("PrintMLC", Integer, nullable=True)
    print_mlc_irreg: Mapped[int] = Column("PrintMLCIrreg", Integer, nullable=True)
    use_trial_for_treatment: Mapped[int] = Column(
        "UseTrialForTreatment", Integer, nullable=True
    )
    use_coord_ref_point: Mapped[int] = Column("UseCoordRefPoint", Integer, nullable=True)
    course_id: Mapped[int] = Column("CourseID", Integer, nullable=True)
    tolerance_table: Mapped[int] = Column("ToleranceTable", Integer, nullable=True)
    always_display_2d_couch_position: Mapped[int] = Column(
        "AlwaysDisplay2DCouchPosition", Integer, nullable=True
    )
    always_display_3d_couch_position: Mapped[int] = Column(
        "AlwaysDisplay3DCouchPosition", Integer, nullable=True
    )
    export_planar_dose_ascii: Mapped[int] = Column(
        "ExportPlanarDoseASCII", Integer, nullable=True
    )
    print_imrt_summary: Mapped[int] = Column("PrintIMRTSummary", Integer, nullable=True)
    print_impt_summary: Mapped[int] = Column("PrintIMPTSummary", Integer, nullable=True)
    multiple_machines: Mapped[int] = Column("MultipleMachines", Integer, nullable=True)
    check_ct_to_density_extension: Mapped[int] = Column(
        "CheckCTToDensityExtension", Integer, nullable=True
    )
    series_number: Mapped[int] = Column("SeriesNumber", Integer, nullable=True)
    series_description: Mapped[str] = Column("SeriesDescription", String, nullable=True)
    ct_scanner: Mapped[str] = Column("CTScanner", String, nullable=True)
    has_dose: Mapped[int] = Column("HasDose", Integer, nullable=True)
    include_dicom_coord_in_report: Mapped[int] = Column(
        "IncludeDicomCoordInReport", Integer, nullable=True
    )
    include_shifts_from_first_in_report: Mapped[int] = Column(
        "IncludeShiftsFromFirstInReport", Integer, nullable=True
    )
    is_absolute_laser_mode: Mapped[int] = Column(
        "IsAbsoluteLaserMode", Integer, nullable=True
    )
    last_laser_transmission_mode: Mapped[str] = Column(
        "LastLaserTransmissionMode", String, nullable=True
    )
    ap_error: Mapped[int] = Column("APError", Integer, nullable=True)
    lr_error: Mapped[int] = Column("LRError", Integer, nullable=True)
    is_error: Mapped[int] = Column("IsError", Integer, nullable=True)
    depth_error: Mapped[int] = Column("DepthError", Integer, nullable=True)
    fluence_dose_spread: Mapped[int] = Column("FluenceDoseSpread", Integer, nullable=True)
    single_gaussian_dose_spread: Mapped[int] = Column(
        "SingleGaussianDoseSpread", Integer, nullable=True
    )
    double_gaussian_dose_spread: Mapped[int] = Column(
        "DoubleGaussianDoseSpread", Integer, nullable=True
    )
    nuclear_dose_spread: Mapped[int] = Column("NuclearDoseSpread", Integer, nullable=True)
    min_dose_threshold: Mapped[float] = Column("MinDoseThreshold", Float, nullable=True)
    is_ro: Mapped[int] = Column("IsRO", Integer, nullable=True)
    ant_post_weight: Mapped[int] = Column("AntPostWeight", Integer, nullable=True)
    lateral_weight: Mapped[int] = Column("LateralWeight", Integer, nullable=True)
    inf_sup_weight: Mapped[int] = Column("InfSupWeight", Integer, nullable=True)
    depth_weight: Mapped[int] = Column("DepthWeight", Integer, nullable=True)
    nominal_weight: Mapped[int] = Column("NominalWeight", Integer, nullable=True)

    # Parent relationship
    plan_id: Mapped[int] = Column("PlanID", Integer, ForeignKey("Plan.ID"))
    plan: Mapped["Plan"] = relationship("Plan", back_populates="trial_list")

    # Child relationships
    beam_list: Mapped[List["Beam"]] = relationship(
        "Beam", back_populates="trial", cascade="all, delete-orphan"
    )
    dose: Mapped[Optional["Dose"]] = relationship(
        "Dose",
        back_populates="trial",
        uselist=False,
        cascade="all, delete-orphan",
        foreign_keys="Dose.trial_id",
    )
    dose_grid: Mapped["DoseGrid"] = relationship(
        "DoseGrid", uselist=False, back_populates="trial", cascade="all, delete-orphan"
    )
    max_dose_point: Mapped["MaxDosePoint"] = relationship(
        "MaxDosePoint",
        uselist=False,
        back_populates="trial",
        cascade="all, delete-orphan",
    )
    # _patient_position: Mapped["PatientSetup"] = relationship("PatientSetup", uselist=False, back_populates="trial", cascade="all, delete-orphan")
    patient_representation: Mapped["PatientRepresentation"] = relationship(
        "PatientRepresentation",
        uselist=False,
        back_populates="trial",
        cascade="all, delete-orphan",
    )
    prescription_list: Mapped[List["Prescription"]] = relationship(
        "Prescription", back_populates="trial", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        """
        Initialize a Trial instance.

        Args:
            **kwargs: Keyword arguments used to initialize Trial attributes.

        Relationships:
            plan (Plan): The parent Plan to which this Trial belongs (many-to-one).
            beams (List[Beam]): List of Beam objects associated with this Trial (one-to-many).
            dose (Dose): Dose object associated with this Trial (one-to-one).
            dose_grid (DoseGrid): DoseGrid object associated with this Trial (one-to-one).
            max_dose_point (MaxDosePoint): MaxDosePoint object associated with this Trial (one-to-one).
            patient_representation (PatientRepresentation): PatientRepresentation details for this Trial (one-to-one).
            prescriptions (List[Prescription]): List of Prescription objects associated with this Trial (one-to-many).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<Trial(id={self.id}, trial_id={self.trial_id}, trial_name='{self.name}')>"

    def get_beam_by_number(self, beam_number: int) -> Optional["Beam"]:
        """
        Get a beam by its number.

        Args:
            beam_number: Beam number to retrieve.

        Returns:
            Beam with the specified number, or None if not found.
        """
        for beam in self.beam_list:
            if beam.beam_number == beam_number:
                return beam
        return None

    def get_beam_by_name(self, beam_name: str) -> Optional["Beam"]:
        """
        Get a beam by its name.

        Args:
            beam_name: Beam name to retrieve.

        Returns:
            Beam with the specified name, or None if not found.
        """
        for beam in self.beam_list:
            if beam.name == beam_name:
                return beam
        return None

    @property
    def total_monitor_units(self) -> float:
        """
        Get the total monitor units for all beams in this trial.

        Returns:
            Total monitor units.
        """
        return sum(beam.compute_monitor_units() for beam in self.beam_list)
