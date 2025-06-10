"""
SQLAlchemy ORM models for Pinnacle treatment machine energy configurations.

This module implements a polymorphic hierarchy for modeling different types of 
machine energies (photon and electron) in a Pinnacle treatment planning system.
The class hierarchy consists of an abstract base class (MachineEnergy) and two
concrete implementations (PhotonEnergy and ElectronEnergy). All energy types 
share the same database table (MachineEnergy) with a type discriminator column.

Class Hierarchy:
    MachineEnergy (Abstract Base Class)
    ├── PhotonEnergy (Concrete Class for photon beams)
    └── ElectronEnergy (Concrete Class for electron beams)

Key Features:
- Polymorphic mapping for different energy types
- Support for both photon and electron beam configurations
- Detailed physics data and output factors
- Relationships to parent Machine and related physics data
- Type-safe relationships between models

Database Schema:
    - All energy types are stored in the MachineEnergy table
    - The 'type' column contains values: 'photon', 'electron'
    - Common fields are defined in the MachineEnergy class
    - Relationships can target specific energy types

Example Usage:
    # Create a new machine with photon and electron energies
    from sqlalchemy.orm import Session
    from pinnacle_io.models.machine import Machine
    from pinnacle_io.models.machine_energy import PhotonEnergy, ElectronEnergy
    
    # Initialize database session
    session = Session(engine)
    
    try:
        # Create a new machine
        machine = Machine(name="TrueBeam")
        
        # Add photon energies
        photon_6x = PhotonEnergy(
            name="6X", 
            value=6.0,
            machine=machine,
            dmax=1.5,
            tpr2010=0.67,
            pdd10=66.7
        )
        
        # Add electron energy with applicator and SSD
        electron_6mev = ElectronEnergy(
            name="6E", 
            value=6.0,
            electron_cone="10x10",
            electron_ssd=100.0,
            machine=machine,
            r50=2.5,
            rp=3.1
        )
        
        # Add to session and commit
        session.add_all([machine, photon_6x, electron_6mev])
        session.commit()
        
        # Query examples
        # Get all photon energies for a machine
        photon_energies = session.query(PhotonEnergy).\
            filter(PhotonEnergy.machine == machine).all()
            
        # Get electron energy by name
        electron = session.query(ElectronEnergy).\
            filter(
                ElectronEnergy.name == "6E",
                ElectronEnergy.machine == machine
            ).first()
            
    finally:
        session.close()
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, ClassVar

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.machine import Machine


class OutputFactor(PinnacleBase):
    """
    Represents output factor data for a machine energy in Pinnacle.

    This class stores calibration and output factor data for a specific machine energy,
    including dose calibration values, measurement conditions, and validation flags.

    Attributes:
        id (int): Primary key
        reference_depth (float): Reference depth for output factor measurements (cm)
        source_to_calibration_point_distance (float): Distance from source to calibration point (cm)
        electron_ssd_tolerance (float): Allowed SSD tolerance for electron beams (cm)
        dose_per_mu_at_calibration (float): Dose per MU at calibration conditions (cGy/MU)
        min_mlc_position_at_calibration (float): Minimum MLC position during calibration (cm)
        calculated_calibration_dose (float): Calculated dose at calibration point (cGy)
        computation_version (str): Version of the computation algorithm used
        calculated_calibration_dose_valid (int): Flag indicating if calculated dose is valid

    Relationships:
        physics_data (PhysicsData): The parent PhysicsData this output factor belongs to (one-to-one)
    """

    __tablename__ = "OutputFactor"

    # Calibration parameters
    reference_depth: Mapped[Optional[float]] = Column("ReferenceDepth", Float, nullable=True)
    source_to_calibration_point_distance: Mapped[Optional[float]] = Column(
        "SourceToCalibrationPointDistance", Float, nullable=True
    )
    electron_ssd_tolerance: Mapped[Optional[float]] = Column(
        "ElectronSSDTolerance", Float, nullable=True
    )
    dose_per_mu_at_calibration: Mapped[Optional[float]] = Column(
        "DosePerMuAtCalibration", Float, nullable=True
    )
    min_mlc_position_at_calibration: Mapped[Optional[float]] = Column(
        "MinMLCPositionAtCalibration", Float, nullable=True
    )
    calculated_calibration_dose: Mapped[Optional[float]] = Column(
        "CalculatedCalibrationDose", Float, nullable=True
    )
    computation_version: Mapped[Optional[str]] = Column(
        "ComputationVersion", String, nullable=True
    )
    calculated_calibration_dose_valid: Mapped[Optional[int]] = Column(
        "CalculatedCalibrationDoseValid", Integer, nullable=True
    )

    # Relationships
    physics_data_id: Mapped[int] = Column(Integer, ForeignKey("PhysicsData.ID"))
    physics_data: Mapped["PhysicsData"] = relationship(
        "PhysicsData", 
        back_populates="output_factor",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __init__(self, **kwargs):
        """
        Initialize an OutputFactor instance.

        Args:
            **kwargs: Keyword arguments used to initialize OutputFactor attributes.
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of the OutputFactor instance.
        
        Returns:
            str: String representation including ID and dose per MU
        """
        return (
            f"<OutputFactor(id={self.id}, "
            f"dose_per_mu_at_calibration={self.dose_per_mu_at_calibration})>"
        )


class PhysicsData(PinnacleBase):
    """
    Represents physics data associated with a machine energy in Pinnacle.

    This class serves as an intermediary between MachineEnergy and OutputFactor,
    encapsulating the output factor data for a specific machine energy. It allows
    for a clean separation of concerns in the data model.

    Attributes:
        id (int): Primary key
        machine_energy_id (int): Foreign key to the parent MachineEnergy

    Relationships:
        machine_energy (MachineEnergy): The parent MachineEnergy this data belongs to (one-to-one)
        output_factor (OutputFactor): The associated output factor data (one-to-one)
    """

    __tablename__ = "PhysicsData"

    # Relationships
    machine_energy_id: Mapped[int] = Column(Integer, ForeignKey("MachineEnergy.ID"))
    machine_energy: Mapped["MachineEnergy"] = relationship(
        "MachineEnergy",
        back_populates="physics_data",
        uselist=False,
        lazy="selectin"  # Use selectin loading for better performance
    )
    
    output_factor: Mapped[Optional["OutputFactor"]] = relationship(
        "OutputFactor",
        uselist=False,
        back_populates="physics_data",
        cascade="all, delete-orphan",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __init__(self, **kwargs):
        """
        Initialize a PhysicsData instance.

        Args:
            **kwargs: Keyword arguments used to initialize PhysicsData attributes.
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of the PhysicsData instance.
        
        Returns:
            str: String representation including ID and machine_energy_id
        """
        return (
            f"<PhysicsData(id={self.id}, "
            f"machine_energy_id={self.machine_energy_id})>"
        )


class MachineEnergy(PinnacleBase):
    """
    Abstract base class for machine energy configurations in Pinnacle.

    This class serves as the base class for PhotonEnergy and ElectronEnergy, implementing
    SQLAlchemy's polymorphic mapping pattern. All energy types share this table with a
    type discriminator column ('type') that determines the specific subclass.

    Key Features:
    - Polymorphic mapping for different energy types
    - Common attributes for all machine energies
    - Standardized PDD (Percent Depth Dose) values
    - Relationships to physics data and parent machine

    Database Schema:
        - Table name: MachineEnergy
        - Discriminator column: 'type' with values: 'photon', 'electron'
        - Common fields for all energy types

    Attributes:
        id (int): Primary key
        value (float): The energy value (e.g., 6.0 for 6MV photons or 6MeV electrons)
        name (str): Display name for the energy (e.g., "6X" or "6E")
        scan_pattern_label (str): Label for the scan pattern
        default_block_and_tray_factor (float): Combined block and tray transmission factor
        default_block_factor (float): Block transmission factor
        default_tray_factor (float): Tray transmission factor
        ssd (float): Source-to-surface distance (cm)
        type (str): Discriminator for polymorphic identity ('photon' or 'electron')

    Relationships:
        physics_data (PhysicsData): Associated physics data including output factors (one-to-one)
        machine_id (int): Foreign key to the parent Machine
        machine (Machine): The parent machine this energy belongs to (many-to-one)
    """

    __tablename__ = "MachineEnergy"
    __mapper_args__ = {
        "polymorphic_identity": "machine_energy",
        "polymorphic_on": "type",
        "with_polymorphic": "*"
    }

    # Energy identification and basic parameters
    value: Mapped[float] = Column("Value", Float, nullable=True)
    units: ClassVar[str] = ""
    name: Mapped[str] = Column("Name", String, nullable=True)
    scan_pattern_label: Mapped[Optional[str]] = Column("ScanPatternLabel", String, nullable=True)
    
    # Transmission factors
    default_block_and_tray_factor: Mapped[float] = Column(
        "DefaultBlockAndTrayFactor", Float, nullable=True
    )
    default_tray_factor: Mapped[float] = Column("DefaultTrayFactor", Float, nullable=True)
    default_mlc_factor: Mapped[float] = Column("DefaultMLCFactor", Float, nullable=True)
    initial_dose_rate_for_table: Mapped[float] = Column(
        "InitialDoseRateForTable", Float, nullable=True
    )
    default_dose_rate: Mapped[float] = Column("DefaultDoseRate", Float, nullable=True)
    fluence_mode: Mapped[int] = Column("FluenceMode", Integer, nullable=True)
    fluence_mode_id: Mapped[str] = Column("FluenceModeID", String, nullable=True)
    high_dose_technique: Mapped[int] = Column("HighDoseTechnique", Integer, nullable=True)

    # Foreign key relationship to Machine
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))

    # Type discriminator column for polymorphic inheritance
    type: Mapped[str] = Column("Type", String(10), nullable=False)

    # Relationships
    physics_data: Mapped[Optional["PhysicsData"]] = relationship(
        "PhysicsData",
        back_populates="machine_energy",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __init__(self, **kwargs):
        """
        Initialize a MachineEnergy instance.

        Args:
            **kwargs: Keyword arguments used to initialize MachineEnergy attributes.

        Relationships:
            machine (Machine): The parent Machine to which this MachineEnergy belongs (many-to-one).
            output_factor (OutputFactor): Associated output factor data (one-to-one).
        """
        machine_energy = kwargs.pop("machine_energy", kwargs.pop("MachineEnergy", None))
        if machine_energy is not None:
            super().__init__(**machine_energy)
            return
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of the MachineEnergy instance.
        
        Returns:
            str: String representation including ID, name, value, and units
        """
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}', value={self.value:g}, units='{self.units}')>"


class PhotonEnergy(MachineEnergy):
    """
    Represents a photon energy configuration for a Pinnacle treatment machine.

    This class is a concrete implementation of MachineEnergy for photon beams.
    It inherits all attributes from MachineEnergy and adds a specific relationship
    to the Machine class for photon energies.

    Key Features:
    - Inherits all attributes from MachineEnergy
    - Polymorphic identity set to 'photon'
    - Specific relationship to parent Machine
    - Additional photon-specific attributes and methods

    Polymorphic Identity:
        type = "photon"

    Example:
        machine = Machine(name="TrueBeam")
        energy = PhotonEnergy(
            name="6X",
            value=6.0,
            machine=machine
        )
        # The energy will be stored in the MachineEnergy table with type="photon"
    
    Attributes:
        id (int): Primary key
        value (float): Photon energy in MV (e.g., 6.0 for 6MV)
        name (str): Display name (e.g., "6X")
        machine_id (int): Foreign key to parent Machine
        
    Relationships:
        machine (Machine): The parent Machine (many-to-one)
        physics_data (PhysicsData): Associated physics data (one-to-one)
    """

    __mapper_args__ = {
        "polymorphic_identity": "photon"
    }

    units: ClassVar[str] = "MV"

    # Relationship back to machine with explicit join condition and loading strategy
    machine: Mapped["Machine"] = relationship(
        "Machine",
        back_populates="photon_energy_list",
        primaryjoin="Machine.id == PhotonEnergy.machine_id",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __init__(self, **kwargs):
        """
        Initialize a PhotonEnergy instance.

        Args:
            **kwargs: Keyword arguments used to initialize PhotonEnergy attributes.
                     Can include any attribute from MachineEnergy plus photon-specific ones.
        """
        super().__init__(**kwargs)


class ElectronEnergy(MachineEnergy):
    """
    Represents an electron energy configuration for a Pinnacle treatment machine.

    This class is a concrete implementation of MachineEnergy for electron beams.
    It inherits all attributes from MachineEnergy and adds electron-specific
    attributes and relationships.

    Key Features:
    - Inherits all attributes from MachineEnergy
    - Polymorphic identity set to 'electron'
    - Specific relationship to parent Machine
    - Additional electron-specific attributes and methods

    Polymorphic Identity:
        type = "electron"

    Example:
        machine = Machine(name="TrueBeam")
        energy = ElectronEnergy(
            name="6E",
            value=6.0,
            machine=machine
        )
        # The energy will be stored in the MachineEnergy table with type="electron"
    
    Attributes:
        id (int): Primary key
        value (float): Electron energy in MeV (e.g., 6.0 for 6 MeV)
        name (str): Display name (e.g., "6E")
        machine_id (int): Foreign key to parent Machine
        electron_cone (str): Electron cone/applicator type
        electron_ssd (float): Source-to-surface distance (cm)
        
    Relationships:
        machine (Machine): The parent Machine (many-to-one)
        physics_data (PhysicsData): Associated physics data (one-to-one)
    """

    __mapper_args__ = {
        "polymorphic_identity": "electron"
    }

    units: ClassVar[str] = "MeV"

    # Relationship back to machine with explicit join condition and loading strategy
    machine: Mapped["Machine"] = relationship(
        "Machine",
        back_populates="electron_energy_list",
        primaryjoin="Machine.id == ElectronEnergy.machine_id",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __init__(self, **kwargs):
        """
        Initialize an ElectronEnergy instance.

        Args:
            **kwargs: Keyword arguments used to initialize ElectronEnergy attributes.

        Relationships:
            machine (Machine): The parent Machine to which this ElectronEnergy belongs (many-to-one).
            output_factor (OutputFactor): Associated output factor data (one-to-one).
        """
        super().__init__(**kwargs)
        