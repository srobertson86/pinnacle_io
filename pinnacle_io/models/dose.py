"""
Dose model for Pinnacle IO.

This module provides the Dose data model for representing dose distribution data.
"""

from typing import Any, ClassVar, List, Optional, Tuple, TYPE_CHECKING
import numpy as np
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.trial import DoseGrid, Trial
    from pinnacle_io.models.beam import Beam


class Dose(PinnacleBase):
    """
    Model representing a dose distribution in the Pinnacle treatment planning system.

    This class encapsulates all dose-related information including dose grid properties,
    dose calculation parameters, and relationships to other treatment planning entities.
    It supports various dose types (PHYSICAL, EFFECTIVE) and units (GY, CGY).

    The dose can be associated with different levels of the treatment hierarchy:
    - Beam-specific dose (for individual beam contributions)
    - Trial dose (for composite dose across all beams in a trial)
    - Plan dose (for the final treatment plan dose)

    Key Features:
    - Supports both grid-based and point-based dose representation
    - Handles dose grid transformations and coordinate systems
    - Manages relationships with DoseGrid, Beam, and Trial entities
    - Provides methods for dose grid manipulation and analysis

    Relationships:
        - dose_grid (DoseGrid): The parent DoseGrid containing spatial information
        - beam (Beam): Associated Beam for beam-specific doses (optional)
        - trial (Trial): Associated Trial for trial-level doses (optional)
        - max_dose_point (MaxDosePoint): Point of maximum dose (one-to-one)
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
    max_dose_point: Mapped[Optional["MaxDosePoint"]] = relationship(
        "MaxDosePoint", 
        back_populates="dose", 
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined"
    )

    # For storing serialized pixel data (optional, could use external storage)
    # We're not storing pixel data in the database to avoid making it unnecessarily large
    # _pixel_data_blob: Mapped[Optional[bytes]] = Column("PixelDataBlob", LargeBinary, nullable=True)

    # Transient attributes (not stored in database)
    _pixel_data: ClassVar[Optional[np.ndarray]] = None

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a Dose instance with optional attributes and relationships.

        Args:
            **kwargs: Keyword arguments to initialize Dose attributes.
                Common attributes include:
                - dose_id (str): Unique identifier for the dose
                - dose_type (str): Type of dose (e.g., 'PHYSICAL', 'EFFECTIVE')
                - dose_unit (str): Unit of dose (e.g., 'GY', 'CGY')
                - dose_summation_type (str): Type of dose summation (e.g., 'PLAN', 'BEAM')
                - pixel_data (np.ndarray): Optional numpy array containing dose grid data
                - referenced_beam_numbers (List[int]): List of beam numbers this dose references

        Relationships:
            dose_grid (DoseGrid): Parent DoseGrid containing spatial information (many-to-one).
            beam (Beam): Associated Beam for beam-specific doses (many-to-one, optional).
            trial (Trial): Associated Trial for trial-level doses (many-to-one, optional).
            max_dose_point (MaxDosePoint): Point of maximum dose (one-to-one).

        Example:
            >>> dose = Dose(
            ...     dose_id='D1',
            ...     dose_type='PHYSICAL',
            ...     dose_unit='GY',
            ...     dose_summation_type='PLAN',
            ...     pixel_data=np.zeros((100, 100, 50)),
            ...     referenced_beam_numbers=[1, 2, 3]
            ... )
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
    """Model representing the maximum dose point in a dose distribution.

    This class stores the spatial location and properties of the point receiving
    the maximum dose in a treatment plan, beam, or trial. It includes display
    properties for visualization and references to the associated dose and beam.

    Attributes:
        color (str): RGB color string for display (e.g., '255,0,0' for red).
        display_2d (str): Display settings for 2D views.
        dose_value (float): The maximum dose value at this point.
        dose_units (str): Units of the dose value (e.g., 'GY').
        location_x (float): X-coordinate of the maximum dose point in mm.
        location_y (float): Y-coordinate of the maximum dose point in mm.
        location_z (float): Z-coordinate of the maximum dose point in mm.

    Relationships:
        beam (Beam): The Beam associated with this maximum dose point (many-to-one).
        dose (Dose): The parent Dose containing this point (many-to-one).
        trial (Trial): The parent Trial for this point (many-to-one).
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

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a MaxDosePoint instance with optional attributes.

        Args:
            **kwargs: Keyword arguments to initialize MaxDosePoint attributes.
                Common attributes include:
                - color (str): RGB color string for display
                - dose_value (float): Maximum dose value
                - location_x (float): X-coordinate in mm
                - location_y (float): Y-coordinate in mm
                - location_z (float): Z-coordinate in mm
                - beam_id (int): ID of associated Beam
                - dose_id (int): ID of parent Dose
                - trial_id (int): ID of parent Trial

        Relationships:
            beam (Beam): Associated Beam (many-to-one).
            dose (Dose): Parent Dose (many-to-one).
            trial (Trial): Parent Trial (many-to-one).

        Example:
            >>> max_point = MaxDosePoint(
            ...     color='255,0,0',
            ...     dose_value=72.5,
            ...     dose_units='GY',
            ...     location_x=10.5,
            ...     location_y=-5.2,
            ...     location_z=15.8
            ... )
        """
        super().__init__(**kwargs)
