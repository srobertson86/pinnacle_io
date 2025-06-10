"""
SQLAlchemy models for Pinnacle machine configuration data.

This module provides data models for machine configurations in Pinnacle,
including rotational beam delivery settings and tolerance tables.
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from pinnacle_io.models.machine import Machine


class ConfigRV(PinnacleBase):
    """
    Represents a Pinnacle treatment machine's configuration for rotational beam delivery.

    This class stores machine-specific parameters related to rotational beam delivery,
    including jaw positions and MLC configurations.

    Attributes:
        id (int): Primary key
        enabled (int): Flag indicating if this configuration is enabled
        left_jaw (str): Left jaw position
        right_jaw (str): Right jaw position
        top_jaw (str): Top jaw position
        bottom_jaw (str): Bottom jaw position
        mlc_bank_swap (str): MLC bank swap configuration
        mlc_order_swap (str): MLC order swap configuration
        elekta_relative_mlc_positions (int): Elekta-specific MLC position setting

    Relationships:
        machine (Machine): The parent Machine this configuration belongs to (one-to-one)
    """

    __tablename__ = "ConfigRV"

    # Configuration parameters
    enabled: Mapped[Optional[int]] = Column("Enabled", Integer, nullable=True)
    left_jaw: Mapped[Optional[str]] = Column("LeftJaw", String, nullable=True)
    right_jaw: Mapped[Optional[str]] = Column("RightJaw", String, nullable=True)
    top_jaw: Mapped[Optional[str]] = Column("TopJaw", String, nullable=True)
    bottom_jaw: Mapped[Optional[str]] = Column("BottomJaw", String, nullable=True)
    mlc_bank_swap: Mapped[Optional[str]] = Column("MLCBankSwap", String, nullable=True)
    mlc_order_swap: Mapped[Optional[str]] = Column("MLCOrderSwap", String, nullable=True)
    elekta_relative_mlc_positions: Mapped[Optional[int]] = Column(
        "ElektaRelativeMLCPositions", Integer, nullable=True
    )

    # Relationships
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))
    machine: Mapped["Machine"] = relationship(
        "Machine", 
        back_populates="config_rv",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __repr__(self) -> str:
        return (
            f"<ConfigRV(id={self.id}, "
            f"machine_id={self.machine_id}, "
            f"enabled={self.enabled}, "
            f"left_jaw='{self.left_jaw}', "
            f"right_jaw='{self.right_jaw}', "
            f"top_jaw='{self.top_jaw}', "
            f"bottom_jaw='{self.bottom_jaw}')>"
        )

    def __init__(self, **kwargs):
        """
        Initialize a ConfigRV instance.

        Args:
            **kwargs: Arbitrary keyword arguments used to initialize ConfigRV attributes.
        """
        super().__init__(**kwargs)


class TolTable(PinnacleBase):
    """
    Represents a tolerance table for a Pinnacle treatment machine.

    This class stores tolerance settings that define the acceptable variations
    in beam delivery parameters for quality assurance purposes.

    Attributes:
        id (int): Primary key
        name (str): Name of the tolerance table
        number (int): Tolerance table number

    Relationships:
        machine (Machine): The parent Machine this tolerance table belongs to (many-to-one)
    """

    __tablename__ = "TolTable"

    # Tolerance table attributes
    name: Mapped[Optional[str]] = Column("Name", String, nullable=True)
    number: Mapped[Optional[int]] = Column("Number", Integer, nullable=True)

    # Relationships
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))
    machine: Mapped["Machine"] = relationship(
        "Machine", 
        back_populates="tolerance_table_list",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __repr__(self) -> str:
        return f"<TolTable(id={self.id}, name='{self.name}', number={self.number})>"

    def __init__(self, **kwargs):
        """
        Initialize a TolTable instance.

        Args:
            **kwargs: Arbitrary keyword arguments used to initialize TolTable attributes.
        """
        super().__init__(**kwargs)
