"""
SQLAlchemy models for Multi-Leaf Collimator (MLC) data in Pinnacle.

This module provides comprehensive models for representing MLC configurations,
leaf positions, and leaf pair data in the Pinnacle treatment planning system.
The models handle both static MLC configurations and dynamic leaf position data
for treatment delivery.
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
    from pinnacle_io.models.control_point import ControlPoint


class MLCLeafPositions(PinnacleBase):
    """
    Model representing Multi-Leaf Collimator (MLC) leaf positions for control points.

    This class stores the precise positions of MLC leaves at specific control points
    during treatment delivery. It handles the serialization and deserialization of
    leaf position data, converting between the database storage format (int16 millimeters)
    and the application format (float32 centimeters) for optimal storage efficiency
    and computational precision.

    The MLC leaf positions are critical for intensity-modulated radiation therapy (IMRT)
    and volumetric modulated arc therapy (VMAT) treatments, where the leaf positions
    change dynamically during beam delivery to create complex dose distributions.

    Attributes:
        id (int): Primary key inherited from PinnacleBase
        number_of_dimensions (int): Number of spatial dimensions (typically 2 for X,Y)
        number_of_points (int): Number of leaf pairs (typically 60 for modern MLCs)
        control_point_id (int): Foreign key to the parent ControlPoint

    Properties:
        points (np.ndarray): Leaf positions in centimeters as a float32 array
                           Shape: (number_of_points, number_of_dimensions)

    Relationships:
        control_point (ControlPoint): The parent control point that owns these positions (many-to-one)

    Storage Details:
        The leaf positions are stored in the database as binary data (_points_data) using
        int16 values representing millimeters. This provides sufficient precision (0.1mm)
        while minimizing storage space. The positions are automatically converted to/from
        centimeters when accessed through the points property.

    Example:
        >>> positions = MLCLeafPositions(
        ...     number_of_dimensions=2,
        ...     number_of_points=60,
        ...     points=np.zeros((60, 2), dtype=np.float32)
        ... )
        >>> positions.points[0, 0] = -5.0  # Left leaf at -5.0 cm
        >>> positions.points[0, 1] = 5.0   # Right leaf at 5.0 cm
    """

    __tablename__ = "MLCLeafPositions"

    number_of_dimensions: Mapped[Optional[int]] = Column("NumberOfDimensions", Integer, nullable=True)
    number_of_points: Mapped[Optional[int]] = Column("NumberOfPoints", Integer, nullable=True)

    # For storing serialized points data as int16 values (millimeters)
    _points_data: Mapped[Optional[bytes]] = Column(
        "PointsData", LargeBinary, nullable=True
    )

    # Parent relationships
    control_point_id: Mapped[Optional[int]] = Column(
        "ControlPointID", Integer, ForeignKey("ControlPoint.ID"), nullable=True
    )
    control_point: Mapped[Optional["ControlPoint"]] = relationship(
        "ControlPoint",
        back_populates="_mlc_leaf_positions",
        lazy="selectin"  # Use selectin loading for better performance
    )

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
        """
        Return a string representation of this MLC leaf positions.
        """
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
    Represents a single leaf pair in a Multi-Leaf Collimator (MLC) system.

    Each leaf pair consists of two opposing leaves that can move independently
    to create complex aperture shapes for radiation therapy. This class stores
    the physical and geometric properties of a leaf pair, including its position,
    dimensions, travel limits, and leakage characteristics.

    The leaf pair configuration is essential for accurate dose calculation and
    treatment delivery verification, as it defines the mechanical constraints
    and physical properties that affect radiation transmission and leakage.

    Attributes:
        id (int): Primary key inherited from PinnacleBase
        y_center_position (float): Y-coordinate of the leaf pair center in cm
        negate_leaf_coordinate (int): Flag to negate leaf coordinates (1=yes, 0=no)
        width (float): Width of the leaf pair in cm (leaf thickness)
        min_tip_position (float): Minimum leaf tip position in cm
        max_tip_position (float): Maximum leaf tip position in cm
        side_leakage_width (float): Width of side leakage region in cm
        tip_leakage_width (float): Width of tip leakage region in cm
        multi_leaf_id (int): Foreign key to the parent MultiLeaf configuration

    Relationships:
        multi_leaf (MultiLeaf): The parent MLC configuration that owns this leaf pair (many-to-one)

    Physical Properties:
        The leaf pair defines the mechanical and dosimetric properties of MLC leaves:
        - Position constraints (min/max tip positions)
        - Geometric dimensions (width, center position)
        - Leakage characteristics (side and tip leakage)
        - Coordinate system orientation (negate flag)

    Example:
        >>> leaf_pair = MLCLeafPair(
        ...     y_center_position=-19.5,
        ...     width=1.0,
        ...     min_tip_position=-20.0,
        ...     max_tip_position=20.0,
        ...     side_leakage_width=0.1,
        ...     tip_leakage_width=0.1
        ... )
    """

    __tablename__ = "MLCLeafPair"

    y_center_position: Mapped[Optional[float]] = Column("YCenterPosition", Float, nullable=True)
    negate_leaf_coordinate: Mapped[Optional[int]] = Column("NegateLeafCoordinate", Integer, nullable=True)
    width: Mapped[Optional[float]] = Column("Width", Float, nullable=True)
    min_tip_position: Mapped[Optional[float]] = Column("MinTipPosition", Float, nullable=True)
    max_tip_position: Mapped[Optional[float]] = Column("MaxTipPosition", Float, nullable=True)
    side_leakage_width: Mapped[Optional[float]] = Column("SideLeakageWidth", Float, nullable=True)
    tip_leakage_width: Mapped[Optional[float]] = Column("TipLeakageWidth", Float, nullable=True)

    # Foreign key relationship to MultiLeaf
    multi_leaf_id: Mapped[int] = Column(Integer, ForeignKey("MultiLeaf.ID"))
    multi_leaf: Mapped["MultiLeaf"] = relationship(
        "MultiLeaf",
        back_populates="leaf_pair_list",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __repr__(self) -> str:
        """
        Return a string representation of this MLC leaf pair.
        """
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
    Model representing the Multi-Leaf Collimator (MLC) configuration for a treatment machine.

    This class stores the comprehensive configuration of an MLC system, including
    physical properties, mechanical constraints, and operational parameters. The MLC
    is a critical component of modern linear accelerators that enables precise beam
    shaping for intensity-modulated radiation therapy (IMRT) and volumetric modulated
    arc therapy (VMAT) treatments.

    The MultiLeaf model serves as the central configuration hub for all MLC-related
    parameters, defining how the leaf system behaves during treatment planning and
    delivery. It manages the relationship between the machine and individual leaf
    pairs, ensuring consistent and accurate beam modulation.

    Attributes:
        id (int): Primary key inherited from PinnacleBase
        left_bank_name (str): Name identifier for the left leaf bank (e.g., "B", "Left")
        right_bank_name (str): Name identifier for the right leaf bank (e.g., "A", "Right")
        leaf_x_base_position (float): Base X position for leaf coordinate system in cm
        max_overall_leaf_difference (float): Maximum allowed difference between opposing leaves in cm
        min_static_leaf_gap (float): Minimum gap between opposing leaves for static fields in cm
        min_dynamic_leaf_gap (float): Minimum gap between opposing leaves for dynamic fields in cm
        opposing_adjacent_leaves_can_overlap (int): Flag allowing adjacent leaf overlap (1=yes, 0=no)
        tongue_and_groove_leakage_width (float): Width of tongue-and-groove leakage region in cm
        tip_leakage_radius (float): Radius of leaf tip leakage region in cm
        rounded_leaf_mlc (int): Flag indicating rounded leaf tips (1=yes, 0=no)
        inter_leaf_leakage_trans (float): Inter-leaf transmission leakage factor
        replaces_jaw (int): Flag indicating if MLC replaces jaw collimation (1=yes, 0=no)
        negate_leaf_coordinates (int): Flag to negate leaf coordinate system (1=yes, 0=no)
        aligned_with_left_right_jaw (int): Flag for jaw alignment (1=yes, 0=no)
        mlc_tracks_jaw_for_open_fields (str): MLC jaw tracking behavior for open fields
        source_to_mlc_distance (float): Distance from radiation source to MLC in cm
        thickness (float): Physical thickness of MLC leaves in cm
        decimal_places (int): Number of decimal places for leaf position precision
        vendor (str): MLC manufacturer/vendor name
        has_carriage (int): Flag indicating carriage-based MLC system (1=yes, 0=no)
        max_tip_position_from_jaw (float): Maximum leaf tip position relative to jaw in cm
        default_max_leaf_speed (float): Default maximum leaf speed in cm/s
        default_max_leaf_speed_mu (float): Default maximum leaf speed per MU in cm/MU
        open_extra_leaf_pairs (int): Number of extra leaf pairs to open for field margins
        default_leaf_position_tolerance (float): Default tolerance for leaf positioning in cm
        jaws_conformance (str): Jaw conformance behavior setting
        min_leaf_jaw_overlap (float): Minimum required overlap between leaves and jaws in cm
        max_leaf_jaw_overlap (float): Maximum allowed overlap between leaves and jaws in cm
        machine_id (int): Foreign key to the parent Machine

    Relationships:
        machine (Machine): The parent treatment machine that owns this MLC (one-to-one)
        leaf_pair_list (List[MLCLeafPair]): List of individual leaf pair configurations (one-to-many)

    Example:
        >>> mlc = MultiLeaf(
        ...     left_bank_name="B",
        ...     right_bank_name="A",
        ...     leaf_x_base_position=60.0,
        ...     min_static_leaf_gap=0.5,
        ...     source_to_mlc_distance=50.0,
        ...     vendor="Varian"
        ... )
    """

    __tablename__ = "MultiLeaf"

    # Primary key is inherited from PinnacleBase
    left_bank_name: Mapped[Optional[str]] = Column("LeftBankName", String, nullable=True)
    right_bank_name: Mapped[Optional[str]] = Column("RightBankName", String, nullable=True)
    leaf_x_base_position: Mapped[Optional[float]] = Column("LeafXBasePosition", Float, nullable=True)
    max_overall_leaf_difference: Mapped[Optional[float]] = Column(
        "MaxOverallLeafDifference", Float, nullable=True
    )
    min_static_leaf_gap: Mapped[Optional[float]] = Column("MinStaticLeafGap", Float, nullable=True)
    min_dynamic_leaf_gap: Mapped[Optional[float]] = Column("MinDynamicLeafGap", Float, nullable=True)
    opposing_adjacent_leaves_can_overlap: Mapped[Optional[int]] = Column(
        "OpposingAdjacentLeavesCanOverlap", Integer, nullable=True
    )
    tongue_and_groove_leakage_width: Mapped[Optional[float]] = Column(
        "TongueAndGrooveLeakageWidth", Float, nullable=True
    )
    tip_leakage_radius: Mapped[Optional[float]] = Column("TipLeakageRadius", Float, nullable=True)
    rounded_leaf_mlc: Mapped[Optional[int]] = Column("RoundedLeafMLC", Integer, nullable=True)
    inter_leaf_leakage_trans: Mapped[Optional[float]] = Column("InterLeafLeakageTrans", Float, nullable=True)
    replaces_jaw: Mapped[Optional[int]] = Column("ReplacesJaw", Integer, nullable=True)
    negate_leaf_coordinates: Mapped[Optional[int]] = Column("NegateLeafCoordinates", Integer, nullable=True)
    aligned_with_left_right_jaw: Mapped[Optional[int]] = Column(
        "AlignedWithLeftRightJaw", Integer, nullable=True
    )
    mlc_tracks_jaw_for_open_fields: Mapped[Optional[str]] = Column(
        "MLCTracksJawForOpenFields", String, nullable=True
    )
    source_to_mlc_distance: Mapped[Optional[float]] = Column("SourceToMLCDistance", Float, nullable=True)
    thickness: Mapped[Optional[float]] = Column("Thickness", Float, nullable=True)
    decimal_places: Mapped[Optional[int]] = Column("DecimalPlaces", Integer, nullable=True)
    vendor: Mapped[Optional[str]] = Column("Vendor", String, nullable=True)
    has_carriage: Mapped[Optional[int]] = Column("HasCarriage", Integer, nullable=True)
    max_tip_position_from_jaw: Mapped[Optional[float]] = Column("MaxTipPositionFromJaw", Float, nullable=True)
    default_max_leaf_speed: Mapped[Optional[float]] = Column("DefaultMaxLeafSpeed", Float, nullable=True)
    default_max_leaf_speed_mu: Mapped[Optional[float]] = Column("DefaultMaxLeafSpeedMU", Float, nullable=True)
    open_extra_leaf_pairs: Mapped[Optional[int]] = Column("OpenExtraLeafPairs", Integer, nullable=True)
    default_leaf_position_tolerance: Mapped[Optional[float]] = Column(
        "DefaultLeafPositionTolerance", Float, nullable=True
    )
    jaws_conformance: Mapped[Optional[str]] = Column("JawsConformance", String, nullable=True)
    min_leaf_jaw_overlap: Mapped[Optional[float]] = Column("MinLeafJawOverlap", Float, nullable=True)
    max_leaf_jaw_overlap: Mapped[Optional[float]] = Column("MaxLeafJawOverlap", Float, nullable=True)

    # One-to-one relationship with Machine
    machine_id: Mapped[int] = Column(Integer, ForeignKey("Machine.ID"))
    machine: Mapped["Machine"] = relationship(
        "Machine",
        back_populates="multi_leaf",
        lazy="selectin"  # Use selectin loading for better performance
    )

    # One-to-many relationship with LeafPairList
    leaf_pair_list: Mapped[List["MLCLeafPair"]] = relationship(
        "MLCLeafPair",
        back_populates="multi_leaf",
        cascade="all, delete-orphan",
        lazy="selectin"  # Use selectin loading for better performance
    )

    def __init__(self, **kwargs):
        """
        Initialize a MultiLeaf instance.

        This constructor handles initialization of all MLC configuration attributes
        and relationships. It supports both direct attribute assignment and nested
        relationship creation through dictionaries for leaf pair configurations.

        Args:
            **kwargs: Keyword arguments used to initialize MultiLeaf attributes.
                Can include any of the MLC configuration attributes as well as
                relationship data for child objects.

        Relationship Parameters:
            machine (dict or Machine): Parent machine configuration data
            leaf_pair_list (list): List of leaf pair data (dicts or MLCLeafPair objects)

        Example:
            >>> mlc = MultiLeaf(
            ...     left_bank_name="B",
            ...     right_bank_name="A",
            ...     source_to_mlc_distance=50.0,
            ...     leaf_pair_list=[
            ...         {"y_center_position": -19.5, "width": 1.0},
            ...         {"y_center_position": -18.5, "width": 1.0}
            ...     ]
            ... )
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this MLC configuration.
        """
        return f"<MultiLeaf(id={self.id}, machine_id={self.machine_id}, machine.name={self.machine.name if self.machine else 'None'})>"
