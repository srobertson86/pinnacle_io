"""
SQLAlchemy model for Pinnacle ImageSet data.
"""

from typing import Optional, List, Tuple, TYPE_CHECKING
from sqlalchemy import Column, String, Integer, Float, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase
from pinnacle_io.models.types import JsonList
import warnings
import numpy as np
from pinnacle_io.models.patient import Patient

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from pinnacle_io.models.image_info import ImageInfo
    from pinnacle_io.models.plan import Plan


class ImageSet(PinnacleBase):
    """
    Model representing an image set (CT, MR, etc.).

    This class stores all image-specific information needed for DICOM conversion,
    including dimensions, pixel spacing, and image orientation.
    """

    __tablename__ = "ImageSet"

    # Primary key is inherited from PinnacleBase
    series_uid: Mapped[Optional[str]] = Column("SeriesUID", String, nullable=True)
    study_uid: Mapped[Optional[str]] = Column("StudyUID", String, nullable=True)
    series_number: Mapped[Optional[int]] = Column(
        "SeriesNumber", Integer, nullable=True
    )
    acquisition_number: Mapped[Optional[int]] = Column(
        "AcquisitionNumber", Integer, nullable=True
    )

    # Patient information
    image_set_id: Mapped[Optional[int]] = Column(
        "ImageSetID", Integer, nullable=True
    )  # From the Patient file. Not the primary key.
    image_name: Mapped[Optional[str]] = Column("ImageName", String, nullable=True)
    name_from_scanner: Mapped[Optional[str]] = Column(
        "NameFromScanner", String, nullable=True
    )
    exam_id: Mapped[Optional[str]] = Column("ExamID", String, nullable=True)
    study_id: Mapped[Optional[str]] = Column("StudyID", String, nullable=True)
    modality: Mapped[Optional[str]] = Column(
        "Modality", String, nullable=True
    )  # CT, MR, etc.
    modality_type: Mapped[Optional[str]] = Column("ModalityType", String, nullable=True)
    number_of_images: Mapped[Optional[int]] = Column(
        "NumberOfImages", Integer, nullable=True
    )
    scan_time_from_scanner: Mapped[Optional[str]] = Column(
        "ScanTimeFromScanner", String, nullable=True
    )
    file_name: Mapped[Optional[str]] = Column("FileName", String, nullable=True)
    series_description: Mapped[Optional[str]] = Column(
        "SeriesDescription", String, nullable=True
    )
    mrn: Mapped[Optional[str]] = Column("MRN", String, nullable=True)
    dob: Mapped[Optional[str]] = Column("DOB", String, nullable=True)
    gating_uid: Mapped[Optional[str]] = Column("GatingUID", String, nullable=True)
    series_uid_text: Mapped[Optional[str]] = Column(
        "SeriesUIDText", String, nullable=True
    )

    # Dimensions
    x_dim: Mapped[Optional[int]] = Column("XDim", Integer, nullable=True)
    y_dim: Mapped[Optional[int]] = Column("YDim", Integer, nullable=True)
    z_dim: Mapped[Optional[int]] = Column("ZDim", Integer, nullable=True)
    t_dim: Mapped[Optional[int]] = Column("TDim", Integer, nullable=True)

    # Additional pixel dimensions from header
    t_pixdim: Mapped[Optional[float]] = Column("TPixDim", Float, nullable=True)
    x_pixdim: Mapped[Optional[float]] = Column("XPixDim", Float, nullable=True)
    y_pixdim: Mapped[Optional[float]] = Column("YPixDim", Float, nullable=True)
    z_pixdim: Mapped[Optional[float]] = Column("ZPixDim", Float, nullable=True)

    # Start positions
    t_start: Mapped[Optional[float]] = Column("TStart", Float, nullable=True)
    x_start: Mapped[Optional[float]] = Column("XStart", Float, nullable=True)
    y_start: Mapped[Optional[float]] = Column("YStart", Float, nullable=True)
    z_start: Mapped[Optional[float]] = Column("ZStart", Float, nullable=True)
    z_time: Mapped[Optional[float]] = Column("ZTime", Float, nullable=True)
    x_start_dicom: Mapped[Optional[float]] = Column("XStartDicom", Float, nullable=True)
    y_start_dicom: Mapped[Optional[float]] = Column("YStartDicom", Float, nullable=True)

    # Data type information
    datatype: Mapped[Optional[int]] = Column("Datatype", Integer, nullable=True)
    bitpix: Mapped[Optional[int]] = Column("Bitpix", Integer, nullable=True)
    bytes_pix: Mapped[Optional[int]] = Column("BytesPix", Integer, nullable=True)
    vol_max: Mapped[Optional[float]] = Column("VolMax", Float, nullable=True)
    vol_min: Mapped[Optional[float]] = Column("VolMin", Float, nullable=True)

    # Additional fields from header
    byte_order: Mapped[Optional[int]] = Column("ByteOrder", Integer, nullable=True)
    read_conversion: Mapped[Optional[str]] = Column(
        "ReadConversion", String, nullable=True
    )
    write_conversion: Mapped[Optional[str]] = Column(
        "WriteConversion", String, nullable=True
    )
    dim_units: Mapped[Optional[str]] = Column("DimUnits", String, nullable=True)
    voxel_type: Mapped[Optional[str]] = Column("VoxelType", String, nullable=True)
    vis_only: Mapped[Optional[int]] = Column("VisOnly", Integer, nullable=True)
    # data_type: Mapped[Optional[str]] = Column("DataType", String, nullable=True) # See datatype above
    vol_type: Mapped[Optional[str]] = Column("VolType", String, nullable=True)
    db_name: Mapped[Optional[str]] = Column("DBName", String, nullable=True)
    medical_record: Mapped[Optional[str]] = Column(
        "MedicalRecord", String, nullable=True
    )
    originator: Mapped[Optional[str]] = Column("Originator", String, nullable=True)
    date: Mapped[Optional[str]] = Column("Date", String, nullable=True)
    scanner_id: Mapped[Optional[str]] = Column("ScannerID", String, nullable=True)
    patient_position: Mapped[Optional[str]] = Column(
        "PatientPosition", String, nullable=True
    )
    orientation: Mapped[Optional[int]] = Column("Orientation", Integer, nullable=True)
    scan_acquisition: Mapped[Optional[int]] = Column(
        "ScanAcquisition", Integer, nullable=True
    )
    comment: Mapped[Optional[str]] = Column("Comment", String, nullable=True)
    fname_format: Mapped[Optional[str]] = Column("FnameFormat", String, nullable=True)
    fname_index_start: Mapped[Optional[int]] = Column(
        "FnameIndexStart", Integer, nullable=True
    )
    fname_index_delta: Mapped[Optional[int]] = Column(
        "FnameIndexDelta", Integer, nullable=True
    )
    binary_header_size: Mapped[Optional[int]] = Column(
        "BinaryHeaderSize", Integer, nullable=True
    )
    manufacturer: Mapped[Optional[str]] = Column("Manufacturer", String, nullable=True)
    model: Mapped[Optional[str]] = Column("Model", String, nullable=True)
    couch_pos: Mapped[Optional[float]] = Column("CouchPos", Float, nullable=True)
    couch_height: Mapped[Optional[float]] = Column("CouchHeight", Float, nullable=True)
    x_offset: Mapped[Optional[float]] = Column("XOffset", Float, nullable=True)
    y_offset: Mapped[Optional[float]] = Column("YOffset", Float, nullable=True)
    dataset_modified: Mapped[Optional[int]] = Column(
        "DatasetModified", Integer, nullable=True
    )
    gating_type: Mapped[Optional[str]] = Column("GatingType", String, nullable=True)
    gating_value: Mapped[Optional[str]] = Column("GatingValue", String, nullable=True)
    irradiation_event_uid: Mapped[Optional[str]] = Column(
        "IrradiationEventUID", String, nullable=True
    )
    scan_options: Mapped[Optional[str]] = Column("ScanOptions", String, nullable=True)
    low_sag: Mapped[Optional[str]] = Column("LowSag", String, nullable=True)
    negative_voxel: Mapped[Optional[str]] = Column(
        "NegativeVoxel", String, nullable=True
    )
    station_name: Mapped[Optional[str]] = Column("StationName", String, nullable=True)
    kvp: Mapped[Optional[str]] = Column("KVP", String, nullable=True)
    exposure: Mapped[Optional[float]] = Column("Exposure", Float, nullable=True)
    series_date_time: Mapped[Optional[str]] = Column(
        "SeriesDateTime", String, nullable=True
    )
    version: Mapped[Optional[str]] = Column("Version", String, nullable=True)
    binning_type: Mapped[Optional[str]] = Column("BinningType", String, nullable=True)
    is_eeov: Mapped[Optional[int]] = Column("IsEEOV", Integer, nullable=True)
    is_omar: Mapped[Optional[int]] = Column("IsOMAR", Integer, nullable=True)
    image_diameter: Mapped[Optional[float]] = Column(
        "ImageDiameter", Float, nullable=True
    )
    has_couchheight: Mapped[Optional[int]] = Column(
        "HasCouchHeight", Integer, nullable=True
    )

    # Image orientation
    image_orientation_patient: Mapped[list] = Column(
        "ImageOrientationPatient", JsonList, default=[1, 0, 0, 0, 1, 0]
    )
    image_position_patient: Mapped[list] = Column(
        "ImagePositionPatient", JsonList, default=[0, 0, 0]
    )

    # Pixel data - stored separately as binary data
    pixel_data: Mapped[bytes] = Column("PixelData", LargeBinary, nullable=True)

    # Parent relationship
    patient_id: Mapped[int] = Column("PatientID", Integer, ForeignKey("Patient.ID"))
    patient: Mapped["Patient"] = relationship(
        "Patient", back_populates="image_set_list"
    )

    # Child relationships
    image_info_list: Mapped[list["ImageInfo"]] = relationship(
        "ImageInfo", back_populates="image_set", cascade="all, delete-orphan"
    )
    plan_list: Mapped[list["Plan"]] = relationship(
        "Plan",
        back_populates="primary_ct_image_set",
        foreign_keys="Plan.primary_ct_image_set_id",
        primaryjoin="ImageSet.id == Plan.primary_ct_image_set_id",
    )

    def __init__(self, pixel_data: Optional[np.ndarray] = None, **kwargs):
        """
        Initialize an ImageSet instance.

        Args:
            pixel_data: Numpy array of pixel data to store in the database
            **kwargs: Keyword arguments used to initialize ImageSet attributes

        Relationships:
            image_info_list (List[ImageInfo]): List of ImageInfo objects associated with this ImageSet (one-to-many).
            plan (Plan): The parent Plan to which this ImageSet belongs (many-to-one), if applicable.
        """
        # Handle pixel_data if it's a numpy array
        if pixel_data is None:
            pixel_data = kwargs.pop("pixel_data", kwargs.pop("PixelData", None))
        if pixel_data is not None:
            try:
                if isinstance(pixel_data, np.ndarray):
                    kwargs["pixel_data"] = pixel_data.tobytes()
                else:
                    warnings.warn(
                        f"pixel_data is not a numpy array (pixel_data={pixel_data!r})",
                        stacklevel=2,
                    )
            except ImportError:
                warnings.warn(
                    f"Could not convert pixel_data to a byte array (pixel_data={pixel_data!r})",
                    stacklevel=2,
                )

        # Initialize the model with the remaining kwargs
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """Return a string representation of the ImageSet instance."""
        return f"<ImageSet(id={self.id}, name='{self.image_name}', modality='{self.modality}')>"

    @property
    def table_positions(self) -> List[float]:
        """Get list of table positions."""
        return [image_info.table_position for image_info in self.image_info_list]

    @property
    def couch_positions(self) -> List[float]:
        """Get list of couch positions."""
        return [image_info.couch_pos for image_info in self.image_info_list]

    @property
    def slice_numbers(self) -> List[int]:
        """Get list of slice numbers."""
        return [image_info.slice_number for image_info in self.image_info_list]

    @property
    def study_instance_uid(self) -> str:
        """Study instance UID."""
        return (
            self.image_info_list[0].study_instance_uid if self.image_info_list else ""
        )

    @property
    def frame_of_reference_uid(self) -> str:
        """Frame of reference UID."""
        return self.image_info_list[0].frame_uid if self.image_info_list else ""

    @property
    def class_uid(self) -> str:
        """DICOM Class UID."""
        return self.image_info_list[0].class_uid if self.image_info_list else ""

    @property
    def instance_uids(self) -> List[str]:
        """Get list of instance UIDs."""
        return [image_info.instance_uid for image_info in self.image_info_list]

    @property
    def suv_scales(self) -> List[float]:
        """Get list of SUV scales."""
        return [image_info.suv_scale for image_info in self.image_info_list]

    @property
    def color_lut_scales(self) -> List[float]:
        """Get list of color LUT scales."""
        return [image_info.color_lut_scale for image_info in self.image_info_list]

    @property
    def dicom_file_names(self) -> List[str]:
        """Get list of DICOM file names."""
        return [image_info.dicom_file_name for image_info in self.image_info_list]

    @property
    def acquisition_times(self) -> List[str]:
        """Get list of acquisition times."""
        return [image_info.acquisition_time for image_info in self.image_info_list]

    @property
    def image_times(self) -> List[str]:
        """Get list of image times."""
        return [image_info.image_time for image_info in self.image_info_list]

    def get_image_dimensions(self) -> Tuple[int, int, int]:
        """
        Get the image dimensions.

        Returns:
            Tuple of (x_dim, y_dim, z_dim).
        """
        return (self.x_dim, self.y_dim, self.z_dim)

    def get_pixel_spacing(self) -> Tuple[float, float, float]:
        """
        Get the pixel spacing.

        Returns:
            Tuple of (x_pixdim, y_pixdim, z_pixdim) in mm.
        """
        return (self.x_pixdim, self.y_pixdim, self.z_pixdim)

    def get_slice_data(self, slice_index: int) -> Optional["np.ndarray"]:
        """
        Get the pixel data for a specific slice.

        Args:
            slice_index: Index of the slice to retrieve.

        Returns:
            2D numpy array of pixel data for the specified slice, or None if pixel data is not available.
        """
        try:
            import numpy as np

            if self.pixel_data is None or slice_index >= self.z_dim:
                return None

            # Convert bytes back to numpy array
            array_data = np.frombuffer(self.pixel_data, dtype=np.int16)
            reshaped_data = array_data.reshape((self.x_dim, self.y_dim, self.z_dim))

            return reshaped_data[:, :, slice_index]
        except ImportError:
            return None

    def set_slice_data(self, slice_index: int, data: "np.ndarray") -> None:
        """
        Set the pixel data for a specific slice.

        Args:
            slice_index: Index of the slice to set.
            data: 2D numpy array of pixel data for the slice.
        """
        try:
            import numpy as np

            # Convert bytes to numpy array if pixel_data exists
            if self.pixel_data is not None:
                array_data = np.frombuffer(self.pixel_data, dtype=np.int16)
                reshaped_data = array_data.reshape((self.x_dim, self.y_dim, self.z_dim))
            else:
                # Initialize pixel data array if it doesn't exist
                reshaped_data = np.zeros(
                    (self.x_dim, self.y_dim, self.z_dim), dtype=np.int16
                )

            if slice_index < self.z_dim:
                reshaped_data[:, :, slice_index] = data

            # Store back as bytes
            self.pixel_data = reshaped_data.tobytes()
        except ImportError:
            pass
