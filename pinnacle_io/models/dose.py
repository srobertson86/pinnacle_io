"""
Dose model for Pinnacle IO.

This module provides the Dose data model for representing dose distribution data.
"""

from typing import Optional, List, Tuple, ClassVar, TYPE_CHECKING
import numpy as np
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.trial import DoseGrid, Trial
    from pinnacle_io.models.beam import Beam


class Dose(PinnacleBase):
    """
    Model representing a dose distribution.

    This class stores all dose-specific information needed for DICOM conversion,
    including dose grid dimensions, resolution, and pixel data.
    """

    __tablename__ = "Dose"

    # Basic information
    dose_id: Mapped[Optional[str]] = Column("DoseID", String, nullable=True)
    dose_type: Mapped[Optional[str]] = Column(
        "DoseType", String, nullable=True, default="PHYSICAL"
    )  # PHYSICAL, EFFECTIVE, etc.
    dose_unit: Mapped[Optional[str]] = Column(
        "DoseUnit", String, nullable=True, default="GY"
    )  # GY, CGY, etc.

    # Data type information
    datatype: Mapped[Optional[int]] = Column(
        "Datatype", Integer, nullable=True, default=1
    )
    bitpix: Mapped[Optional[int]] = Column("Bitpix", Integer, nullable=True, default=32)
    bytes_pix: Mapped[Optional[int]] = Column(
        "BytesPix", Integer, nullable=True, default=4
    )
    vol_max: Mapped[Optional[float]] = Column(
        "VolMax", Float, nullable=True, default=0.0
    )
    vol_min: Mapped[Optional[float]] = Column(
        "VolMin", Float, nullable=True, default=0.0
    )
    dose_comment: Mapped[Optional[str]] = Column(
        "DoseComment", String, nullable=True, default=""
    )
    dose_grid_scaling: Mapped[Optional[float]] = Column(
        "DoseGridScaling", Float, nullable=True, default=1.0
    )
    dose_summation_type: Mapped[Optional[str]] = Column(
        "DoseSummationType", String, nullable=True, default="PLAN"
    )  # PLAN, BEAM, etc.

    # References to other objects
    referenced_plan_id: Mapped[Optional[str]] = Column(
        "ReferencedPlanID", String, nullable=True
    )

    # For storing serialized beam numbers
    _referenced_beam_numbers: Mapped[Optional[str]] = Column(
        "ReferencedBeamNumbers", String, nullable=True
    )

    # Parent relationships:
    # All Dose instances should be associated with a trial.dose_grid
    dose_grid_id: Mapped[Optional[int]] = Column(
        "DoseGridID", Integer, ForeignKey("DoseGrid.ID"), nullable=True
    )
    dose_grid: Mapped[Optional["DoseGrid"]] = relationship(
        "DoseGrid", back_populates="dose_list"
    )

    # For beam dose, associate the dose with the given beam
    beam_id: Mapped[Optional[int]] = Column(
        "BeamID", Integer, ForeignKey("Beam.ID"), nullable=True
    )
    beam: Mapped[Optional["Beam"]] = relationship("Beam", back_populates="dose")

    # For trial dose (i.e., the sum of beam doses), associate the dose with the given trial
    trial_id: Mapped[Optional[int]] = Column(
        "TrialID", Integer, ForeignKey("Trial.ID"), nullable=True
    )
    trial: Mapped[Optional["Trial"]] = relationship("Trial", back_populates="dose")

    # Child relationship
    max_dose_point: Mapped["MaxDosePoint"] = relationship(
        "MaxDosePoint", back_populates="dose", uselist=False
    )

    # For storing serialized pixel data (optional, could use external storage)
    # We're not storing pixel data in the database to avoid making it unnecessarily large
    # _pixel_data_blob: Mapped[Optional[bytes]] = Column("PixelDataBlob", LargeBinary, nullable=True)

    # Transient attributes (not stored in database)
    _pixel_data: ClassVar[Optional[np.ndarray]] = None

    def __init__(self, **kwargs):
        """
        Initialize a Dose instance.

        Args:
            **kwargs: Keyword arguments used to initialize Dose attributes.

        Relationships:
            dose_grid (DoseGrid or None): The parent DoseGrid to which this Dose belongs (many-to-one).
            beam (Beam or None): The parent Beam to which this Dose belongs (many-to-one, for beam dose).
            trial (Trial or None): The parent Trial to which this Dose belongs (many-to-one, for trial dose).
            max_dose_point (MaxDosePoint): The associated MaxDosePoint (one-to-one).
        """
        # Handle referenced_beam_numbers if provided. These are stored as a comma-separated list of integers in the database
        beam_numbers = kwargs.pop("referenced_beam_numbers", None)
        if beam_numbers is not None:
            self.referenced_beam_numbers = beam_numbers

        # Handle pixel_data if provided
        pixel_data = kwargs.pop("pixel_data", None)
        if pixel_data is not None:
            self._pixel_data = pixel_data

        super().__init__(**kwargs)

    @property
    def referenced_beam_numbers(self) -> List[int]:
        """Get the referenced beam numbers."""
        if not self._referenced_beam_numbers:
            return []
        return [int(num) for num in self._referenced_beam_numbers.split(",") if num]

    @referenced_beam_numbers.setter
    def referenced_beam_numbers(self, value: List[int]) -> None:
        """Set the referenced beam numbers."""
        if not value:
            self._referenced_beam_numbers = None
        else:
            self._referenced_beam_numbers = ",".join(str(num) for num in value)

    @property
    def pixel_data(self) -> Optional[np.ndarray]:
        """Get the pixel data."""
        return self._pixel_data

    @pixel_data.setter
    def pixel_data(self, value: Optional[np.ndarray]) -> None:
        """Set the pixel data."""
        self._pixel_data = value

    def get_dose_dimensions(self) -> Tuple[int, int, int]:
        """
        Get the dose grid dimensions.

        Returns:
            Tuple of (x_dim, y_dim, z_dim).
        """
        if self.dose_grid is None:
            raise ValueError("DoseGrid is not set for this Dose object.")
        return (
            int(self.dose_grid.dimension_x),
            int(self.dose_grid.dimension_y),
            int(self.dose_grid.dimension_z),
        )

    def get_dose_grid_resolution(self) -> Tuple[float, float, float]:
        """
        Get the dose grid resolution.

        Returns:
            Tuple of (x_pixdim, y_pixdim, z_pixdim) in mm.
        """
        if self.dose_grid is None:
            raise ValueError("DoseGrid is not set for this Dose object.")
        return (
            self.dose_grid.voxel_size_x,
            self.dose_grid.voxel_size_y,
            self.dose_grid.voxel_size_z,
        )

    def get_dose_grid_origin(self) -> Tuple[float, float, float]:
        """
        Get the dose grid origin.

        Returns:
            Tuple of (x_start, y_start, z_start) in mm.
        """
        if self.dose_grid is None:
            raise ValueError("DoseGrid is not set for this Dose object.")
        return (
            self.dose_grid.origin_x,
            self.dose_grid.origin_y,
            self.dose_grid.origin_z,
        )

    def get_slice_data(self, slice_index: int) -> Optional[np.ndarray]:
        """
        Get the dose data for a specific slice.

        Args:
            slice_index: Index of the slice to retrieve.

        Returns:
            2D numpy array of dose data for the specified slice, or None if dose data is not available.
        """
        if self.pixel_data is None:
            return None

        dimensions = self.get_dose_dimensions()
        if slice_index >= dimensions[2]:
            return None

        return self.pixel_data[:, :, slice_index]

    def set_slice_data(self, slice_index: int, data: np.ndarray) -> None:
        """
        Set the dose data for a specific slice.

        Args:
            slice_index: Index of the slice to set.
            data: 2D numpy array of dose data for the slice.
        """
        dimensions = self.get_dose_dimensions()

        if self.pixel_data is None:
            # Initialize dose data array if it doesn't exist
            self.pixel_data = np.zeros(
                (dimensions[0], dimensions[1], dimensions[2]), dtype=data.dtype
            )

        if slice_index < dimensions[2]:
            self.pixel_data[:, :, slice_index] = data

    def get_dose_value(self, x: int, y: int, z: int) -> Optional[float]:
        """
        Get the dose value at a specific grid point.

        Args:
            x: X coordinate in grid space.
            y: Y coordinate in grid space.
            z: Z coordinate in grid space.

        Returns:
            Dose value at the specified grid point, or None if coordinates are out of bounds or dose data is not available.
        """
        if self.pixel_data is None:
            return None

        dimensions = self.get_dose_dimensions()
        if (
            x < 0
            or x >= dimensions[0]
            or y < 0
            or y >= dimensions[1]
            or z < 0
            or z >= dimensions[2]
        ):
            return None

        return float(self.pixel_data[x, y, z] * self.dose_grid_scaling)

    def get_max_dose(self) -> Optional[float]:
        """
        Get the maximum dose value in the dose grid.

        Returns:
            Maximum dose value, or None if dose data is not available.
        """
        if self.pixel_data is None:
            return None

        return float(np.max(self.pixel_data) * self.dose_grid_scaling)

    def get_min_dose(self) -> Optional[float]:
        """
        Get the minimum dose value in the dose grid.

        Returns:
            Minimum dose value, or None if dose data is not available.
        """
        if self.pixel_data is None:
            return None

        return float(np.min(self.pixel_data) * self.dose_grid_scaling)

    def get_mean_dose(self) -> Optional[float]:
        """
        Get the mean dose value in the dose grid.

        Returns:
            Mean dose value, or None if dose data is not available.
        """
        if self.pixel_data is None:
            return None

        return float(np.mean(self.pixel_data) * self.dose_grid_scaling)

    def __repr__(self) -> str:
        """
        Return a string representation of this dose.
        """
        return f"<Dose(id='{self.dose_id}', type='{self.dose_type}', dimensions={self.get_dose_dimensions()})>"


class MaxDosePoint(PinnacleBase):
    """
    Model representing the maximum dose point for a treatment trial.

    This class stores information about the maximum dose point for a treatment trial,
    including the color and display settings.
    """

    __tablename__ = "MaxDosePoint"

    # Primary key is inherited from PinnacleBase

    # Only Color and Display2d are specified in the plan.Trial file
    color: Mapped[str] = Column("Color", String, nullable=True)
    display_2d: Mapped[str] = Column("Display2D", String, nullable=True)

    # The following fields are added for convenience but are not part of the original Pinnacle plan.Trial file
    dose_value: Mapped[Optional[float]] = Column("DoseValue", Float, nullable=True)
    dose_units: Mapped[Optional[str]] = Column("DoseUnits", String, nullable=True)
    location_x: Mapped[Optional[float]] = Column("LocationX", Float, nullable=True)
    location_y: Mapped[Optional[float]] = Column("LocationY", Float, nullable=True)
    location_z: Mapped[Optional[float]] = Column("LocationZ", Float, nullable=True)

    # Parent relationships
    beam_id: Mapped[Optional[int]] = Column(
        "BeamID", Integer, ForeignKey("Beam.ID"), nullable=True
    )
    beam = relationship("Beam", back_populates="max_dose_point")
    dose_id: Mapped[Optional[int]] = Column(
        "DoseID", Integer, ForeignKey("Dose.ID"), nullable=True
    )
    dose = relationship("Dose", back_populates="max_dose_point")
    trial_id: Mapped[int] = Column("TrialID", Integer, ForeignKey("Trial.ID"))
    trial = relationship("Trial", back_populates="max_dose_point")

    def __repr__(self) -> str:
        color = self.color if self.color else "None"
        dose = self.dose_value if self.dose_value is not None else ""
        if dose and self.dose_units:
            dose = f"{dose} {self.dose_units}"
        if not dose:
            dose = "None"
        return f"<MaxDosePoint(id={self.id}, color={color}, dose={dose})>"

    def __init__(self, **kwargs):
        """
        Initialize a MaxDosePoint instance.

        Args:
            **kwargs: Keyword arguments used to initialize MaxDosePoint attributes.

        Relationships:
            beam (Beam): The parent Beam to which this MaxDosePoint belongs (many-to-one).
            dose (Dose): The parent Dose to which this MaxDosePoint belongs (many-to-one).
            trial (Trial): The parent Trial to which this MaxDosePoint belongs (many-to-one).
        """
        super().__init__(**kwargs)
