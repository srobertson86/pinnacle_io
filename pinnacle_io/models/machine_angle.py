"""
SQLAlchemy model for Pinnacle machine data.

This module implements angle configurations using SQLAlchemy's abstract base class pattern.
Unlike the machine_energy module which uses polymorphic inheritance with a shared table,
this module uses separate tables for each angle type. This design choice reflects that:

1. Angle types are distinct and cannot change (a couch angle never becomes a gantry angle)
2. Each machine has exactly one of each angle type (one-to-one relationships)
3. Angles are typically queried by their specific type, not as a collection
4. Separate tables provide better type safety and clearer database structure

Database Schema:
    - CouchAngle table: Stores couch angle configurations
    - GantryAngle table: Stores gantry angle configurations
    - CollimatorAngle table: Stores collimator angle configurations
    Each table inherits common fields from AngleBase but exists independently.

Usage:
    # Each angle type is accessed directly
    machine.couch_angle      # Returns CouchAngle instance
    machine.gantry_angle     # Returns GantryAngle instance
    machine.collimator_angle # Returns CollimatorAngle instance
"""

from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.machine import Machine


class AngleBase(PinnacleBase):
    """
    Abstract base class for angle configurations in Pinnacle treatment machines.

    This class uses SQLAlchemy's abstract base class pattern (__abstract__ = True)
    to provide common fields and functionality for all angle types without creating
    a shared table. Each subclass (CouchAngle, GantryAngle, CollimatorAngle) has
    its own table with these common fields.

    This design was chosen over polymorphic inheritance because:
    - Each angle type is distinct and cannot change
    - Machines have exactly one of each angle type
    - Angles are queried individually, not as collections
    - Separate tables provide better type safety

    Common Attributes:
        name (str): Display name for the angle
        twelve_o_clock_angle (float): Reference angle for 12 o'clock position
        clockwise_increases (int): Whether angle increases clockwise
        nominal_angle (float): Default angle value
        minimum_angle (float): Minimum allowed angle
        maximum_angle (float): Maximum allowed angle
        roll_angle (float): Roll angle around the beam's eye view
        pitch_angle (float): Pitch angle around the lateral axis
        max_gantry_rotation_speed (float): Max speed for gantry rotation
        max_gantry_rotation_speed_mu (float): Max speed for gantry rotation (MU)
        min_gantry_rotation_speed_mu (float): Min speed for gantry rotation (MU)
        decimal_places (int): Number of decimal places for angle values
        can_be_arc (int): Whether the angle can be part of an arc
        rotation_direction (str): Direction of rotation (e.g., 'CW' for clockwise)
        conformal_arc (int): Whether conformal arc is enabled
        dynamic_arc (int): Whether dynamic arc is enabled
        has_c_arm (int): Whether a C-arm is present
        c_arm_max_angle (float): Max angle for C-arm rotation
        c_arm_decimal_places (float): Decimal places for C-arm angles
        angular_rate_constant (int): Constant for angular rate calculations
        is_gantry_continuous (int): Whether gantry rotation is continuous
    """

    __abstract__ = True

    # Common fields for all angle types
    name: Mapped[Optional[str]] = Column("Name", String, nullable=True)
    twelve_o_clock_angle: Mapped[Optional[float]] = Column(
        "TwelveOClockAngle", Float, nullable=True
    )
    clockwise_increases: Mapped[Optional[int]] = Column(
        "ClockwiseIncreases", Integer, nullable=True
    )
    nominal_angle: Mapped[Optional[float]] = Column(
        "NominalAngle", Float, nullable=True
    )
    minimum_angle: Mapped[Optional[float]] = Column(
        "MinimumAngle", Float, nullable=True
    )
    maximum_angle: Mapped[Optional[float]] = Column(
        "MaximumAngle", Float, nullable=True
    )
    roll_angle: Mapped[Optional[float]] = Column("RollAngle", Float, nullable=True)
    pitch_angle: Mapped[Optional[float]] = Column("PitchAngle", Float, nullable=True)
    max_gantry_rotation_speed: Mapped[Optional[float]] = Column(
        "MaxGantryRotationSpeed", Float, nullable=True
    )
    max_gantry_rotation_speed_mu: Mapped[Optional[float]] = Column(
        "MaxGantryRotationSpeedMU", Float, nullable=True
    )
    min_gantry_rotation_speed_mu: Mapped[Optional[float]] = Column(
        "MinGantryRotationSpeedMU", Float, nullable=True
    )
    decimal_places: Mapped[Optional[int]] = Column(
        "DecimalPlaces", Integer, nullable=True
    )
    can_be_arc: Mapped[Optional[int]] = Column("CanBeArc", Integer, nullable=True)
    rotation_direction: Mapped[Optional[str]] = Column(
        "RotationDirection", String, nullable=True
    )
    conformal_arc: Mapped[Optional[int]] = Column(
        "ConformalArc", Integer, nullable=True
    )
    dynamic_arc: Mapped[Optional[int]] = Column("DynamicArc", Integer, nullable=True)
    has_c_arm: Mapped[Optional[int]] = Column("HasCArm", Integer, nullable=True)
    c_arm_max_angle: Mapped[Optional[float]] = Column(
        "CArmMaxAngle", Float, nullable=True
    )
    c_arm_decimal_places: Mapped[Optional[float]] = Column(
        "CArmDecimalPlaces", Float, nullable=True
    )
    angular_rate_constant: Mapped[Optional[int]] = Column(
        "AngularRateConstant", Integer, nullable=True
    )
    is_gantry_continuous: Mapped[Optional[int]] = Column(
        "IsGantryContinuous", Integer, nullable=True
    )

    # Common foreign key relationship
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, machine_id={self.machine_id}, min={self.minimum_angle}, max={self.maximum_angle})>"


class CouchAngle(AngleBase):
    """
    Represents couch angle configuration for a Pinnacle treatment machine.
    """

    __tablename__ = "CouchAngle"

    # Relationship back to machine
    machine: Mapped["Machine"] = relationship(
        "Machine",
        back_populates="couch_angle",
        primaryjoin="Machine.id == CouchAngle.machine_id",
    )

    def __init__(self, **kwargs):
        """
        Initialize a CouchAngle instance.

        Args:
            **kwargs: Keyword arguments used to initialize CouchAngle attributes.

        Relationships:
            machine (Machine): The parent Machine to which this CouchAngle belongs (many-to-one).
        """
        super().__init__(**kwargs)


class GantryAngle(AngleBase):
    """
    Represents gantry angle configuration for a Pinnacle treatment machine.
    """

    __tablename__ = "GantryAngle"

    # Relationship back to machine
    machine: Mapped["Machine"] = relationship(
        "Machine",
        back_populates="gantry_angle",
        primaryjoin="Machine.id == GantryAngle.machine_id",
    )

    def __init__(self, **kwargs):
        """
        Initialize a GantryAngle instance.

        Args:
            **kwargs: Keyword arguments used to initialize GantryAngle attributes.

        Relationships:
            machine (Machine): The parent Machine to which this GantryAngle belongs (many-to-one).
        """
        super().__init__(**kwargs)


class CollimatorAngle(AngleBase):
    """
    Represents collimator angle configuration for a Pinnacle treatment machine.
    """

    __tablename__ = "CollimatorAngle"

    # Relationship back to machine
    machine: Mapped["Machine"] = relationship(
        "Machine",
        back_populates="collimator_angle",
        primaryjoin="Machine.id == CollimatorAngle.machine_id",
    )

    def __init__(self, **kwargs):
        """
        Initialize a CollimatorAngle instance.

        Args:
            **kwargs: Keyword arguments used to initialize CollimatorAngle attributes.

        Relationships:
            machine (Machine): The parent Machine to which this CollimatorAngle belongs (many-to-one).
        """
        super().__init__(**kwargs)
