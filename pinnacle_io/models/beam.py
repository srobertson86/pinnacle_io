"""
SQLAlchemy model for Pinnacle Beam data.

This module provides the Beam data model for representing treatment beams in Pinnacle,
including all beam-specific parameters, relationships to control points, and associated
beam modifiers like wedges and MLCs.
"""

from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING, TypeVar, Any

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.control_point import ControlPoint
    from pinnacle_io.models.trial import Trial
    from pinnacle_io.models.dose import Dose, MaxDosePoint
    from pinnacle_io.models.compensator import Compensator
    from pinnacle_io.models.dose_engine import DoseEngine
    from pinnacle_io.models.monitor_unit_info import MonitorUnitInfo
    from pinnacle_io.models.cp_manager import CPManager

# Type variable for the Beam class to support better type hints
B = TypeVar('B', bound='Beam')


class Beam(PinnacleBase):
    """
    Model representing a treatment beam in Pinnacle.

    This class stores all beam-specific information including machine parameters,
    control points, and beam modifiers needed for treatment planning and delivery.
    It serves as the central model for beam data in the Pinnacle I/O system.

    Attributes:
        id (int): Primary key
        name (str): Name of the beam
        beam_number (int): Beam number in the treatment plan
        isocenter_name (str): Name of the isocenter used by this beam
        modality (str): Beam modality (e.g., "PHOTON", "ELECTRON")
        machine_energy_name (str): Name of the machine energy for this beam
        monitor_units (float): Number of monitor units for this beam
        
    Relationships:
        trial (Trial): Parent trial that this beam belongs to
        control_point_list (List[ControlPoint]): List of control points defining this beam
        cp_manager (CPManager): Manager for control point data
        dose (Dose): Dose information for this beam
        dose_engine (DoseEngine): Dose calculation engine settings
        max_dose_point (MaxDosePoint): Point of maximum dose
        monitor_unit_info (MonitorUnitInfo): Monitor unit calculation details
        compensator (Compensator): Associated compensator if any
    """

    __tablename__ = "Beam"

    # Identification and basic info
    name: Mapped[Optional[str]] = Column("Name", String, nullable=True)
    beam_number: Mapped[Optional[int]] = Column("BeamNumber", Integer, nullable=True)
    isocenter_name: Mapped[Optional[str]] = Column("IsocenterName", String, nullable=True)
    
    # Prescription and dose
    prescription_name: Mapped[Optional[str]] = Column("PrescriptionName", String, nullable=True)
    use_poi_for_prescription_point: Mapped[Optional[int]] = Column(
        "UsePoiForPrescriptionPoint", Integer, nullable=True
    )
    prescription_point_name: Mapped[str] = Column(
        "PrescriptionPointName", String, nullable=True
    )
    prescription_point_depth: Mapped[float] = Column(
        "PrescriptionPointDepth", Float, nullable=True
    )
    prescription_point_x_offset: Mapped[float] = Column(
        "PrescriptionPointXOffset", Float, nullable=True
    )
    prescription_point_y_offset: Mapped[float] = Column(
        "PrescriptionPointYOffset", Float, nullable=True
    )
    specify_dose_per_mu_at_prescription_point: Mapped[int] = Column(
        "SpecifyDosePerMuAtPrescriptionPoint", Integer, nullable=True
    )
    dose_per_mu_at_prescription_point: Mapped[float] = Column(
        "DosePerMuAtPrescriptionPoint", Float, nullable=True
    )
    machine_name_and_version: Mapped[str] = Column(
        "MachineNameAndVersion", String, nullable=True
    )
    modality: Mapped[str] = Column("Modality", String, nullable=True)
    machine_energy_name: Mapped[str] = Column(
        "MachineEnergyName", String, nullable=True
    )
    desired_localizer_name: Mapped[str] = Column(
        "DesiredLocalizerName", String, nullable=True
    )
    actual_localizer_name: Mapped[str] = Column(
        "ActualLocalizerName", String, nullable=True
    )
    display_laser_motion: Mapped[str] = Column(
        "DisplayLaserMotion", String, nullable=True
    )
    set_beam_type: Mapped[str] = Column("SetBeamType", String, nullable=True)
    prev_beam_type: Mapped[str] = Column("PrevBeamType", String, nullable=True)
    computation_version: Mapped[str] = Column(
        "ComputationVersion", String, nullable=True
    )
    extend_past_target: Mapped[float] = Column("ExtendPastTarget", Float, nullable=True)
    extend_block_plane_past_target: Mapped[float] = Column(
        "ExtendBlockPlanePastTarget", Float, nullable=True
    )
    extend_arc_past_target: Mapped[float] = Column(
        "ExtendArcPastTarget", Float, nullable=True
    )
    bev_rotation_angle: Mapped[float] = Column("BevRotationAngle", Float, nullable=True)
    bev_is_parallel: Mapped[int] = Column("BevIsParallel", Integer, nullable=True)
    rotation_indicator_offset: Mapped[float] = Column(
        "RotationIndicatorOffset", Float, nullable=True
    )
    imrt_filter: Mapped[str] = Column("ImrtFilter", String, nullable=True)
    imrt_wedge: Mapped[str] = Column("ImrtWedge", String, nullable=True)
    imrt_direction: Mapped[str] = Column("ImrtDirection", String, nullable=True)
    imrt_parameter_type: Mapped[str] = Column(
        "ImrtParameterType", String, nullable=True
    )
    prev_imrt_parameter_type: Mapped[str] = Column(
        "PrevImrtParameterType", String, nullable=True
    )
    philips_mlc_treatment: Mapped[str] = Column(
        "PhilipsMlcTreatment", String, nullable=True
    )
    philips_mlc_beam_number: Mapped[str] = Column(
        "PhilipsMlcBeamNumber", String, nullable=True
    )
    toshiba_mlc_plan_number: Mapped[str] = Column(
        "ToshibaMlcPlanNumber", String, nullable=True
    )
    toshiba_mlc_beam_number_string: Mapped[str] = Column(
        "ToshibaMlcBeamNumberString", String, nullable=True
    )
    use_mlc: Mapped[int] = Column("UseMlc", Integer, nullable=True)
    clip_mlc_display: Mapped[int] = Column("ClipMlcDisplay", Integer, nullable=True)
    solid_mlc_display: Mapped[int] = Column("SolidMlcDisplay", Integer, nullable=True)
    dynamic_blocks: Mapped[int] = Column("DynamicBlocks", Integer, nullable=True)
    display_2d: Mapped[int] = Column("Display2d", Integer, nullable=True)
    display_3d: Mapped[int] = Column("Display3d", Integer, nullable=True)
    circular_field_diameter: Mapped[float] = Column(
        "CircularFieldDiameter", Float, nullable=True
    )
    electron_applicator_name: Mapped[str] = Column(
        "ElectronApplicatorName", String, nullable=True
    )
    ssd: Mapped[float] = Column("Ssd", Float, nullable=True)
    avg_ssd: Mapped[float] = Column("AvgSsd", Float, nullable=True)
    ssd_valid: Mapped[int] = Column("SsdValid", Integer, nullable=True)
    left_auto_surround_margin: Mapped[float] = Column(
        "LeftAutoSurroundMargin", Float, nullable=True
    )
    right_auto_surround_margin: Mapped[float] = Column(
        "RightAutoSurroundMargin", Float, nullable=True
    )
    top_auto_surround_margin: Mapped[float] = Column(
        "TopAutoSurroundMargin", Float, nullable=True
    )
    bottom_auto_surround_margin: Mapped[float] = Column(
        "BottomAutoSurroundMargin", Float, nullable=True
    )
    auto_surround: Mapped[int] = Column("AutoSurround", Integer, nullable=True)
    blocking_mask_pixel_size: Mapped[float] = Column(
        "BlockingMaskPixelSize", Float, nullable=True
    )
    blocking_mask_cutoff_area: Mapped[float] = Column(
        "BlockingMaskCutoffArea", Float, nullable=True
    )
    block_and_tray_factor: Mapped[float] = Column(
        "BlockAndTrayFactor", Float, nullable=True
    )
    tray_number: Mapped[str] = Column("TrayNumber", String, nullable=True)
    block_export_name: Mapped[str] = Column("BlockExportName", String, nullable=True)
    block_cutter_format: Mapped[str] = Column(
        "BlockCutterFormat", String, nullable=True
    )
    block_jaw_overlap: Mapped[int] = Column("BlockJawOverlap", Integer, nullable=True)
    tray_factor: Mapped[float] = Column("TrayFactor", Float, nullable=True)
    compensator_scale_factor: Mapped[float] = Column(
        "CompensatorScaleFactor", Float, nullable=True
    )
    degrees_between_subbeams_for_dose_calc: Mapped[float] = Column(
        "DegreesBetweenSubbeamsForDoseCalc", Float, nullable=True
    )
    irreg_prescription_point_name: Mapped[str] = Column(
        "IrregPrescriptionPointName", String, nullable=True
    )
    irreg_specify_monitor_units: Mapped[int] = Column(
        "IrregSpecifyMonitorUnits", Integer, nullable=True
    )
    irreg_point_prescription_dose: Mapped[float] = Column(
        "IrregPointPrescriptionDose", Float, nullable=True
    )
    irreg_point_monitor_units: Mapped[float] = Column(
        "IrregPointMonitorUnits", Float, nullable=True
    )
    irreg_point_actual_monitor_units: Mapped[float] = Column(
        "IrregPointActualMonitorUnits", Float, nullable=True
    )
    irreg_point_prescribe_overall: Mapped[int] = Column(
        "IrregPointPrescribeOverall", Integer, nullable=True
    )
    irreg_point_number_of_fractions: Mapped[int] = Column(
        "IrregPointNumberOfFractions", Integer, nullable=True
    )
    photon_model_description: Mapped[str] = Column(
        "PhotonModelDescription", String, nullable=True
    )
    avg_tar: Mapped[float] = Column("AvgTar", Float, nullable=True)
    stereo_dose_per_mu_lookup: Mapped[int] = Column(
        "StereoDosePerMuLookup", Integer, nullable=True
    )
    stereo_dose_di_value: Mapped[float] = Column(
        "StereoDoseDiValue", Float, nullable=True
    )
    blocks_are_locked: Mapped[int] = Column("BlocksAreLocked", Integer, nullable=True)
    is_proton_beam_locked: Mapped[int] = Column(
        "IsProtonBeamLocked", Integer, nullable=True
    )
    rely_on_bolus_names: Mapped[str] = Column("RelyOnBolusNames", String, nullable=True)
    dose_volume: Mapped[str] = Column("DoseVolume", String, nullable=True)
    dose_var_volume: Mapped[str] = Column("DoseVarVolume", String, nullable=True)
    weight: Mapped[float] = Column("Weight", Float, nullable=True)
    is_weight_locked: Mapped[int] = Column("IsWeightLocked", Integer, nullable=True)
    monitor_units_valid: Mapped[int] = Column(
        "MonitorUnitsValid", Integer, nullable=True
    )
    monitor_units_approximate: Mapped[int] = Column(
        "MonitorUnitsApproximate", Integer, nullable=True
    )
    field_id: Mapped[str] = Column("FieldId", String, nullable=True)
    speed_up_collimator: Mapped[int] = Column(
        "SpeedUpCollimator", Integer, nullable=True
    )
    speed_up_virt_flouro: Mapped[int] = Column(
        "SpeedUpVirtFlouro", Integer, nullable=True
    )
    display_max_leaf_motion: Mapped[int] = Column(
        "DisplayMaxLeafMotion", Integer, nullable=True
    )
    beam_was_split: Mapped[int] = Column("BeamWasSplit", Integer, nullable=True)
    dose_rate: Mapped[float] = Column("DoseRate", Float, nullable=True)
    is_copy_oppose_allowed: Mapped[int] = Column(
        "IsCopyOpposeAllowed", Integer, nullable=True
    )
    vertical_jaw_sync: Mapped[int] = Column("VerticalJawSync", Integer, nullable=True)
    scenario_dose_volume0: Mapped[str] = Column(
        "ScenarioDoseVolume0", String, nullable=True
    )
    scenario_dose_volume1: Mapped[str] = Column(
        "ScenarioDoseVolume1", String, nullable=True
    )
    scenario_dose_volume2: Mapped[str] = Column(
        "ScenarioDoseVolume2", String, nullable=True
    )
    scenario_dose_volume3: Mapped[str] = Column(
        "ScenarioDoseVolume3", String, nullable=True
    )
    scenario_dose_volume4: Mapped[str] = Column(
        "ScenarioDoseVolume4", String, nullable=True
    )
    scenario_dose_volume5: Mapped[str] = Column(
        "ScenarioDoseVolume5", String, nullable=True
    )
    scenario_dose_volume6: Mapped[str] = Column(
        "ScenarioDoseVolume6", String, nullable=True
    )
    scenario_dose_volume7: Mapped[str] = Column(
        "ScenarioDoseVolume7", String, nullable=True
    )
    deserialization_completed: Mapped[int] = Column(
        "DeserializationCompleted", Integer, nullable=True
    )

    # Derived fields (not in the Pinnacle plan.Trial file but still useful)
    _monitor_units: Mapped[float] = Column(
        "MonitorUnits", Float, nullable=True, default=0.0
    )
    
    # Relationships
    trial_id: Mapped[Optional[int]] = Column("TrialID", Integer, ForeignKey("Trial.ID"))
    trial: Mapped[Optional["Trial"]] = relationship(
        "Trial", 
        back_populates="beam_list"
    )
    
    # One-to-many relationships (parent side)
    control_point_list: Mapped[List["ControlPoint"]] = relationship(
        "ControlPoint", 
        back_populates="beam", 
        cascade="all, delete-orphan"
    )
    
    # One-to-one relationships
    compensator: Mapped[Optional["Compensator"]] = relationship(
        "Compensator",
        back_populates="beam",
        uselist=False,
        cascade="all, delete-orphan"
    )
    cp_manager: Mapped[Optional["CPManager"]] = relationship(
        "CPManager", 
        back_populates="beam", 
        uselist=False, 
        cascade="all, delete-orphan"
    )
    dose: Mapped[Optional["Dose"]] = relationship(
        "Dose", 
        back_populates="beam", 
        uselist=False, 
        cascade="all, delete-orphan"
    )
    dose_engine: Mapped[Optional["DoseEngine"]] = relationship(
        "DoseEngine", 
        back_populates="beam", 
        uselist=False, 
        cascade="all, delete-orphan"
    )
    max_dose_point: Mapped[Optional["MaxDosePoint"]] = relationship(
        "MaxDosePoint", 
        back_populates="beam", 
        uselist=False,
    )
    monitor_unit_info: Mapped[Optional["MonitorUnitInfo"]] = relationship(
        "MonitorUnitInfo",
        back_populates="beam",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a new Beam instance.

        Args:
            **kwargs: Arbitrary keyword arguments for setting attributes.
                Common attributes include:
                - name: Name of the beam
                - beam_number: Number of the beam in the plan
                - isocenter_name: Name of the isocenter
                - modality: Beam modality (e.g., "PHOTON", "ELECTRON")
                - machine_energy_name: Name of the machine energy
                - monitor_units: Number of monitor units
        
        Note:
            This constructor is typically called by SQLAlchemy during object loading.
            For creating new beams programmatically, consider using the appropriate
            factory methods or the Trial.add_beam() method.
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this beam.
        
        Returns:
            str: A string containing the beam's ID, number, name, and modality.
        """
        return f"<Beam(id={self.id}, beam_number={self.beam_number}, name='{self.name}')>"

    def add_control_point(self, control_point: "ControlPoint") -> None:
        """
        Add a control point to this beam.

        Args:
            control_point: Control point to add.
        """
        if self.cp_manager:
            self.cp_manager.control_point_list.append(control_point)

    def get_control_point(self, index: int) -> Optional["ControlPoint"]:
        """
        Get a control point by its index.

        Args:
            index: Control point index to retrieve.

        Returns:
            Control point with the specified index, or None if not found.
        """
        if not self.cp_manager:
            return None

        for cp in self.cp_manager.control_point_list:
            if cp.index == index:
                return cp

        return None

    def is_arc(self) -> bool:
        """
        Check if this beam is an arc.

        Returns:
            True if this beam is an arc, False otherwise.
        """
        if not self.cp_manager:
            return False

        if len(self.cp_manager.control_point_list) < 2:
            return False

        first_cp = self.cp_manager.control_point_list[0]
        second_cp = self.cp_manager.control_point_list[1]

        return abs(first_cp.gantry - second_cp.gantry) > 1.0

    @property
    def is_cw(self) -> Optional[bool]:
        """
        Check if this beam is a clockwise arc.

        Returns:
            None if this beam is not an arc, True if this beam is a clockwise arc, False otherwise.
        """
        if self.is_arc:
            return not self.cp_manager.gantry_is_ccw
        return None

    @property
    def is_ccw(self) -> Optional[bool]:
        """
        Check if this beam is a counter-clockwise arc.

        Returns:
            None if this beam is not an arc, True if this beam is a counter-clockwise arc, False otherwise.
        """
        if self.is_arc:
            return self.cp_manager.gantry_is_ccw
        return None

    def has_wedge(self) -> bool:
        """
        Check if this beam has a wedge.

        Returns:
            True if this beam has a wedge, False otherwise.
        """
        if not self.cp_manager:
            return False

        for cp in self.cp_manager.control_point_list:
            if cp.wedge_context and cp.wedge_context.wedge_name:
                return True

        return False

    def has_mlc(self) -> bool:
        """
        Check if this beam has MLC positions.

        Returns:
            True if any control point has MLC positions, False otherwise.
        """
        if not self.cp_manager:
            return False

        for cp in self.cp_manager.control_point_list:
            if cp.mlc_leaf_positions and cp.mlc_leaf_positions.number_of_points > 0:
                return True

        return False

    def compute_monitor_units(self, pdd: float) -> float:
        """
        Compute the monitor units for this beam.

        Args:
            pdd: Percent depth dose at 10cm for the current machine and beam energy

        Returns:
            Computed monitor units.
        """
        if self.monitor_unit_info is None:
            raise ValueError("Monitor unit information is not available.")

        # From Pinnacle:
        # Dose at Ref Pt/Fraction = MU * ND * OFc * TTF * (D/MU)cal
        # where:
        #    MU = monitor units
        #    ND = normalization dose at reference point
        #    OFc = collimator output factor
        #    TTF = total transmission fraction. Typically 1.000
        #    (D/MU)cal = dose per monitor unit at calibration depth (e.g., PDD10)
        # TODO: Simplify using the MU Info Normalized Dose. See PyMedPhys
        beam_dose = self.monitor_unit_info.prescription_dose
        norm_dose = self.monitor_unit_info.normalized_dose
        output_factor = self.monitor_unit_info.collimator_output_factor
        transmission_factor = self.monitor_unit_info.total_transmission_fraction
        return beam_dose / (norm_dose * output_factor * transmission_factor * pdd)

    @property
    def dose_volume_file(self) -> str:
        """
        Get the dose volume file name.

        Returns:
            Dose volume file name, e.g., plan.Trial.binary.001
        """
        return f"plan.Trial.binary.{self.dose_volume.split(':')[1].zfill(3)}"
