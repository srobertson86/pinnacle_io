"""
SQLAlchemy model for Pinnacle machine energy and output factor data.

This module implements a polymorphic mapping pattern for machine energies using SQLAlchemy.
The class hierarchy consists of an abstract base class (MachineEnergy) and two concrete
implementations (PhotonEnergy and ElectronEnergy). All energy types share the same
database table (MachineEnergy) with a type discriminator column that distinguishes
between photon and electron energies.

Database Schema:
    - All energy types are stored in the MachineEnergy table
    - The 'type' column contains values: 'photon', 'electron'
    - Common fields are defined in the MachineEnergy class
    - Relationships can target specific energy types

Usage:
    # Create specific energy types
    photon = PhotonEnergy(name="6X", value=6.0)  # type="photon" set automatically
    electron = ElectronEnergy(name="6E", value=6.0)  # type="electron" set automatically

    # Query options
    all_energies = session.query(MachineEnergy).all()  # Get all energy types
    photon_energies = session.query(PhotonEnergy).all()  # Get only photon energies
    electron_energies = session.query(ElectronEnergy).all()  # Get only electron energies
"""

from typing import TYPE_CHECKING
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models import Machine


class OutputFactor(PinnacleBase):
    """
    Represents output factor data for a machine energy in Pinnacle.
    """

    __tablename__ = "OutputFactor"

    # Primary key is inherited from PinnacleBase
    reference_depth: Mapped[float] = Column("ReferenceDepth", Float, nullable=True)
    source_to_calibration_point_distance: Mapped[float] = Column(
        "SourceToCalibrationPointDistance", Float, nullable=True
    )
    electron_ssd_tolerance: Mapped[float] = Column(
        "ElectronSSDTolerance", Float, nullable=True
    )
    dose_per_mu_at_calibration: Mapped[float] = Column(
        "DosePerMuAtCalibration", Float, nullable=True
    )
    min_mlc_position_at_calibration: Mapped[float] = Column(
        "MinMLCPositionAtCalibration", Float, nullable=True
    )
    calculated_calibration_dose: Mapped[float] = Column(
        "CalculatedCalibrationDose", Float, nullable=True
    )
    computation_version: Mapped[str] = Column(
        "ComputationVersion", String, nullable=True
    )
    calculated_calibration_dose_valid: Mapped[int] = Column(
        "CalculatedCalibrationDoseValid", Integer, nullable=True
    )

    # Foreign key relationship to MachineEnergy
    physics_data_id: Mapped[int] = Column(Integer, ForeignKey("PhysicsData.ID"))
    physics_data: Mapped["PhysicsData"] = relationship(
        "PhysicsData", back_populates="output_factor"
    )

    def __init__(self, **kwargs):
        """
        Initialize an OutputFactor instance.
        Args:
            **kwargs: Keyword arguments used to initialize OutputFactor attributes.

        Relationships:
            physics_data (PhysicsData): The parent PhysicsData to which this OutputFactor belongs (one-to-one).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<OutputFactor(id={self.id}, dose_per_mu_at_calibration={self.dose_per_mu_at_calibration})>"


class PhysicsData(PinnacleBase):
    """
    Represents physics data associated with a machine energy in Pinnacle.

    This class is used to encapsulate the output factor data for a specific machine energy.
    It serves as a container for the OutputFactor relationship, allowing for easy access
    to physics-related attributes.

    Attributes:
        output_factor (OutputFactor): The associated output factor data.
    """

    __tablename__ = "PhysicsData"

    # Parent relationship
    machine_energy_id: Mapped[int] = Column(Integer, ForeignKey("MachineEnergy.ID"))
    machine_energy: Mapped["MachineEnergy"] = relationship(
        "MachineEnergy",
        back_populates="physics_data",
        uselist=False,
    )
    
    # Child relationship
    output_factor: Mapped["OutputFactor"] = relationship(
        "OutputFactor",
        uselist=False,
        back_populates="physics_data",
        cascade="all, delete-orphan",
    )

    def __init__(self, **kwargs):
        """
        Initialize a PhysicsData instance.

        Args:
            **kwargs: Keyword arguments used to initialize PhysicsData attributes.

        Relationships:
            machine_energy (MachineEnergy): The parent MachineEnergy to which this PhysicsData belongs (one-to-one).
            output_factor (OutputFactor): The associated output factor data (one-to-one).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of the PhysicsData instance.
        """
        return f"<PhysicsData(id={self.id}, machine_energy_id={self.machine_energy_id})>"


class MachineEnergy(PinnacleBase):
    """
    Abstract base class for machine energy configurations in Pinnacle.

    This class serves as the base class for PhotonEnergy and ElectronEnergy, implementing
    SQLAlchemy's polymorphic mapping pattern. All energy types share this table with a
    type discriminator column ('type') that determines the specific subclass.

    Polymorphic Configuration:
        - Table name: MachineEnergy
        - Discriminator column: 'type'
        - Possible type values: 'photon', 'electron'

    Common Attributes:
        value (float): The energy value (e.g., 6.0 for 6MV photons or 6MeV electrons)
        name (str): Display name for the energy (e.g., "6X" or "6E")
        scan_pattern_label (str): Label for the scan pattern
        default_block_and_tray_factor (float): Combined block and tray transmission factor
        default_tray_factor (float): Tray transmission factor
        default_mlc_factor (float): MLC transmission factor
        initial_dose_rate_for_table (float): Initial dose rate setting
        default_dose_rate (float): Default dose rate setting
        fluence_mode (int): Fluence calculation mode
        fluence_mode_id (str): Identifier for fluence mode
        high_dose_technique (int): Flag for high dose technique

    Relationships:
        machine (Machine): The parent Machine (defined in subclasses)
        output_factor (OutputFactor): Associated physics data (one-to-one)
    """

    __tablename__ = "MachineEnergy"

    # Primary key is inherited from PinnacleBase
    value: Mapped[float] = Column("Value", Float, nullable=True)
    name: Mapped[str] = Column("Name", String, nullable=True)
    scan_pattern_label: Mapped[str] = Column("ScanPatternLabel", String, nullable=True)
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

    # Type discriminator to determine subclass
    type: Mapped[str] = Column("Type", String(10), nullable=False)

    # One-to-one relationship with PhysicsData
    physics_data: Mapped["PhysicsData"] = relationship(
        "PhysicsData",
        uselist=False,
        back_populates="machine_energy",
        cascade="all, delete-orphan",
    )

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "machine_energy"
    }

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
        
        # physics_data = kwargs.pop("physics_data", kwargs.pop("PhysicsData", None))
        # if physics_data is not None:
        #     output_factor = physics_data.get("output_factor", physics_data.get("OutputFactor", None))
        #     if output_factor is not None:
        #         kwargs["output_factor"] = output_factor
        
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}', value={self.value})>"


class PhotonEnergy(MachineEnergy):
    """
    Represents a photon energy configuration for a Pinnacle treatment machine.

    This class is a concrete implementation of MachineEnergy for photon beams.
    It inherits all attributes from MachineEnergy and adds a specific relationship
    to the Machine class for photon energies.

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
    """

    __mapper_args__ = {
        "polymorphic_identity": "photon"
    }

    # Relationship back to machine
    machine: Mapped["Machine"] = relationship(
        "Machine",
        back_populates="photon_energy_list",
        primaryjoin="Machine.id == PhotonEnergy.machine_id",
    )

    def __init__(self, **kwargs):
        """
        Initialize a PhotonEnergy instance.

        Args:
            **kwargs: Keyword arguments used to initialize PhotonEnergy attributes.

        Relationships:
            machine (Machine): The parent Machine to which this PhotonEnergy belongs (many-to-one).
            output_factor (OutputFactor): Associated output factor data (one-to-one).
        """
        super().__init__(**kwargs)


class ElectronEnergy(MachineEnergy):
    """
    Represents an electron energy configuration for a Pinnacle treatment machine.

    This class is a concrete implementation of MachineEnergy for electron beams.
    It inherits all attributes from MachineEnergy and adds a specific relationship
    to the Machine class for electron energies.

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
    """

    __mapper_args__ = {
        "polymorphic_identity": "electron"
    }

    # Relationship back to machine
    machine: Mapped["Machine"] = relationship(
        "Machine",
        back_populates="electron_energy_list",
        primaryjoin="Machine.id == ElectronEnergy.machine_id",
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
