"""
SQLAlchemy model for Pinnacle CPManager data.

This module provides the CPManager data models for representing control point manager configuration.
"""

from typing import TYPE_CHECKING, List

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.control_point import ControlPoint
    from pinnacle_io.models.beam import Beam


class CPManager(PinnacleBase):
    """
    Model representing a control point manager
    """

    __tablename__ = "CPManager"

    # Primary key is inherited from PinnacleBase
    is_gantry_start_stop_locked: Mapped[int] = Column(
        "IsGantryStartStopLocked", Integer, nullable=True
    )
    is_couch_start_stop_locked: Mapped[int] = Column(
        "IsCouchStartStopLocked", Integer, nullable=True
    )
    is_collimator_start_stop_locked: Mapped[int] = Column(
        "IsCollimatorStartStopLocked", Integer, nullable=True
    )
    is_left_right_independent: Mapped[int] = Column(
        "IsLeftRightIndependent", Integer, nullable=True
    )
    is_top_bottom_independent: Mapped[int] = Column(
        "IsTopBottomIndependent", Integer, nullable=True
    )
    _number_of_control_points: Mapped[int] = Column(
        "NumberOfControlPoints", Integer, nullable=True
    )
    gantry_is_ccw: Mapped[int] = Column("GantryIsCcw", Integer, nullable=True)
    mlc_push_method: Mapped[str] = Column("MlcPushMethod", String, nullable=True)
    jaws_conformance: Mapped[str] = Column("JawsConformance", String, nullable=True)

    # Parent relationship
    beam_id: Mapped[int] = Column("BeamID", Integer, ForeignKey("Beam.ID"))
    beam: Mapped["Beam"] = relationship("Beam", back_populates="cp_manager")

    # Child relationship
    control_point_list: Mapped[List["ControlPoint"]] = relationship(
        "ControlPoint", back_populates="cp_manager", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        """
        Initialize a CPManager instance.

        Args:
            **kwargs: Keyword arguments used to initialize CPManager attributes.

        Relationships:
            beam (Beam): The parent Beam to which this CPManager belongs (many-to-one).
            control_points (List[ControlPoint]): List of control points managed by this CPManager (one-to-many).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this control point manager.
        """
        beam = self.beam.name if self.beam else ""
        return f"<CPManager(id={self.id}, beam='{beam}', number_of_control_points={self.number_of_control_points})>"

    @property
    def number_of_control_points(self) -> int:
        """
        Get the number of control points.
        """
        return len(self.control_point_list)

    @number_of_control_points.setter
    def number_of_control_points(self, value: int) -> None:
        """
        Set the number of control points. This will not raise an error if different from the actual number of control points.
        """
        self._number_of_control_points = value
