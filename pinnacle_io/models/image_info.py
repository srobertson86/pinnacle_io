"""
SQLAlchemy model for Pinnacle ImageInfo data.
"""

from typing import Any, Optional, TYPE_CHECKING
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from pinnacle_io.models.image_set import ImageSet


class ImageInfo(PinnacleBase):
    """
    Model representing metadata for an individual image slice in a medical imaging study.

    This class stores DICOM-compatible metadata for a single slice in an image series,
    including positioning, UIDs, and acquisition parameters. It's part of a one-to-many
    relationship with ImageSet, where one ImageSet contains multiple ImageInfo objects.

    Key Features:
    - Stores DICOM-compatible metadata for individual image slices
    - Maintains relationships with parent ImageSet
    - Provides access to slice-specific positioning and timing information

    Attributes:
        table_position (float): Table position of the slice in mm.
        couch_pos (float): Couch position at the time of acquisition.
        slice_number (int): Slice number in the series.
        series_uid (str): DICOM Series Instance UID.
        study_instance_uid (str): DICOM Study Instance UID.
        frame_uid (str): DICOM Frame of Reference UID.
        class_uid (str): DICOM Class UID.
        instance_uid (str): DICOM SOP Instance UID.
        suv_scale (float): Scale factor for Standardized Uptake Value (SUV) calculation.
        color_lut_scale (float): Scale factor for color lookup table.
        dicom_file_name (str): Original DICOM file name.
        acquisition_time (str): Time of acquisition.
        image_time (str): Time when image was created.

    Relationships:
        image_set (ImageSet): Parent ImageSet containing this slice (many-to-one).
    """

    __tablename__ = "ImageInfo"

    # Primary key is inherited from PinnacleBase
    table_position: Mapped[Optional[float]] = Column(
        "TablePosition", Float, nullable=True
    )
    couch_pos: Mapped[Optional[float]] = Column("CouchPos", Float, nullable=True)
    slice_number: Mapped[Optional[int]] = Column("SliceNumber", Integer, nullable=True)
    series_uid: Mapped[Optional[str]] = Column("SeriesUID", String, nullable=True)
    study_instance_uid: Mapped[Optional[str]] = Column(
        "StudyInstanceUID", String, nullable=True
    )
    frame_uid: Mapped[Optional[str]] = Column("FrameUID", String, nullable=True)
    class_uid: Mapped[Optional[str]] = Column("ClassUID", String, nullable=True)
    instance_uid: Mapped[Optional[str]] = Column("InstanceUID", String, nullable=True)
    suv_scale: Mapped[Optional[float]] = Column("SUVDICOMScale", Float, nullable=True)
    color_lut_scale: Mapped[Optional[float]] = Column(
        "ColorLUTScale", Float, nullable=True
    )
    dicom_file_name: Mapped[Optional[str]] = Column(
        "DICOMFileName", String, nullable=True
    )
    acquisition_time: Mapped[Optional[str]] = Column(
        "AcquisitionTime", String, nullable=True
    )
    image_time: Mapped[Optional[str]] = Column("ImageTime", String, nullable=True)
    # Parent relationship
    image_set_id: Mapped[int] = Column(Integer, ForeignKey("ImageSet.ID"))
    image_set: Mapped["ImageSet"] = relationship(
        "ImageSet", 
        back_populates="image_info_list",
        lazy="selectin"
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize an ImageInfo instance with optional attributes.

        Args:
            **kwargs: Keyword arguments to initialize ImageInfo attributes.
                Common attributes include:
                - table_position (float): Table position in mm
                - slice_number (int): Slice number
                - series_uid (str): DICOM Series UID
                - study_instance_uid (str): DICOM Study Instance UID
                - instance_uid (str): DICOM SOP Instance UID

        Relationships:
            image_set (ImageSet): Parent ImageSet containing this slice (many-to-one).

        Example:
            >>> image_info = ImageInfo(
            ...     slice_number=42,
            ...     table_position=0.0,
            ...     series_uid='1.2.840.113619.2.5.1762583153.21551.1000004.1289335474.1.0',
            ...     study_instance_uid='1.2.840.113619.2.5.1762583153.21551.1000004.1289335474',
            ...     instance_uid='1.2.840.113619.2.5.1762583153.21551.1000004.1289335474.1.1'
            ... )
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """Return a string representation of the ImageInfo instance.
        
        Returns:
            str: String representation including ID, slice number, and table position.
        """
        return f"<ImageInfo(id={self.id}, slice_number={self.slice_number}, table_position={self.table_position})>"
