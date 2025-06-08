"""
SQLAlchemy model for Pinnacle machine configuration data.
"""

from typing import TYPE_CHECKING
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models import Machine


class ConfigRV(PinnacleBase):
    """
    Represents a Pinnacle treatment machine's configuration for rotational
    beam delivery.
    """

    __tablename__ = "ConfigRV"

    # Primary key is inherited from PinnacleBase
    enabled: Mapped[int] = Column("Enabled", Integer, nullable=True)
    left_jaw: Mapped[str] = Column("LeftJaw", String, nullable=True)
    right_jaw: Mapped[str] = Column("RightJaw", String, nullable=True)
    top_jaw: Mapped[str] = Column("TopJaw", String, nullable=True)
    bottom_jaw: Mapped[str] = Column("BottomJaw", String, nullable=True)
    mlc_bank_swap: Mapped[str] = Column("MLCBankSwap", String, nullable=True)
    mlc_order_swap: Mapped[str] = Column("MLCOrderSwap", String, nullable=True)
    elekta_relative_mlc_positions: Mapped[int] = Column(
        "ElektaRelativeMLCPositions", Integer, nullable=True
    )

    # One-to-one relationship with Machine
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))
    machine: Mapped["Machine"] = relationship("Machine", back_populates="config_rv")

    def __repr__(self) -> str:
        return f"<ConfigRV(id={self.id}, machine_id={self.machine_id}, enabled={self.enabled}, left_jaw='{self.left_jaw}', right_jaw='{self.right_jaw}', top_jaw='{self.top_jaw}', bottom_jaw='{self.bottom_jaw}')>"

    def __init__(self, **kwargs):
        """
        Initialize a ConfigRV instance.
        Args:
            **kwargs: Arbitrary keyword arguments used to initialize ConfigRV attributes.

        Relationships:
            machine (Machine): The parent Machine to which this ConfigRV belongs (one-to-one).
        """
        super().__init__(**kwargs)


class TolTable(PinnacleBase):
    """
    Represents a tolerance table for a Pinnacle treatment machine.
    """

    __tablename__ = "TolTable"

    # Primary key is inherited from PinnacleBase
    name: Mapped[str] = Column("Name", String, nullable=True)
    number: Mapped[int] = Column("Number", Integer, nullable=True)

    # Foreign key relationship to Machine
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))
    machine: Mapped["Machine"] = relationship(
        "Machine", back_populates="tolerance_table_list"
    )

    def __repr__(self) -> str:
        return f"<TolTable(id={self.id}, name='{self.name}', number={self.number})>"

    def __init__(self, **kwargs):
        """
        Initialize a TolTable instance.
        Args:
            **kwargs: Arbitrary keyword arguments used to initialize TolTable attributes.

        Relationships:
            machine (Machine): The parent Machine to which this TolTable belongs (many-to-one).
        """
        super().__init__(**kwargs)
