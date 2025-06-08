"""
ControlPoint model for Pinnacle IO.

This module provides the ControlPoint data models for representing beam configuration.
"""

from typing import Optional, Tuple, TYPE_CHECKING
import numpy as np
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.beam import Beam
    from pinnacle_io.models.cp_manager import CPManager
    from pinnacle_io.models.mlc import MLCLeafPositions
    from pinnacle_io.models.wedge_context import WedgeContext


class ControlPoint(PinnacleBase):
    """
    Model representing a beam control point.

    This class stores all control point-specific information needed for DICOM conversion,
    including gantry, collimator, and couch angles, as well as jaw and MLC positions.
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

    def __init__(self, **kwargs):
        """
        Initialize a ControlPoint instance.

        Args:
            **kwargs: Keyword arguments used to initialize ControlPoint attributes.

        Relationships:
            beam (Beam): The parent Beam to which this control point belongs (many-to-one).
            cp_manager (CPManager): The parent CPManager to which this control point belongs (many-to-one).
            _mlc_leaf_positions (MLCLeafPositions): Associated MLC leaf positions (one-to-one).
            wedge_context (WedgeContext): Associated wedge context (one-to-one).
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
            # Import here to avoid circular import
            from pinnacle_io.models.mlc import MLCLeafPositions

            if isinstance(mlc_leaf_positions, MLCLeafPositions):
                self._mlc_leaf_positions = mlc_leaf_positions
            elif isinstance(mlc_leaf_positions, dict):
                self._mlc_leaf_positions = MLCLeafPositions(**mlc_leaf_positions)
            else:
                self._mlc_leaf_positions = MLCLeafPositions(points=mlc_leaf_positions)

    def __repr__(self) -> str:
        """
        Return a string representation of this control point.
        """
        return f"<ControlPoint(id={self.id}, index={self.index}, gantry={self.gantry}, collimator={self.collimator}, couch={self.couch})>"

    @property
    def mlc_leaf_positions(self) -> Optional[np.ndarray]:
        """
        Get the MLC leaf positions.

        Returns:
            Optional[np.ndarray]: The MLC leaf positions.
        """
        if self._mlc_leaf_positions is not None:
            return self._mlc_leaf_positions.points
        return None

    @property
    def has_mlc(self) -> bool:
        """
        Check if this control point has MLC positions.

        Returns:
            True if MLC positions are set, False otherwise.
        """
        return self._mlc_leaf_positions is not None

    def get_jaw_positions(self) -> Tuple[float, float, float, float]:
        """
        Get the jaw positions.

        Returns:
            Tuple of (X1, X2, Y1, Y2) jaw positions in mm.
        """
        return (
            self.left_jaw_position,
            self.right_jaw_position,
            self.top_jaw_position,
            self.bottom_jaw_position,
        )

    def get_field_size(self) -> Tuple[float, float]:
        """
        Get the field size.

        Returns:
            Tuple of (X, Y) field size in mm.

        Raises:
            ValueError: If jaw positions are invalid (left > right or bottom > top)
        """
        if (self.left_jaw_position is not None and self.right_jaw_position is not None and 
            self.left_jaw_position > self.right_jaw_position):
            raise ValueError("Left jaw position cannot be greater than right jaw position")
        
        if (self.bottom_jaw_position is not None and self.top_jaw_position is not None and 
            self.bottom_jaw_position > self.top_jaw_position):
            raise ValueError("Bottom jaw position cannot be greater than top jaw position")
        
        return (
            self.right_jaw_position - self.left_jaw_position,
            self.top_jaw_position - self.bottom_jaw_position,
        )

    @mlc_leaf_positions.setter
    def mlc_leaf_positions(self, value: Optional[np.ndarray]) -> None:
        """
        Set the MLC leaf positions.

        Args:
            value: The MLC leaf positions.

        Raises:
            ValueError: If the MLC positions array has invalid shape
            TypeError: If the input data is not a numpy array or properly formatted dict
        """
        if value is None:
            self._mlc_leaf_positions = None
        else:
            # Import here to avoid circular import
            from pinnacle_io.models.mlc import MLCLeafPositions            # Create new MLCLeafPositions - validation happens in its points setter
            self._mlc_leaf_positions = MLCLeafPositions(points=value)
