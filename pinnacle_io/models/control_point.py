"""
SQLAlchemy model for Pinnacle Control Point data.

This module provides the ControlPoint data model for representing control points in
Pinnacle treatment beams, including all control point-specific parameters and relationships
to other beam components like MLCs and wedges.
"""

from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING, Any, Dict, Union

import numpy as np
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.beam import Beam
    from pinnacle_io.models.cp_manager import CPManager
    from pinnacle_io.models.mlc import MLCLeafPositions
    from pinnacle_io.models.wedge_context import WedgeContext


# Type alias for MLC leaf positions input
try:
    MLCInputType = Union[np.ndarray, Dict[str, Any], 'MLCLeafPositions']
except NameError:
    MLCInputType = Any  # Fallback for runtime


class ControlPoint(PinnacleBase):
    """
    Model representing a control point in a treatment beam.

    This class stores all control point-specific information including machine parameters,
    jaw positions, and MLC leaf positions needed for treatment delivery. Each control
    point represents a snapshot of the beam's state during delivery.

    Attributes:
        id (int): Primary key
        index (int): Index of this control point in the beam's control point sequence
        gantry (float): Gantry angle in degrees
        collimator (float): Collimator angle in degrees
        couch (float): Couch angle in degrees
        left_jaw_position (float): Left jaw position in mm
        right_jaw_position (float): Right jaw position in mm
        top_jaw_position (float): Top jaw position in mm
        bottom_jaw_position (float): Bottom jaw position in mm
        weight (float): Weight of this control point
        dose_rate (float): Dose rate in MU/min
        delivery_time (float): Delivery time in seconds
        
    Relationships:
        beam (Beam): Parent beam that this control point belongs to
        cp_manager (CPManager): Manager for control point data
        _mlc_leaf_positions (MLCLeafPositions): MLC leaf positions for this control point
        wedge_context (WedgeContext): Wedge parameters for this control point
    """

    __tablename__ = "ControlPoint"

    index: Mapped[int] = Column(
        "Index", Integer, nullable=True
    )  # Not part of the Pinnacle plan.Trial file
    gantry: Mapped[Optional[float]] = Column("Gantry", Float, nullable=True)
    couch: Mapped[Optional[float]] = Column("Couch", Float, nullable=True)
    collimator: Mapped[Optional[float]] = Column("Collimator", Float, nullable=True)
    left_jaw_position: Mapped[Optional[float]] = Column(
        "LeftJawPosition", Float, nullable=True
    )
    right_jaw_position: Mapped[Optional[float]] = Column(
        "RightJawPosition", Float, nullable=True
    )
    top_jaw_position: Mapped[Optional[float]] = Column(
        "TopJawPosition", Float, nullable=True
    )
    bottom_jaw_position: Mapped[Optional[float]] = Column(
        "BottomJawPosition", Float, nullable=True
    )
    weight: Mapped[Optional[float]] = Column("Weight", Float, nullable=True)
    weight_locked: Mapped[Optional[int]] = Column(
        "WeightLocked", Integer, nullable=True
    )
    percent_of_arc: Mapped[Optional[float]] = Column(
        "PercentOfArc", Float, nullable=True
    )
    has_shared_modifier_list: Mapped[Optional[int]] = Column(
        "HasSharedModifierList", Integer, nullable=True
    )
    mlc_trans_for_display: Mapped[Optional[float]] = Column(
        "MLCTransForDisplay", Float, nullable=True
    )
    c_arm_angle: Mapped[Optional[float]] = Column("CArmAngle", Float, nullable=True)
    target_projection_valid: Mapped[Optional[int]] = Column(
        "TargetProjectionValid", Integer, nullable=True
    )
    dose_rate: Mapped[Optional[float]] = Column("DoseRate", Float, nullable=True)
    delivery_time: Mapped[Optional[float]] = Column(
        "DeliveryTime", Float, nullable=True
    )
    odm: Mapped[Optional[str]] = Column("ODM", String, nullable=True)
    dose_vector: Mapped[Optional[str]] = Column("DoseVector", String, nullable=True)
    cumulative_meterset_weight: Mapped[Optional[float]] = Column(
        "CumulativeMeterset", Float, nullable=True
    )

    # Parent relationships. Control points are saved in Pinnacle under the Beam -> CPManager.
    # For convenience, control points are also associated with the Beam model directly
    beam_id: Mapped[Optional[int]] = Column(
        "BeamID", Integer, ForeignKey("Beam.ID"), nullable=True
    )
    beam: Mapped[Optional["Beam"]] = relationship("Beam", back_populates="control_point_list")
    
    cp_manager_id: Mapped[Optional[int]] = Column(
        "CPManagerID", Integer, ForeignKey("CPManager.ID"), nullable=True
    )
    cp_manager: Mapped[Optional["CPManager"]] = relationship(
        "CPManager", 
        back_populates="control_point_list"
    )

    # Child relationships
    _mlc_leaf_positions: Mapped[Optional["MLCLeafPositions"]] = relationship(
        "MLCLeafPositions",
        back_populates="control_point",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    wedge_context: Mapped[Optional["WedgeContext"]] = relationship(
        "WedgeContext",
        back_populates="control_point",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a ControlPoint instance.

        Args:
            **kwargs: Keyword arguments used to initialize ControlPoint attributes.
                Supported keyword arguments include all column names as attributes and:
                - mlc_leaf_positions: Optional[MLCInputType]
                - cp_manager: Optional[CPManager]
                - beam: Optional[Beam]
        """
        # Handle mlc_leaf_positions if provided
        mlc_leaf_positions = kwargs.pop(
            "mlc_leaf_positions", kwargs.pop("MLCLeafPositions", None)
        )

        # Get cp_manager before super init to handle relationship
        cp_manager = kwargs.get('cp_manager')
        if cp_manager is not None and not kwargs.get('beam'):
            # If cp_manager is provided but beam isn't, use the beam from cp_manager
            kwargs['beam'] = cp_manager.beam
        
        super().__init__(**kwargs)

        # Create related objects after initialization if provided
        if mlc_leaf_positions is not None:
            self._set_mlc_leaf_positions(mlc_leaf_positions)

    def __repr__(self) -> str:
        """
        Return a string representation of this control point.
        """
        return f"<ControlPoint(id={self.id}, index={self.index}, gantry={self.gantry}, collimator={self.collimator}, couch={self.couch})>"

    @property
    def mlc_leaf_positions(self) -> Optional[np.ndarray]:
        """
        Get the MLC leaf positions as a numpy array.

        Returns:
            Optional[np.ndarray]: A numpy array containing the MLC leaf positions in mm,
                or None if no MLC positions are set.
                Shape is (n_leaves, 2) where the second dimension contains [leaf_left, leaf_right]
                positions relative to the central axis.
        """
        if self._mlc_leaf_positions is not None:
            return self._mlc_leaf_positions.points
        return None

    @property
    def has_mlc(self) -> bool:
        """
        Check if this control point has MLC positions defined.

        Returns:
            bool: True if MLC positions are set, False otherwise.
        """
        return self._mlc_leaf_positions is not None and self._mlc_leaf_positions.points is not None

    def get_jaw_positions(self) -> Tuple[float, float, float, float]:
        """
        Get the jaw positions in the standard DICOM coordinate system.

        Returns:
            Tuple[float, float, float, float]: A tuple containing (X1, X2, Y1, Y2) jaw
                positions in mm, where:
                - X1: Left jaw position (negative from isocenter)
                - X2: Right jaw position (positive from isocenter)
                - Y1: Bottom jaw position (negative from isocenter)
                - Y2: Top jaw position (positive from isocenter)

        Note:
            All positions are in the DICOM coordinate system with the beam's eye view.
        """
        return (
            self.left_jaw_position or 0.0,
            self.right_jaw_position or 0.0,
            self.bottom_jaw_position or 0.0,
            self.top_jaw_position or 0.0,
        )

    def get_field_size(self) -> Tuple[float, float]:
        """
        Calculate the field size defined by the jaw positions.

        Returns:
            Tuple[float, float]: A tuple containing (width, height) in mm.

        Raises:
            ValueError: If jaw positions are invalid (left > right or bottom > top)
            RuntimeError: If any jaw position is None
            
        Example:
            >>> cp = ControlPoint(
            ...     left_jaw_position=-50,
            ...     right_jaw_position=50,
            ...     bottom_jaw_position=-40,
            ...     top_jaw_position=40
            ... )
            >>> cp.get_field_size()
            (100.0, 80.0)
        """
        if None in (self.left_jaw_position, self.right_jaw_position,
                   self.bottom_jaw_position, self.top_jaw_position):
            raise RuntimeError("Cannot calculate field size: one or more jaw positions are None")
            
        if self.left_jaw_position > self.right_jaw_position:
            raise ValueError(
                f"Invalid jaw positions: left ({self.left_jaw_position}) > "
                f"right ({self.right_jaw_position})"
            )
            
        if self.bottom_jaw_position > self.top_jaw_position:
            raise ValueError(
                f"Invalid jaw positions: bottom ({self.bottom_jaw_position}) > "
                f"top ({self.top_jaw_position})"
            )
            
        return (
            self.right_jaw_position - self.left_jaw_position,
            self.top_jaw_position - self.bottom_jaw_position,
        )

    def _set_mlc_leaf_positions(self, value: MLCInputType) -> None:
        """
        Internal method to set MLC leaf positions with proper type handling.

        Args:
            value: The MLC leaf positions. Can be:
                - MLCLeafPositions instance
                - numpy array of shape (n_leaves, 2)
                - dict with MLC parameters

        Raises:
            ValueError: If the MLC positions array has invalid shape
            TypeError: If the input data is not a supported type
        """
        from pinnacle_io.models.mlc import MLCLeafPositions

        if value is None:
            self._mlc_leaf_positions = None
        elif isinstance(value, MLCLeafPositions):
            self._mlc_leaf_positions = value
        elif isinstance(value, dict):
            self._mlc_leaf_positions = MLCLeafPositions(**value)
        else:
            # Assume it's a numpy array or compatible sequence
            self._mlc_leaf_positions = MLCLeafPositions(points=value)

    @mlc_leaf_positions.setter
    def mlc_leaf_positions(self, value: Optional[np.ndarray]) -> None:
        """
        Set the MLC leaf positions from a numpy array.

        Args:
            value: The MLC leaf positions as a numpy array of shape (n_leaves, 2).
                Each row should contain [left_leaf, right_leaf] positions in mm.

        Raises:
            ValueError: If the MLC positions array has invalid shape
            TypeError: If the input is not a numpy array or None
        """
        self._set_mlc_leaf_positions(value)
