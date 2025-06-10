"""
SQLAlchemy model for Pinnacle machine data.

This module provides comprehensive models for representing treatment machines
and their associated components in the Pinnacle treatment planning system.
"""

from typing import List, Optional
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

    An electron applicator is a device used to shape and collimate electron beams
    for radiation therapy treatments. This class stores all the physical and
    geometric properties of the applicator including dimensions, materials,
    and cutout specifications.

    Attributes:
        id (int): Primary key inherited from PinnacleBase
        name (str): Display name of the applicator (e.g., "10x10", "15x15")
        width (float): Width of the applicator opening in cm
        length (float): Length of the applicator opening in cm
        manufacturer_code (str): Manufacturer's product code for the applicator
        source_to_cutout_distance (float): Distance from electron source to cutout in cm
        cutout_thickness (float): Thickness of the cutout material in cm
        cutout_material (str): Material composition of the cutout (e.g., "Cerrobend")
        cutout_mass_density (float): Mass density of cutout material in g/cm³
        cutout_is_divergent (int): Flag indicating if cutout is divergent (1) or parallel (0)
        cutout_is_rectangular (int): Flag indicating if cutout is rectangular (1) or circular (0)
        cutout_half_x_outside (float): Half-width of cutout exterior dimension in cm
        cutout_half_y_outside (float): Half-height of cutout exterior dimension in cm
        machine_id (int): Foreign key to the parent Machine

    Relationships:
        machine (Machine): The parent Machine to which this applicator belongs (many-to-one)

    Example:
        >>> applicator = ElectronApplicator(
        ...     name="10x10",
        ...     width=10.0,
        ...     length=10.0,
        ...     manufacturer_code="10X10",
        ...     cutout_material="Cerrobend",
        ...     machine_id=1
        ... )
    """

    __tablename__ = "ElectronApplicator"

    # Primary key is inherited from PinnacleBase
    name: Mapped[Optional[str]] = Column("Name", String, nullable=True)
    width: Mapped[Optional[float]] = Column("Width", Float, nullable=True)
    length: Mapped[Optional[float]] = Column("Length", Float, nullable=True)
    manufacturer_code: Mapped[Optional[str]] = Column("ManufacturerCode", String, nullable=True)
    source_to_cutout_distance: Mapped[Optional[float]] = Column("SourceToCutoutDistance", Float, nullable=True)
    cutout_thickness: Mapped[Optional[float]] = Column("CutoutThickness", Float, nullable=True)
    cutout_material: Mapped[Optional[str]] = Column("CutoutMaterial", String, nullable=True)
    cutout_mass_density: Mapped[Optional[float]] = Column("CutoutMassDensity", Float, nullable=True)
    cutout_is_divergent: Mapped[Optional[int]] = Column("CutoutIsDivergent", Integer, nullable=True)
    cutout_is_rectangular: Mapped[Optional[int]] = Column("CutoutIsRectangular", Integer, nullable=True)
    cutout_half_x_outside: Mapped[Optional[float]] = Column("CutoutHalfXOutside", Float, nullable=True)
    cutout_half_y_outside: Mapped[Optional[float]] = Column("CutoutHalfYOutside", Float, nullable=True)

    # Foreign key relationship to Machine
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))
    machine: Mapped["Machine"] = relationship(
        "Machine",
        back_populates="electron_applicator_list",
        lazy="selectin"  # Use selectin loading for better performance
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
    Model representing a treatment machine in Pinnacle.

    This class stores comprehensive configuration data for a specific treatment machine
    including physical properties, jaw settings, operational parameters, and all
    associated components. It serves as the central model for machine data in the
    Pinnacle I/O system and manages relationships with various machine components
    such as energies, angles, MLC configurations, and applicators.

    The Machine model inherits from VersionedBase, providing automatic version
    tracking and timestamp management for configuration changes. This ensures
    full traceability of machine commissioning and modification history.

    Attributes:
        id (int): Primary key inherited from VersionedBase
        name (str): Display name of the machine (e.g., "Clinac iX", "TrueBeam")
        machine_type (str): Type/model of the machine (e.g., "Varian Clinac-2100")
        version_timestamp (str): Timestamp of the machine configuration version
        version_description (str): Description of the configuration version
        commissioned_by (str): Name of the person who commissioned the machine
        commission_version (str): Version of Pinnacle used for commissioning
        login_name (str): Login name of the user who last modified the configuration
        institution (str): Institution where the machine is located

        # Commission flags
        commissioned_for_photons (int): Flag indicating photon beam commissioning (1=yes, 0=no)
        commissioned_for_electrons (int): Flag indicating electron beam commissioning (1=yes, 0=no)
        commissioned_for_mc_electrons (int): Flag indicating Monte Carlo electron commissioning (1=yes, 0=no)
        commissioned_for_stereo (int): Flag indicating stereotactic commissioning (1=yes, 0=no)
        commissioned_for_protons (int): Flag indicating proton beam commissioning (1=yes, 0=no)
        read_write_machine (int): Flag indicating if machine can be modified (1=yes, 0=no)
        is_simulator (int): Flag indicating if this is a simulator machine (1=yes, 0=no)
        has_fixed_jaw (int): Flag indicating if machine has fixed jaws (1=yes, 0=no)

        # Physical properties
        sad (float): Source-to-axis distance in cm
        source_to_flattening_filter_distance (float): Distance to flattening filter in cm
        source_to_first_scattering_foil_distance (float): Distance to first scattering foil in cm
        source_to_last_scattering_foil_distance (float): Distance to last scattering foil in cm
        source_to_left_right_jaw_distance (float): Distance to X-jaw system in cm
        left_right_jaw_thickness (float): Thickness of X-jaws in cm
        source_to_top_bottom_jaw_distance (float): Distance to Y-jaw system in cm
        top_bottom_jaw_thickness (float): Thickness of Y-jaws in cm
        source_to_block_tray_distance (float): Distance to block tray in cm
        primary_collimation_angle (float): Primary collimation angle in degrees

    Relationships:
        couch_angle (CouchAngle): Couch angle configuration (one-to-one)
        gantry_angle (GantryAngle): Gantry angle configuration (one-to-one)
        collimator_angle (CollimatorAngle): Collimator angle configuration (one-to-one)
        config_rv (ConfigRV): Record and verify configuration (one-to-one)
        multi_leaf (MultiLeaf): Multi-leaf collimator configuration (one-to-one)
        electron_applicator_list (List[ElectronApplicator]): Available electron applicators (one-to-many)
        tolerance_table_list (List[TolTable]): Tolerance tables for QA (one-to-many)
        photon_energy_list (List[PhotonEnergy]): Available photon energies (one-to-many)
        electron_energy_list (List[ElectronEnergy]): Available electron energies (one-to-many)

    Example:
        >>> machine = Machine(
        ...     name="Clinac iX",
        ...     machine_type="Varian Clinac-2100",
        ...     commissioned_for_photons=1,
        ...     commissioned_for_electrons=1,
        ...     sad=100.0,
        ...     institution="General Hospital"
        ... )
    """

    __tablename__ = "Machine"

    # Primary key is inherited from VersionedBase
    name: Mapped[str] = Column("Name", String, nullable=False)
    machine_type: Mapped[Optional[str]] = Column("MachineType", String, nullable=True)
    version_timestamp: Mapped[Optional[str]] = Column("VersionTimestamp", String, nullable=True)
    version_description: Mapped[Optional[str]] = Column("VersionDescription", String, nullable=True)
    commissioned_by: Mapped[Optional[str]] = Column("CommissionedBy", String, nullable=True)
    commission_version: Mapped[Optional[str]] = Column("CommissionVersion", String, nullable=True)
    login_name: Mapped[Optional[str]] = Column("LoginName", String, nullable=True)
    institution: Mapped[Optional[str]] = Column("Institution", String, nullable=True)

    # Commission flags
    commissioned_for_photons: Mapped[Optional[int]] = Column("CommissionedForPhotons", Integer, nullable=True)
    commissioned_for_electrons: Mapped[Optional[int]] = Column(
        "CommissionedForElectrons", Integer, nullable=True
    )
    commissioned_for_mc_electrons: Mapped[Optional[int]] = Column(
        "CommissionedForMCElectrons", Integer, nullable=True
    )
    commissioned_for_stereo: Mapped[Optional[int]] = Column("CommissionedForStereo", Integer, nullable=True)
    commissioned_for_protons: Mapped[Optional[int]] = Column("CommissionedForProtons", Integer, nullable=True)
    read_write_machine: Mapped[Optional[int]] = Column("ReadWriteMachine", Integer, nullable=True)
    is_simulator: Mapped[Optional[int]] = Column("IsSimulator", Integer, nullable=True)
    has_fixed_jaw: Mapped[Optional[int]] = Column("HasFixedJaw", Integer, nullable=True)

    # Physical properties
    sad: Mapped[Optional[float]] = Column("SAD", Float, nullable=True)
    source_to_flattening_filter_distance: Mapped[Optional[float]] = Column(
        "SourceToFlatteningFilterDistance", Float, nullable=True
    )
    source_to_first_scattering_foil_distance: Mapped[Optional[float]] = Column(
        "SourceToFirstScatteringFoilDistance", Float, nullable=True
    )
    source_to_last_scattering_foil_distance: Mapped[Optional[float]] = Column(
        "SourceToLastScatteringFoilDistance", Float, nullable=True
    )
    source_to_left_right_jaw_distance: Mapped[Optional[float]] = Column(
        "SourceToLeftRightJawDistance", Float, nullable=True
    )
    left_right_jaw_thickness: Mapped[Optional[float]] = Column("LeftRightJawThickness", Float, nullable=True)
    source_to_top_bottom_jaw_distance: Mapped[Optional[float]] = Column(
        "SourceToTopBottomJawDistance", Float, nullable=True
    )
    top_bottom_jaw_thickness: Mapped[Optional[float]] = Column("TopBottomJawThickness", Float, nullable=True)
    source_to_block_tray_distance: Mapped[Optional[float]] = Column(
        "SourceToBlockTrayDistance", Float, nullable=True
    )
    primary_collimation_angle: Mapped[Optional[float]] = Column("PrimaryCollimationAngle", Float, nullable=True)

    # Left-Right jaw settings
    left_right_can_be_independent: Mapped[Optional[int]] = Column(
        "LeftRightCanBeIndependent", Integer, nullable=True
    )
    left_right_minimum_position: Mapped[Optional[float]] = Column(
        "LeftRightMinimumPosition", Float, nullable=True
    )
    left_right_maximum_position: Mapped[Optional[float]] = Column(
        "LeftRightMaximumPosition", Float, nullable=True
    )
    proton_left_right_maximum_position: Mapped[Optional[float]] = Column(
        "ProtonLeftRightMaximumPosition", Float, nullable=True
    )
    nominal_left_jaw_position: Mapped[Optional[float]] = Column("NominalLeftJawPosition", Float, nullable=True)
    nominal_right_jaw_position: Mapped[Optional[float]] = Column("NominalRightJawPosition", Float, nullable=True)
    fixed_left_right_jaw_position: Mapped[Optional[float]] = Column(
        "FixedLeftRightJawPosition", Float, nullable=True
    )
    left_jaw_name: Mapped[Optional[str]] = Column("LeftJawName", String, nullable=True)
    right_jaw_name: Mapped[Optional[str]] = Column("RightJawName", String, nullable=True)
    left_right_name: Mapped[Optional[str]] = Column("LeftRightName", String, nullable=True)
    left_right_decimal_places: Mapped[Optional[int]] = Column("LeftRightDecimalPlaces", Integer, nullable=True)
    left_right_jaw_material: Mapped[Optional[str]] = Column("LeftRightJawMaterial", String, nullable=True)
    left_right_mass_density: Mapped[Optional[float]] = Column("LeftRightMassDensity", Float, nullable=True)

    # Top-Bottom jaw settings
    top_bottom_can_be_independent: Mapped[Optional[int]] = Column(
        "TopBottomCanBeIndependent", Integer, nullable=True
    )
    top_bottom_minimum_position: Mapped[Optional[float]] = Column(
        "TopBottomMinimumPosition", Float, nullable=True
    )
    top_bottom_maximum_position: Mapped[Optional[float]] = Column(
        "TopBottomMaximumPosition", Float, nullable=True
    )
    proton_top_bottom_maximum_position: Mapped[Optional[float]] = Column(
        "ProtonTopBottomMaximumPosition", Float, nullable=True
    )
    nominal_top_jaw_position: Mapped[Optional[float]] = Column("NominalTopJawPosition", Float, nullable=True)
    nominal_bottom_jaw_position: Mapped[Optional[float]] = Column(
        "NominalBottomJawPosition", Float, nullable=True
    )
    fixed_top_bottom_jaw_position: Mapped[Optional[float]] = Column(
        "FixedTopBottomJawPosition", Float, nullable=True
    )
    top_jaw_name: Mapped[Optional[str]] = Column("TopJawName", String, nullable=True)
    bottom_jaw_name: Mapped[Optional[str]] = Column("BottomJawName", String, nullable=True)
    top_bottom_name: Mapped[Optional[str]] = Column("TopBottomName", String, nullable=True)
    top_bottom_decimal_places: Mapped[Optional[int]] = Column("TopBottomDecimalPlaces", Integer, nullable=True)
    top_bottom_jaw_material: Mapped[Optional[str]] = Column("TopBottomJawMaterial", String, nullable=True)
    top_bottom_mass_density: Mapped[Optional[float]] = Column("TopBottomMassDensity", Float, nullable=True)

    # Monitor unit settings
    cp_monitor_unit_decimal_places: Mapped[Optional[int]] = Column(
        "CPMonitorUnitDecimalPlaces", Integer, nullable=True
    )
    monitor_unit_decimal_places: Mapped[Optional[int]] = Column(
        "MonitorUnitDecimalPlaces", Integer, nullable=True
    )
    clip_beam_mu_to_max: Mapped[Optional[int]] = Column("ClipBeamMUToMax", Integer, nullable=True)
    clip_high_dose_beam_mu_to_max: Mapped[Optional[int]] = Column(
        "ClipHighDoseBeamMUToMax", Integer, nullable=True
    )
    monitor_unit_maximum: Mapped[Optional[int]] = Column("MonitorUnitMaximum", Integer, nullable=True)
    monitor_unit_max_for_high_dose: Mapped[Optional[int]] = Column(
        "MonitorUnitMaxForHighDose", Integer, nullable=True
    )
    monitor_unit_per_degree_maximum: Mapped[Optional[int]] = Column(
        "MonitorUnitPerDegreeMaximum", Integer, nullable=True
    )

    # Delivery settings
    blocks_allowed: Mapped[Optional[int]] = Column("BlocksAllowed", Integer, nullable=True)
    default_block_jaw_overlap: Mapped[Optional[int]] = Column("DefaultBlockJawOverlap", Integer, nullable=True)
    has_mlc: Mapped[Optional[int]] = Column("HasMLC", Integer, nullable=True)
    default_tolerance_table_name: Mapped[Optional[str]] = Column(
        "DefaultToleranceTableName", String, nullable=True
    )
    max_jaw_speed: Mapped[Optional[float]] = Column("MaxJawSpeed", Float, nullable=True)
    default_min_mu_per_seg: Mapped[Optional[int]] = Column("DefaultMinMUPerSeg", Integer, nullable=True)
    dose_rate_continuously_variable: Mapped[Optional[int]] = Column(
        "DoseRateContinuouslyVariable", Integer, nullable=True
    )
    dose_rate_constant: Mapped[Optional[int]] = Column("DoseRateConstant", Integer, nullable=True)
    limit_gantry_acceleration: Mapped[Optional[int]] = Column("LimitGantryAcceleration", Integer, nullable=True)
    gantry_acceleration_limit: Mapped[Optional[float]] = Column("GantryAccelerationLimit", Float, nullable=True)
    not_for_dose_computation: Mapped[Optional[int]] = Column("NotForDoseComputation", Integer, nullable=True)
    is_particle_machine: Mapped[Optional[int]] = Column("IsParticleMachine", Integer, nullable=True)
    use_high_dose: Mapped[Optional[int]] = Column("UseHighDose", Integer, nullable=True)

    # MU thresholds
    mu_threshold_static: Mapped[Optional[int]] = Column("MUThresholdStatic", Integer, nullable=True)
    mu_threshold_arc: Mapped[Optional[int]] = Column("MUThresholdArc", Integer, nullable=True)
    mu_threshold_conformal_arc: Mapped[Optional[int]] = Column("MUThresholdConformalArc", Integer, nullable=True)
    mu_threshold_mlc: Mapped[Optional[int]] = Column("MUThresholdMLC", Integer, nullable=True)
    mu_threshold_slid_win: Mapped[Optional[int]] = Column("MUThresholdSlidWin", Integer, nullable=True)
    mu_threshold_dynamic_arc: Mapped[Optional[int]] = Column("MUThresholdDynamicArc", Integer, nullable=True)
    mu_threshold_motorized_wedge: Mapped[Optional[int]] = Column(
        "MUThresholdMotorizedWedge", Integer, nullable=True
    )

    # Relationships
    couch_angle: Mapped[Optional["CouchAngle"]] = relationship(
        "CouchAngle",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == CouchAngle.machine_id",
        lazy="selectin"  # Use selectin loading for better performance
    )
    gantry_angle: Mapped[Optional["GantryAngle"]] = relationship(
        "GantryAngle",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == GantryAngle.machine_id",
        lazy="selectin"  # Use selectin loading for better performance
    )
    collimator_angle: Mapped[Optional["CollimatorAngle"]] = relationship(
        "CollimatorAngle",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == CollimatorAngle.machine_id",
        lazy="selectin"  # Use selectin loading for better performance
    )
    config_rv: Mapped[Optional["ConfigRV"]] = relationship(
        "ConfigRV",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
        lazy="selectin"  # Use selectin loading for better performance
    )
    multi_leaf: Mapped[Optional["MultiLeaf"]] = relationship(
        "MultiLeaf",
        uselist=False,
        back_populates="machine",
        cascade="all, delete-orphan",
        lazy="selectin"  # Use selectin loading for better performance
    )
    electron_applicator_list: Mapped[List["ElectronApplicator"]] = relationship(
        "ElectronApplicator",
        back_populates="machine",
        cascade="all, delete-orphan",
        lazy="selectin"  # Use selectin loading for better performance
    )
    tolerance_table_list: Mapped[List["TolTable"]] = relationship(
        "TolTable",
        back_populates="machine",
        cascade="all, delete-orphan",
        lazy="selectin"  # Use selectin loading for better performance
    )
    photon_energy_list: Mapped[List["PhotonEnergy"]] = relationship(
        "PhotonEnergy",
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == PhotonEnergy.machine_id",
        lazy="selectin"  # Use selectin loading for better performance
    )
    electron_energy_list: Mapped[List["ElectronEnergy"]] = relationship(
        "ElectronEnergy",
        back_populates="machine",
        cascade="all, delete-orphan",
        primaryjoin="Machine.id == ElectronEnergy.machine_id",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __repr__(self) -> str:
        return (
            f"<Machine(id={self.id}, name='{self.name}', type='{self.machine_type}')>"
        )

    def __init__(self, **kwargs):
        """
        Initialize a Machine instance.

        This constructor handles initialization of all machine attributes and relationships.
        It supports both direct attribute assignment and nested relationship creation
        through dictionaries. The constructor automatically processes version information
        and establishes proper relationships with child objects.

        Args:
            **kwargs: Keyword arguments used to initialize Machine attributes.
                Can include any of the machine attributes (name, machine_type, etc.)
                as well as relationship data for child objects.

        Relationship Parameters:
            couch_angle (dict or CouchAngle): Couch angle configuration data
            gantry_angle (dict or GantryAngle): Gantry angle configuration data
            collimator_angle (dict or CollimatorAngle): Collimator angle configuration data
            config_rv (dict or ConfigRV): Record and verify configuration data
            multi_leaf (dict or MultiLeaf): Multi-leaf collimator configuration data
            electron_applicator_list (list): List of electron applicator data (dicts or objects)
            tolerance_table_list (list): List of tolerance table data (dicts or objects)
            photon_energy_list (list): List of photon energy data (dicts or objects)
            electron_energy_list (list): List of electron energy data (dicts or objects)

        Example:
            >>> machine = Machine(
            ...     name="Clinac iX",
            ...     machine_type="Varian Clinac-2100",
            ...     commissioned_for_photons=1,
            ...     sad=100.0,
            ...     couch_angle={
            ...         "minimum_angle": -90.0,
            ...         "maximum_angle": 90.0
            ...     },
            ...     photon_energy_list=[
            ...         {"name": "6X", "value": 6.0}
            ...     ]
            ... )
        """
        super().__init__(**kwargs)
