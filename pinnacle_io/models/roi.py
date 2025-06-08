"""
ROI model for Pinnacle IO.

This module provides the ROI data model for representing structure set information.
"""

from typing import Optional, List, Union, TYPE_CHECKING

import numpy as np
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase
from pinnacle_io.models.plan import Plan

if TYPE_CHECKING:
    from pinnacle_io.models.plan import Plan


class Curve(PinnacleBase):
    """
    Model representing a single curve within an ROI.

    This class stores the points that make up a single curve on a single slice.
    """

    __tablename__ = "Curve"

    # Points stored as binary data (4-byte floats)
    points_data: Mapped[bytes] = Column("PointsData", LargeBinary, nullable=True)
    contour_geometric_type: Mapped[str] = Column(
        "ContourGeometricType", String, nullable=True
    )

    flags: Mapped[int] = Column("Flags", Integer, nullable=True)
    block_size: Mapped[int] = Column("BlockSize", Integer, nullable=True)
    num_points: Mapped[int] = Column("NumPoints", Integer, nullable=True)
    curve_number: Mapped[int] = Column("CurveNumber", Integer, nullable=True)
    slice_index: Mapped[Optional[int]] = Column("SliceIndex", Integer, nullable=True)
    z_position: Mapped[Optional[float]] = Column("ZPosition", Float, nullable=True)

    # Parent relationship
    roi_id: Mapped[int] = Column("ROIID", Integer, ForeignKey("ROI.ID"))
    roi = relationship("ROI", back_populates="curve_list")

    def __init__(self, points: Optional[np.ndarray] = None, **kwargs):
        """Initialize a Curve instance.

        Args:
            points: Optional array-like of points, shape (N, 3) where N is the number of points
            **kwargs: Keyword arguments used to initialize Curve attributes.

        Relationships:
            roi (ROI): The parent ROI to which this Curve belongs (many-to-one).
        """
        super().__init__(**kwargs)
        if points is not None:
            self.points = points

    def __repr__(self) -> str:
        """String representation of the Curve instance."""
        return f"<Curve(id={self.id}, curve_number={self.curve_number}, point_count={self.point_count})>"

    @property
    def points(self) -> np.ndarray:
        """Get the points as a numpy array of shape (N, 3) where N is the number of points."""
        if self.points_data is None:
            return np.zeros((0, 3), dtype=np.float32)
        return np.frombuffer(self.points_data, dtype=np.float32).reshape(-1, 3)

    @points.setter
    def points(self, value: Union[np.ndarray, List[List[float]]]):
        """Set the points from a numpy array or list of [x, y, z] coordinates.

        Args:
            value: Array-like of shape (N, 3) where N is the number of points
        """
        arr = np.asarray(value, dtype=np.float32)
        if arr.ndim != 2 or arr.shape[1] != 3:
            raise ValueError("Points must be a 2D array with shape (N, 3)")
        self.points_data = arr.tobytes()
        self.num_points = len(arr)

    @property
    def point_count(self) -> int:
        """
        Get the number of points in the curve.

        Returns:
            Number of points.
        """
        return self.num_points

    def get_curve_data(self) -> np.ndarray:
        """
        Get the curve data as a flat numpy array of coordinates.

        Returns:
            1D numpy array of coordinates [x1, y1, z1, x2, y2, z2, ...].
        """
        return self.points.ravel()


class ROI(PinnacleBase):
    """
    Model representing a Region of Interest (ROI).

    This class stores all ROI-specific information needed for DICOM conversion,
    including curves and associated metadata.
    """

    __tablename__ = "ROI"

    roi_number: Mapped[int] = Column("ROINumber", Integer, nullable=True)
    name: Mapped[str] = Column("Name", String, nullable=True)
    volume_name: Mapped[str] = Column("VolumeName", String, nullable=True)
    stats_volume_name: Mapped[str] = Column("StatsVolumeName", String, nullable=True)
    roi_description: Mapped[str] = Column("ROIDescription", String, nullable=True)
    roi_generation_algorithm: Mapped[str] = Column(
        "ROIGenerationAlgorithm", String, nullable=True
    )
    roi_type: Mapped[str] = Column("ROIType", String, nullable=True)
    structure_type: Mapped[str] = Column("StructureType", String, nullable=True)

    author: Mapped[str] = Column("Author", String, nullable=True)
    organ_name: Mapped[str] = Column("OrganName", String, nullable=True)
    flags: Mapped[int] = Column("Flags", Integer, nullable=True)
    roi_interpreted_type: Mapped[str] = Column(
        "ROIInterpretedType", String, nullable=True
    )
    color: Mapped[str] = Column("Color", String, nullable=True)
    box_size: Mapped[float] = Column("BoxSize", Float, nullable=True)
    line_2d_width: Mapped[int] = Column("Line2DWidth", Integer, nullable=True)
    line_3d_width: Mapped[int] = Column("Line3DWidth", Integer, nullable=True)
    paint_brush_radius: Mapped[float] = Column("PaintBrushRadius", Float, nullable=True)
    paint_allow_curve_closing: Mapped[bool] = Column(
        "PaintAllowCurveClosing", Boolean, nullable=True
    )
    curve_min_area: Mapped[float] = Column("CurveMinArea", Float, nullable=True)
    curve_overlap_min: Mapped[float] = Column("CurveOverlapMin", Float, nullable=True)
    lower_threshold: Mapped[float] = Column("Lower", Float, nullable=True)
    upper_threshold: Mapped[float] = Column("Upper", Float, nullable=True)
    radius: Mapped[float] = Column("Radius", Float, nullable=True)
    density: Mapped[float] = Column("Density", Float, nullable=True)
    density_units: Mapped[str] = Column("DensityUnits", String, nullable=True)
    override_data: Mapped[bool] = Column("OverrideData", Boolean, nullable=True)
    override_order: Mapped[int] = Column("OverrideOrder", Integer, nullable=True)
    override_material: Mapped[bool] = Column("OverrideMaterial", Boolean, nullable=True)
    material: Mapped[Optional[str]] = Column("Material", String, nullable=True)
    invert_density_loading: Mapped[bool] = Column(
        "InvertDensityLoading", Boolean, nullable=True
    )
    volume: Mapped[float] = Column("Volume", Float, nullable=True)
    pixel_min: Mapped[float] = Column("PixelMin", Float, nullable=True)
    pixel_max: Mapped[float] = Column("PixelMax", Float, nullable=True)
    pixel_mean: Mapped[float] = Column("PixelMean", Float, nullable=True)
    pixel_std: Mapped[float] = Column("PixelStd", Float, nullable=True)
    bev_drr_outline: Mapped[bool] = Column("bBEVDRROutline", Boolean, nullable=True)
    display_on_other_vols: Mapped[bool] = Column(
        "DisplayOnOtherVolumes", Boolean, nullable=True
    )
    is_linked: Mapped[bool] = Column("IsLinked", Boolean, nullable=True)

    # Parent relationship
    plan_id: Mapped[Optional[int]] = Column(
        "PlanID", Integer, ForeignKey("Plan.ID"), nullable=True
    )
    plan: Mapped[Optional["Plan"]] = relationship("Plan", back_populates="roi_list")

    # Child relationship
    curve_list: Mapped[List["Curve"]] = relationship(
        "Curve", back_populates="roi", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        """Initialize an ROI instance.

        Args:
            **kwargs: Keyword arguments used to initialize ROI attributes

        Relationships:
            plan (Plan): The parent Plan to which this ROI belongs (many-to-one).
            curves (List[Curve]): List of Curves associated with this ROI (one-to-many).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """String representation of the ROI instance."""
        return f"<ROI(id={self.id}, number={self.roi_number}, name='{self.name}')>"
