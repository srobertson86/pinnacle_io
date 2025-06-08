"""
MLCLeafPositions model for Pinnacle IO.

This module provides the MLCLeafPositions data models for representing beam configuration.
"""

from typing import Optional, ClassVar, List, TYPE_CHECKING
import numpy as np
import struct
import warnings
from sqlalchemy import Column, Integer, ForeignKey, LargeBinary, Float, String
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.machine import Machine


class MLCLeafPositions(PinnacleBase):
    """
    Model representing the MLC leaf positions for control points
    """

    __tablename__ = "MLCLeafPositions"

    number_of_dimensions: Mapped[int] = Column("NumberOfDimensions", Integer, nullable=True)
    number_of_points: Mapped[int] = Column("NumberOfPoints", Integer, nullable=True)

    # For storing serialized points data as int16 values (millimeters)
    _points_data: Mapped[Optional[bytes]] = Column(
        "PointsData", LargeBinary, nullable=True
    )

    # Parent relationships
    control_point_id: Mapped[Optional[int]] = Column(
        "ControlPointID", Integer, ForeignKey("ControlPoint.ID"), nullable=True
    )
    control_point = relationship("ControlPoint", back_populates="_mlc_leaf_positions")

    # Transient attributes (not stored in database)
    _points: ClassVar[Optional[np.ndarray]] = None

    def __init__(self, **kwargs):
        """
        Initialize a MLCLeafPositions instance.

        Args:
            **kwargs: Keyword arguments used to initialize MLCLeafPositions attributes.

        Relationships:
            control_point (ControlPoint): The parent ControlPoint to which this MLCLeafPositions belongs (many-to-one).
        """
        # Handle points if provided
        points = kwargs.pop("points", None)

        super().__init__(**kwargs)

        if points is not None:
            self.points = points

    def __repr__(self) -> str:
        return f"<MLCLeafPositions(id={self.id}, points={self.number_of_points})>"

    @property
    def points(self) -> Optional[np.ndarray]:
        """
        Get the points data in centimeters (float).

        Returns:
            Optional[np.ndarray]: The points data in centimeters (float).
        """
        if self._points is None and self._points_data is not None:
            # Deserialize from database (int16 millimeters -> float centimeters)
            # Determine the shape based on dimensions and number of points
            if self.number_of_dimensions > 0 and self.number_of_points > 0:
                total_elements = self.number_of_dimensions * self.number_of_points
                # Check if the buffer size matches the expected size
                expected_bytes = total_elements * 2  # int16 = 2 bytes
                actual_bytes = len(self._points_data)
                if expected_bytes != actual_bytes:
                    warnings.warn(
                        f"MLCLeafPositions: Buffer size mismatch (expected {expected_bytes} bytes, got {actual_bytes} bytes). "
                        "Resetting number_of_dimensions to 2."
                    )
                    self.number_of_dimensions = 2
                    total_elements = self.number_of_dimensions * self.number_of_points
                    expected_bytes = total_elements * 2
                    if expected_bytes != actual_bytes:
                        raise ValueError(
                            f"MLCLeafPositions: Buffer size still mismatched after resetting dimensions. "
                            f"Expected {expected_bytes} bytes, got {actual_bytes} bytes."
                        )
                int_values = struct.unpack(f"<{total_elements}h", self._points_data)
                mm_array = np.array(int_values, dtype=np.int16)
                reshaped_array = mm_array.reshape(
                    self.number_of_points, self.number_of_dimensions
                )
                self._points = reshaped_array.astype(np.float32) / 10.0
        return self._points

    @points.setter
    def points(self, value: Optional[np.ndarray]) -> None:
        """
        Set the points data in centimeters (float) and serialize to millimeters (int16).

        Args:
            value: The points data in centimeters (float) as a numpy array.
                  Will attempt to convert non-array inputs to numpy arrays.

        Raises:
            ValueError: If the MLC positions array has invalid shape
            TypeError: If the input cannot be converted to a numpy array
        """
        if value is None:
            self._points = None
            self._points_data = None
            self.number_of_dimensions = 0
            self.number_of_points = 0
            return

        # Convert to numpy array if not already
        if not isinstance(value, np.ndarray):
            try:
                value = np.array(value, dtype=np.float32)
            except (ValueError, TypeError) as e:
                raise TypeError(f"Could not convert input to numpy array: {e}")

        # Validate shape
        if value.shape[0] != 60 or value.shape[1] != 2:
            raise ValueError("MLC positions must be a 60x2 array")

        self._points = value
        self.number_of_dimensions = 2
        self.number_of_points = value.shape[0]

        # Convert from centimeters (float) to millimeters (int16)
        mm_values = np.round(value * 10).astype(np.int16)

        # Ensure values are within the valid range (-200 to 200)
        np.clip(mm_values, -200, 200, out=mm_values)

        # Serialize to binary
        self._points_data = struct.pack(f"<{mm_values.size}h", *mm_values.flatten())


class MLCLeafPair(PinnacleBase):
    """
    Represents a leaf pair for a Pinnacle treatment machine.
    """

    __tablename__ = "MLCLeafPair"

    y_center_position: Mapped[float] = Column("YCenterPosition", Float, nullable=True)
    negate_leaf_coordinate: Mapped[int] = Column("NegateLeafCoordinate", Integer, nullable=True)
    width: Mapped[float] = Column("Width", Float, nullable=True)
    min_tip_position: Mapped[float] = Column("MinTipPosition", Float, nullable=True)
    max_tip_position: Mapped[float] = Column("MaxTipPosition", Float, nullable=True)
    side_leakage_width: Mapped[float] = Column("SideLeakageWidth", Float, nullable=True)
    tip_leakage_width: Mapped[float] = Column("TipLeakageWidth", Float, nullable=True)

    # Foreign key relationship to MultiLeaf
    multi_leaf_id: Mapped[int] = Column(Integer, ForeignKey("MultiLeaf.ID"))
    multi_leaf: Mapped["MultiLeaf"] = relationship(
        "MultiLeaf", back_populates="leaf_pair_list"
    )

    def __repr__(self) -> str:
        return f"<MLCLeafPair(id={self.id}, width={self.width}, y_center_position={self.y_center_position})>"

    def __init__(self, **kwargs):
        """
        Initialize a MLCLeafPair instance.

        Args:
            **kwargs: Keyword arguments used to initialize MLCLeafPair attributes.

        Relationships:
            multi_leaf (MultiLeaf): The parent MultiLeaf to which this MLCLeafPair belongs (many-to-one).
        """
        super().__init__(**kwargs)


class MultiLeaf(PinnacleBase):
    """
    Represents the multi-leaf collimator (MLC) configuration for a Pinnacle
    treatment machine.
    """

    __tablename__ = "MultiLeaf"

    # Primary key is inherited from PinnacleBase
    left_bank_name: Mapped[str] = Column("LeftBankName", String, nullable=True)
    right_bank_name: Mapped[str] = Column("RightBankName", String, nullable=True)
    leaf_x_base_position: Mapped[float] = Column("LeafXBasePosition", Float, nullable=True)
    max_overall_leaf_difference: Mapped[float] = Column(
        "MaxOverallLeafDifference", Float, nullable=True
    )
    min_static_leaf_gap: Mapped[float] = Column("MinStaticLeafGap", Float, nullable=True)
    min_dynamic_leaf_gap: Mapped[float] = Column("MinDynamicLeafGap", Float, nullable=True)
    opposing_adjacent_leaves_can_overlap: Mapped[int] = Column(
        "OpposingAdjacentLeavesCanOverlap", Integer, nullable=True
    )
    tongue_and_groove_leakage_width: Mapped[float] = Column(
        "TongueAndGrooveLeakageWidth", Float, nullable=True
    )
    tip_leakage_radius: Mapped[float] = Column("TipLeakageRadius", Float, nullable=True)
    rounded_leaf_mlc: Mapped[int] = Column("RoundedLeafMLC", Integer, nullable=True)
    inter_leaf_leakage_trans: Mapped[float] = Column("InterLeafLeakageTrans", Float, nullable=True)
    replaces_jaw: Mapped[int] = Column("ReplacesJaw", Integer, nullable=True)
    negate_leaf_coordinates: Mapped[int] = Column("NegateLeafCoordinates", Integer, nullable=True)
    aligned_with_left_right_jaw: Mapped[int] = Column(
        "AlignedWithLeftRightJaw", Integer, nullable=True
    )
    mlc_tracks_jaw_for_open_fields: Mapped[str] = Column(
        "MLCTracksJawForOpenFields", String, nullable=True
    )
    source_to_mlc_distance: Mapped[float] = Column("SourceToMLCDistance", Float, nullable=True)
    thickness: Mapped[float] = Column("Thickness", Float, nullable=True)
    decimal_places: Mapped[int] = Column("DecimalPlaces", Integer, nullable=True)
    vendor: Mapped[str] = Column("Vendor", String, nullable=True)
    has_carriage: Mapped[int] = Column("HasCarriage", Integer, nullable=True)
    max_tip_position_from_jaw: Mapped[float] = Column("MaxTipPositionFromJaw", Float, nullable=True)
    default_max_leaf_speed: Mapped[float] = Column("DefaultMaxLeafSpeed", Float, nullable=True)
    default_max_leaf_speed_mu: Mapped[float] = Column("DefaultMaxLeafSpeedMU", Float, nullable=True)
    open_extra_leaf_pairs: Mapped[int] = Column("OpenExtraLeafPairs", Integer, nullable=True)
    default_leaf_position_tolerance: Mapped[float] = Column(
        "DefaultLeafPositionTolerance", Float, nullable=True
    )
    jaws_conformance: Mapped[str] = Column("JawsConformance", String, nullable=True)
    min_leaf_jaw_overlap: Mapped[float] = Column("MinLeafJawOverlap", Float, nullable=True)
    max_leaf_jaw_overlap: Mapped[float] = Column("MaxLeafJawOverlap", Float, nullable=True)

    # One-to-one relationship with Machine
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))
    machine: Mapped["Machine"] = relationship("Machine", back_populates="multi_leaf")

    # One-to-one relationship with LeafPairList
    leaf_pair_list: Mapped[List["MLCLeafPair"]] = relationship(
        "MLCLeafPair", back_populates="multi_leaf", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        """
        Initialize a MultiLeaf instance.

        Args:
            **kwargs: Keyword arguments used to initialize MultiLeaf attributes.

        Relationships:
            machine (Machine): The parent Machine to which this MultiLeaf belongs (one-to-one).
            leaf_pair_list (List[MLCLeafPair]): List of MLCLeafPair objects associated with this MultiLeaf (one-to-many).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<MultiLeaf(id={self.id}, machine_id={self.machine_id}, machine.name={self.machine.name if self.machine else 'None'})>"
