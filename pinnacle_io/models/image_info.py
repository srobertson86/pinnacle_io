"""
SQLAlchemy model for Pinnacle ImageInfo data.
"""

from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from pinnacle_io.models.image_set import ImageSet


class ImageInfo(PinnacleBase):
    """
    Data model for representing an image slice in a study.

    This model stores metadata for an individual image in a study.
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
        "ImageSet", back_populates="image_info_list"
    )

    def __init__(self, **kwargs):
        """
        Initialize an ImageInfo instance.

        Args:
            **kwargs: Keyword arguments used to initialize ImageInfo attributes.

        Relationships:
            image_set (ImageSet): The parent ImageSet to which this ImageInfo belongs (many-to-one).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<ImageInfo(id={self.id}, slice_number={self.slice_number}, table_position={self.table_position})>"
