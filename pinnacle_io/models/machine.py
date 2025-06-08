"""
SQLAlchemy model for Pinnacle machine data.
"""

from typing import List
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.machine_angle import CouchAngle, GantryAngle, CollimatorAngle
from pinnacle_io.models.machine_config import ConfigRV, TolTable
from pinnacle_io.models.machine_energy import PhotonEnergy, ElectronEnergy
from pinnacle_io.models.mlc import MultiLeaf
from pinnacle_io.models.pinnacle_base import PinnacleBase
from pinnacle_io.models.versioned_base import VersionedBase


class ElectronApplicator(PinnacleBase):
    """
    Represents an electron applicator for a Pinnacle treatment machine.
    """

    __tablename__ = "ElectronApplicator"

    # Primary key is inherited from PinnacleBase
    name: Mapped[str] = Column("Name", String, nullable=True)
    width: Mapped[float] = Column("Width", Float, nullable=True)
    length: Mapped[float] = Column("Length", Float, nullable=True)
    manufacturer_code: Mapped[str] = Column("ManufacturerCode", String, nullable=True)
    source_to_cutout_distance: Mapped[float] = Column("SourceToCutoutDistance", Float, nullable=True)
    cutout_thickness: Mapped[float] = Column("CutoutThickness", Float, nullable=True)
    cutout_material: Mapped[str] = Column("CutoutMaterial", String, nullable=True)
    cutout_mass_density: Mapped[float] = Column("CutoutMassDensity", Float, nullable=True)
    cutout_is_divergent: Mapped[int] = Column("CutoutIsDivergent", Integer, nullable=True)
    cutout_is_rectangular: Mapped[int] = Column("CutoutIsRectangular", Integer, nullable=True)
    cutout_half_x_outside: Mapped[float] = Column("CutoutHalfXOutside", Float, nullable=True)
    cutout_half_y_outside: Mapped[float] = Column("CutoutHalfYOutside", Float, nullable=True)

    # Foreign key relationship to Machine
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))
    machine: Mapped["Machine"] = relationship(
        "Machine", back_populates="electron_applicator_list"
    )

    def __repr__(self) -> str:
        return f"<ElectronApplicator(id={self.id}, name='{self.name}', length={self.length}, width={self.width})>"

    def __init__(self, **kwargs):
        """
        Initialize an ElectronApplicator instance.

        Args:
            **kwargs: Keyword arguments used to initialize ElectronApplicator attributes.

        Relationships:
            machine (Machine): The parent Machine to which this ElectronApplicator belongs (many-to-one).
        """
        super().__init__(**kwargs)


class Machine(VersionedBase):
    """
    Represents a Pinnacle treatment machine.

    Contains configuration data for a specific treatment machine including
    physical properties, jaw settings, and operational parameters.
    """

    __tablename__ = "Machine"

    # Primary key is inherited from PinnacleBase
    name: Mapped[str] = Column("Name", String, nullable=False)
    machine_type: Mapped[str] = Column("MachineType", String, nullable=True)
    version_timestamp: Mapped[str] = Column("VersionTimestamp", String, nullable=True)
    version_description: Mapped[str] = Column("VersionDescription", String, nullable=True)
    commissioned_by: Mapped[str] = Column("CommissionedBy", String, nullable=True)
    commission_version: Mapped[str] = Column("CommissionVersion", String, nullable=True)
    login_name: Mapped[str] = Column("LoginName", String, nullable=True)
    institution: Mapped[str] = Column("Institution", String, nullable=True)

    # Commission flags
    commissioned_for_photons: Mapped[int] = Column("CommissionedForPhotons", Integer, nullable=True)
    commissioned_for_electrons: Mapped[int] = Column(
        "CommissionedForElectrons", Integer, nullable=True
    )
    commissioned_for_mc_electrons: Mapped[int] = Column(
        "CommissionedForMCElectrons", Integer, nullable=True
    )
    commissioned_for_stereo: Mapped[int] = Column("CommissionedForStereo", Integer, nullable=True)
    commissioned_for_protons: Mapped[int] = Column("CommissionedForProtons", Integer, nullable=True)
    read_write_machine: Mapped[int] = Column("ReadWriteMachine", Integer, nullable=True)
    is_simulator: Mapped[int] = Column("IsSimulator", Integer, nullable=True)
    has_fixed_jaw: Mapped[int] = Column("HasFixedJaw", Integer, nullable=True)

    # Physical properties
    sad: Mapped[float] = Column("SAD", Float, nullable=True)
    source_to_flattening_filter_distance: Mapped[float] = Column(
        "SourceToFlatteningFilterDistance", Float, nullable=True
    )
    source_to_first_scattering_foil_distance: Mapped[float] = Column(
        "SourceToFirstScatteringFoilDistance", Float, nullable=True
    )
    source_to_last_scattering_foil_distance: Mapped[float] = Column(
        "SourceToLastScatteringFoilDistance", Float, nullable=True
    )
    source_to_left_right_jaw_distance: Mapped[float] = Column(
        "SourceToLeftRightJawDistance", Float, nullable=True
    )
    left_right_jaw_thickness: Mapped[float] = Column("LeftRightJawThickness", Float, nullable=True)
    source_to_top_bottom_jaw_distance: Mapped[float] = Column(
        "SourceToTopBottomJawDistance", Float, nullable=True
    )
    top_bottom_jaw_thickness: Mapped[float] = Column("TopBottomJawThickness", Float, nullable=True)
    source_to_block_tray_distance: Mapped[float] = Column(
        "SourceToBlockTrayDistance", Float, nullable=True
    )
    primary_collimation_angle: Mapped[float] = Column("PrimaryCollimationAngle", Float, nullable=True)

    # Left-Right jaw settings
    left_right_can_be_independent: Mapped[int] = Column(
        "LeftRightCanBeIndependent", Integer, nullable=True
    )
    left_right_minimum_position: Mapped[float] = Column(
        "LeftRightMinimumPosition", Float, nullable=True
    )
    left_right_maximum_position: Mapped[float] = Column(
        "LeftRightMaximumPosition", Float, nullable=True
    )
    proton_left_right_maximum_position: Mapped[float] = Column(
        "ProtonLeftRightMaximumPosition", Float, nullable=True
    )
    nominal_left_jaw_position: Mapped[float] = Column("NominalLeftJawPosition", Float, nullable=True)
    nominal_right_jaw_position: Mapped[float] = Column("NominalRightJawPosition", Float, nullable=True)
    fixed_left_right_jaw_position: Mapped[float] = Column(
        "FixedLeftRightJawPosition", Float, nullable=True
    )
    left_jaw_name: Mapped[str] = Column("LeftJawName", String, nullable=True)
    right_jaw_name: Mapped[str] = Column("RightJawName", String, nullable=True)
    left_right_name: Mapped[str] = Column("LeftRightName", String, nullable=True)
    left_right_decimal_places: Mapped[int] = Column("LeftRightDecimalPlaces", Integer, nullable=True)
    left_right_jaw_material: Mapped[str] = Column("LeftRightJawMaterial", String, nullable=True)
    left_right_mass_density: Mapped[float] = Column("LeftRightMassDensity", Float, nullable=True)

    # Top-Bottom jaw settings
    top_bottom_can_be_independent: Mapped[int] = Column(
        "TopBottomCanBeIndependent", Integer, nullable=True
    )
    top_bottom_minimum_position: Mapped[float] = Column(
        "TopBottomMinimumPosition", Float, nullable=True
    )
    top_bottom_maximum_position: Mapped[float] = Column(
        "TopBottomMaximumPosition", Float, nullable=True
    )
    proton_top_bottom_maximum_position: Mapped[float] = Column(
        "ProtonTopBottomMaximumPosition", Float, nullable=True
    )
    nominal_top_jaw_position: Mapped[float] = Column("NominalTopJawPosition", Float, nullable=True)
    nominal_bottom_jaw_position: Mapped[float] = Column(
        "NominalBottomJawPosition", Float, nullable=True
    )
    fixed_top_bottom_jaw_position: Mapped[float] = Column(
        "FixedTopBottomJawPosition", Float, nullable=True
    )
    top_jaw_name: Mapped[str] = Column("TopJawName", String, nullable=True)
    bottom_jaw_name: Mapped[str] = Column("BottomJawName", String, nullable=True)
    top_bottom_name: Mapped[str] = Column("TopBottomName", String, nullable=True)
    top_bottom_decimal_places: Mapped[int] = Column("TopBottomDecimalPlaces", Integer, nullable=True)
    top_bottom_jaw_material: Mapped[str] = Column("TopBottomJawMaterial", String, nullable=True)
    top_bottom_mass_density: Mapped[float] = Column("TopBottomMassDensity", Float, nullable=True)

    # Monitor unit settings
    cp_monitor_unit_decimal_places: Mapped[int] = Column(
        "CPMonitorUnitDecimalPlaces", Integer, nullable=True
    )
    monitor_unit_decimal_places: Mapped[int] = Column(
        "MonitorUnitDecimalPlaces", Integer, nullable=True
    )
    clip_beam_mu_to_max: Mapped[int] = Column("ClipBeamMUToMax", Integer, nullable=True)
    clip_high_dose_beam_mu_to_max: Mapped[int] = Column(
        "ClipHighDoseBeamMUToMax", Integer, nullable=True
    )
    monitor_unit_maximum: Mapped[int] = Column("MonitorUnitMaximum", Integer, nullable=True)
    monitor_unit_max_for_high_dose: Mapped[int] = Column(
        "MonitorUnitMaxForHighDose", Integer, nullable=True
    )
    monitor_unit_per_degree_maximum: Mapped[int] = Column(
        "MonitorUnitPerDegreeMaximum", Integer, nullable=True
    )

    # Delivery settings
    blocks_allowed: Mapped[int] = Column("BlocksAllowed", Integer, nullable=True)
    default_block_jaw_overlap: Mapped[int] = Column("DefaultBlockJawOverlap", Integer, nullable=True)
    has_mlc: Mapped[int] = Column("HasMLC", Integer, nullable=True)
    default_tolerance_table_name: Mapped[str] = Column(
        "DefaultToleranceTableName", String, nullable=True
    )
    max_jaw_speed: Mapped[float] = Column("MaxJawSpeed", Float, nullable=True)
    default_min_mu_per_seg: Mapped[int] = Column("DefaultMinMUPerSeg", Integer, nullable=True)
    dose_rate_continuously_variable: Mapped[int] = Column(
        "DoseRateContinuouslyVariable", Integer, nullable=True
    )
    dose_rate_constant: Mapped[int] = Column("DoseRateConstant", Integer, nullable=True)
    limit_gantry_acceleration: Mapped[int] = Column("LimitGantryAcceleration", Integer, nullable=True)
    gantry_acceleration_limit: Mapped[float] = Column("GantryAccelerationLimit", Float, nullable=True)
    not_for_dose_computation: Mapped[int] = Column("NotForDoseComputation", Integer, nullable=True)
    is_particle_machine: Mapped[int] = Column("IsParticleMachine", Integer, nullable=True)
    use_high_dose: Mapped[int] = Column("UseHighDose", Integer, nullable=True)

    # MU thresholds
    mu_threshold_static: Mapped[int] = Column("MUThresholdStatic", Integer, nullable=True)
    mu_threshold_arc: Mapped[int] = Column("MUThresholdArc", Integer, nullable=True)
    mu_threshold_conformal_arc: Mapped[int] = Column("MUThresholdConformalArc", Integer, nullable=True)
    mu_threshold_mlc: Mapped[int] = Column("MUThresholdMLC", Integer, nullable=True)
    mu_threshold_slid_win: Mapped[int] = Column("MUThresholdSlidWin", Integer, nullable=True)
    mu_threshold_dynamic_arc: Mapped[int] = Column("MUThresholdDynamicArc", Integer, nullable=True)
    mu_threshold_motorized_wedge: Mapped[int] = Column(
        "MUThresholdMotorizedWedge", Integer, nullable=True
    )

    # Relationships
    couch_angle: Mapped["CouchAngle"] = relationship(
        "CouchAngle",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == CouchAngle.machine_id",
    )
    gantry_angle: Mapped["GantryAngle"] = relationship(
        "GantryAngle",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == GantryAngle.machine_id",
    )
    collimator_angle: Mapped["CollimatorAngle"] = relationship(
        "CollimatorAngle",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == CollimatorAngle.machine_id",
    )
    config_rv: Mapped["ConfigRV"] = relationship(
        "ConfigRV",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
    )
    multi_leaf: Mapped["MultiLeaf"] = relationship(
        "MultiLeaf",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
    )
    electron_applicator_list: Mapped[List["ElectronApplicator"]] = relationship(
        "ElectronApplicator", back_populates="machine", cascade="all, delete-orphan"
    )
    tolerance_table_list: Mapped[List["TolTable"]] = relationship(
        "TolTable", back_populates="machine", cascade="all, delete-orphan"
    )
    photon_energy_list: Mapped[List["PhotonEnergy"]] = relationship(
        "PhotonEnergy",
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == PhotonEnergy.machine_id",
    )
    electron_energy_list: Mapped[List["ElectronEnergy"]] = relationship(
        "ElectronEnergy",
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == ElectronEnergy.machine_id",
    )

    def __repr__(self) -> str:
        return (
            f"<Machine(id={self.id}, name='{self.name}', type='{self.machine_type}')>"
        )

    def __init__(self, **kwargs):
        """
        Initialize a Machine instance.

        Args:
            **kwargs: Keyword arguments used to initialize Machine attributes.

        Relationships:
            electron_applicators (List[ElectronApplicator]): List of ElectronApplicator objects associated with this Machine (one-to-many).
            photon_energies (List[PhotonEnergy]): List of photon energy configurations (one-to-many).
            electron_energies (List[ElectronEnergy]): List of electron energy configurations (one-to-many).
            config_rv (ConfigRV): The associated ConfigRV object (one-to-one).
            tolerance_tables (List[TolTable]): List of TolTable objects (one-to-many).
            couch_angle (CouchAngle): The associated CouchAngle object (one-to-one).
            gantry_angle (GantryAngle): The associated GantryAngle object (one-to-one).
            collimator_angle (CollimatorAngle): The associated CollimatorAngle object (one-to-one).
            multi_leaf (MultiLeaf): The associated MultiLeaf object (one-to-one).
        """
        super().__init__(**kwargs)
