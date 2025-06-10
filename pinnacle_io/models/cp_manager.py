"""
SQLAlchemy model for Pinnacle CPManager data.

This module provides the CPManager data model for managing control points in Pinnacle treatment
beams. The CPManager handles the configuration and management of control points for a beam,
including gantry, couch, and collimator movement settings.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List, Any

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.control_point import ControlPoint
    from pinnacle_io.models.beam import Beam


class CPManager(PinnacleBase):
    """
    Model representing a control point manager for a treatment beam.

    This class manages the configuration and collection of control points for a beam,
    including settings for gantry, couch, and collimator movement, as well as MLC and
    jaw configurations.

    Attributes:
        id (int): Primary key
        is_gantry_start_stop_locked (int): Whether gantry start/stop positions are locked
        is_couch_start_stop_locked (int): Whether couch start/stop positions are locked
        is_collimator_start_stop_locked (int): Whether collimator start/stop positions are locked
        is_left_right_independent (int): Whether left/right jaws move independently
        is_top_bottom_independent (int): Whether top/bottom jaws move independently
        _number_of_control_points (int): Number of control points (cached value)
        gantry_is_ccw (int): Gantry rotation direction (1 for counter-clockwise)
        mlc_push_method (str): MLC push method configuration
        jaws_conformance (str): Jaws conformance configuration
        
    Relationships:
        beam (Beam): The parent beam that this manager belongs to
        control_point_list (List[ControlPoint]): List of control points managed by this manager
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

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a CPManager instance.

        Args:
            **kwargs: Keyword arguments used to initialize CPManager attributes.
                Supported keyword arguments include all column names as attributes and:
                - beam: Optional[Beam] - The parent beam
                - control_point_list: Optional[List[ControlPoint]] - List of control points
        """
        # Initialize control point list if provided
        self.control_point_list = kwargs.pop('control_point_list', [])
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this control point manager.

        Returns:
            str: A string representation in the format:
                <CPManager(id=X, beam='beam_name', number_of_control_points=Y)>
        """
        beam_name = getattr(getattr(self, 'beam', ''), 'name', '')
        return (
            f"<CPManager(id={self.id}, "
            f"beam='{beam_name}', "
            f"number_of_control_points={self.number_of_control_points})>"
        )

    @property
    def number_of_control_points(self) -> int:
        """
        Get the number of control points.

        Returns:
            int: The number of control points in the control_point_list.
                Returns 0 if control_point_list is None.
        """
        if not hasattr(self, 'control_point_list') or self.control_point_list is None:
            return 0
        return len(self.control_point_list)

    @number_of_control_points.setter
    def number_of_control_points(self, value: int) -> None:
        """
        Set the number of control points.

        Args:
            value (int): The number of control points to set.
                This updates the cached value but doesn't modify the actual control point list.

        Note:
            This method only updates the cached value and doesn't modify the actual
            control points list. Use with caution as it may cause inconsistency.
        """
        if not isinstance(value, int) or value < 0:
            raise ValueError("Number of control points must be a non-negative integer")
        self._number_of_control_points = value
        
    def add_control_point(self, control_point: 'ControlPoint') -> None:
        """
        Add a control point to this manager.

        Args:
            control_point: The ControlPoint instance to add.
                The control point will be associated with this manager.
                
        Raises:
            TypeError: If control_point is not a ControlPoint instance
            ValueError: If the control point is already associated with another manager
        """
        if not isinstance(control_point, ControlPoint):
            raise TypeError("control_point must be an instance of ControlPoint")
            
        if control_point in self.control_point_list:
            return  # Already in the list
            
        if control_point.cp_manager is not None and control_point.cp_manager is not self:
            raise ValueError("Control point is already associated with another manager")
            
        self.control_point_list.append(control_point)
        control_point.cp_manager = self
        
    def remove_control_point(self, control_point: 'ControlPoint') -> None:
        """
        Remove a control point from this manager.
        
        Args:
            control_point: The ControlPoint instance to remove.
            
        Returns:
            bool: True if the control point was removed, False if it wasn't found
        """
        if control_point in self.control_point_list:
            self.control_point_list.remove(control_point)
            control_point.cp_manager = None
            return True
        return False
