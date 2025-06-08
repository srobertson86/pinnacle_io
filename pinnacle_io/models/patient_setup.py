"""
SQLAlchemy model for Pinnacle PatientPosition data.

This module provides the PatientPosition model for representing patient position and setup information.
"""

from typing import Optional, List
import numpy as np
import json

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from pinnacle_io.models.versioned_base import VersionedBase
from pinnacle_io.utils.patient_enum import (
    PatientPositionEnum,
    PatientOrientationEnum,
    TableMotionEnum,
    PatientSetupEnum,
)


class PatientSetup(VersionedBase):
    """
    Model representing patient position and associated coordinate transformations.

    This class stores information about patient positioning and provides methods
    for transforming coordinates between different coordinate systems.
    """

    __tablename__ = "PatientSetup"

    # Primary key is inherited from VersionedBase

    # These fields come from the plan.PatientSetup file
    position: Mapped[str] = Column(
        "Position", String, nullable=True
    )
    orientation: Mapped[str] = Column(
        "Orientation", String, nullable=True
    )
    table_motion: Mapped[str] = Column(
        "TableMotion", String, nullable=True
    )

    # Patient setup is derived from the fields above
    patient_setup: Mapped[str] = Column(
        "PatientSetup", String, nullable=True
    )

    # Transformation matrices stored as serialized strings
    # These matrices transform coordinates from one system to another
    pinnacle_to_dicom_matrix: Mapped[str] = Column(
        "PinnacleToDicomMatrix", String, nullable=True
    )
    dicom_to_pinnacle_matrix: Mapped[str] = Column(
        "DicomToPinnacleMatrix", String, nullable=True
    )

    # Image orientation stored as serialized array
    image_orientation_patient: Mapped[str] = Column(
        "ImageOrientationPatient", String, nullable=True
    )

    # Patient position description and enum
    patient_position_description: Mapped[Optional[str]] = Column(
        "PatientPositionDescription", String, nullable=True
    )
    patient_position_enum: Mapped[str] = Column(
        "PatientPositionEnum", String, nullable=True
    )

    # Parent Relationships
    plan_id: Mapped[Optional[int]] = Column(
        "PlanID", Integer, ForeignKey("Plan.ID"), nullable=True
    )
    plan = relationship("Plan", back_populates="_patient_position")

    # trial_id: Mapped[Optional[int]] = Column(
    #     "TrialID", Integer, ForeignKey("Trial.ID"), nullable=True
    # )
    # trial = relationship("Trial", back_populates="_patient_position")

    def __init__(self, **kwargs):
        """
        Initialize a PatientPosition instance.

        Args:
            **kwargs: Keyword arguments used to initialize PatientSetup attributes.

        Relationships:
            plan (Plan): The parent Plan to which this PatientSetup belongs (many-to-one).
        """
        # Convert enum fields to strings
        for field in [
            "position",
            "Position",
            "orientation",
            "Orientation",
            "table_motion",
            "TableMotion",
            "patient_setup",
            "PatientSetup",
        ]:
            if field in kwargs and not isinstance(kwargs[field], str):
                kwargs[field] = getattr(kwargs[field], "value", str(kwargs[field]))

        if "patient_setup" not in kwargs:
            kwargs["patient_setup"] = PatientSetupEnum.from_orientation_and_position(
                PatientOrientationEnum(
                    kwargs.get("orientation", kwargs.get("Orientation"))
                    or PatientOrientationEnum.Unknown.value
                ),
                PatientPositionEnum(
                    kwargs.get("position", kwargs.get("Position"))
                    or PatientPositionEnum.Unknown.value
                ),
            ).value

        # Handle numpy array serialization
        if "pinnacle_to_dicom_matrix" in kwargs and isinstance(
            kwargs["pinnacle_to_dicom_matrix"], np.ndarray
        ):
            kwargs["pinnacle_to_dicom_matrix"] = np.array2string(
                kwargs["pinnacle_to_dicom_matrix"]
            )

        if "dicom_to_pinnacle_matrix" in kwargs and isinstance(
            kwargs["dicom_to_pinnacle_matrix"], np.ndarray
        ):
            kwargs["dicom_to_pinnacle_matrix"] = np.array2string(
                kwargs["dicom_to_pinnacle_matrix"]
            )

        if "image_orientation_patient" in kwargs and isinstance(
            kwargs["image_orientation_patient"], list
        ):
            kwargs["image_orientation_patient"] = ",".join(
                map(str, kwargs["image_orientation_patient"])
            )

        super().__init__(**kwargs)

        # Initialize transformation matrices if not provided
        if (
            "pinnacle_to_dicom_matrix" not in kwargs
            and "dicom_to_pinnacle_matrix" not in kwargs
        ):
            self._initialize_transformation_matrices()

    def __repr__(self) -> str:
        """String representation of the PatientSetup instance."""
        return f"<PatientSetup(id={self.id}, setup='{self.patient_setup}')>"

    @property
    def position_enum(self) -> PatientPositionEnum:
        """
        Get the position as an enum.

        Returns:
            Position as a PatientPositionEnum.
        """
        try:
            return PatientPositionEnum(self.position)
        except ValueError:
            return PatientPositionEnum.Unknown

    @property
    def orientation_enum(self) -> PatientOrientationEnum:
        """
        Get the orientation as an enum.

        Returns:
            Orientation as a PatientOrientationEnum.
        """
        try:
            return PatientOrientationEnum(self.orientation)
        except ValueError:
            return PatientOrientationEnum.Unknown

    @property
    def table_motion_enum(self) -> TableMotionEnum:
        """
        Get the table motion as an enum.

        Returns:
            Table motion as a TableMotionEnum.
        """
        try:
            return TableMotionEnum(self.table_motion)
        except ValueError:
            return TableMotionEnum.Unknown

    @property
    def patient_setup_enum(self) -> PatientSetupEnum:
        """
        Get the patient setup as an enum.

        Returns:
            Patient setup as a PatientSetupEnum.
        """
        try:
            return PatientSetupEnum(self.patient_setup)
        except ValueError:
            return PatientSetupEnum.Unknown

    @property
    def pinnacle_to_dicom_matrix_array(self) -> np.ndarray:
        """
        Get the pinnacle to DICOM transformation matrix as a numpy array.

        Returns:
            Transformation matrix as a numpy array.
        """
        try:
            return np.array(json.loads(self.pinnacle_to_dicom_matrix))
        except (json.JSONDecodeError, ValueError):
            return np.eye(4)

    @property
    def dicom_to_pinnacle_matrix_array(self) -> np.ndarray:
        """
        Get the DICOM to pinnacle transformation matrix as a numpy array.

        Returns:
            Transformation matrix as a numpy array.
        """
        try:
            return np.array(json.loads(self.dicom_to_pinnacle_matrix))
        except (json.JSONDecodeError, ValueError):
            return np.eye(4)

    @property
    def image_orientation_patient_array(self) -> List[float]:
        """
        Get the image orientation patient as a list of floats.

        Returns:
            Image orientation patient as a list of floats.
        """
        try:
            return [float(x) for x in self.image_orientation_patient.split(",")]
        except ValueError:
            return [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]

    def _initialize_transformation_matrices(self):
        """
        Initialize transformation matrices based on position type.
        """
        if self.patient_setup == PatientSetupEnum.HFS:  # Head First Supine
            # Default transformations for different patient positions
            # For HFS and anything that isn't HFP, FFS, and FFP,
            # Pinnacle and DICOM coordinates are related as follows:
            # DICOM X = -Pinnacle X
            # DICOM Y = -Pinnacle Y
            # DICOM Z = Pinnacle Z
            self.pinnacle_to_dicom_matrix = json.dumps(
                [[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            )

            # Inverse transformation
            self.dicom_to_pinnacle_matrix = json.dumps(
                [[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            )

            # Image orientation for HFS
            self.image_orientation_patient = ",".join(map(str, [1, 0, 0, 0, 1, 0]))

        elif self.patient_setup == PatientSetupEnum.HFP:  # Head First Prone
            # For HFP, Pinnacle and DICOM coordinates are related as follows:
            # DICOM X = Pinnacle X
            # DICOM Y = Pinnacle Y
            # DICOM Z = Pinnacle Z
            self.pinnacle_to_dicom_matrix = json.dumps(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            )

            # Inverse transformation
            self.dicom_to_pinnacle_matrix = json.dumps(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            )

            # Image orientation for HFP
            self.image_orientation_patient = ",".join(map(str, [-1, 0, 0, 0, -1, 0]))

        elif self.patient_setup == PatientSetupEnum.FFS:  # Feet First Supine
            # For FFS, Pinnacle and DICOM coordinates are related as follows:
            # DICOM X = Pinnacle X
            # DICOM Y = -Pinnacle Y
            # DICOM Z = -Pinnacle Z
            self.pinnacle_to_dicom_matrix = json.dumps(
                [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
            )

            # Inverse transformation
            self.dicom_to_pinnacle_matrix = json.dumps(
                [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
            )

            # Image orientation for FFS
            self.image_orientation_patient = ",".join(map(str, [-1, 0, 0, 0, 1, 0]))

        elif self.patient_setup == PatientSetupEnum.FFP:  # Feet First Prone
            # For FFP, Pinnacle and DICOM coordinates are related as follows:
            # DICOM X = -Pinnacle X
            # DICOM Y = Pinnacle Y
            # DICOM Z = -Pinnacle Z
            self.pinnacle_to_dicom_matrix = json.dumps(
                [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
            )

            # Inverse transformation
            self.dicom_to_pinnacle_matrix = json.dumps(
                [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
            )

            # Image orientation for FFP
            self.image_orientation_patient = ",".join(map(str, [1, 0, 0, 0, -1, 0]))

    def transform_point_pinnacle_to_dicom(self, point: List[float]) -> List[float]:
        """
        Transform a point from Pinnacle coordinates to DICOM coordinates.

        Args:
            point: Point in Pinnacle coordinates [x, y, z].

        Returns:
            Point in DICOM coordinates [x, y, z].
        """
        # Convert to homogeneous coordinates
        homogeneous_point = np.array([point[0], point[1], point[2], 1.0])

        # Apply transformation
        transformed_point = np.dot(self.pinnacle_to_dicom_matrix_array, homogeneous_point)

        # Convert back to 3D coordinates
        return [transformed_point[0], transformed_point[1], transformed_point[2]]

    def transform_point_dicom_to_pinnacle(self, point: List[float]) -> List[float]:
        """
        Transform a point from DICOM coordinates to Pinnacle coordinates.

        Args:
            point: Point in DICOM coordinates [x, y, z].

        Returns:
            Point in Pinnacle coordinates [x, y, z].
        """
        # Convert to homogeneous coordinates
        homogeneous_point = np.array([point[0], point[1], point[2], 1.0])

        # Apply transformation
        transformed_point = np.dot(self.dicom_to_pinnacle_matrix_array, homogeneous_point)

        # Convert back to 3D coordinates
        return [transformed_point[0], transformed_point[1], transformed_point[2]]

    def transform_contour_pinnacle_to_dicom(
        self, contour_points: List[List[float]]
    ) -> List[List[float]]:
        """
        Transform a list of contour points from Pinnacle coordinates to DICOM coordinates.

        Args:
            contour_points: List of points in Pinnacle coordinates [[x1, y1, z1], [x2, y2, z2], ...].

        Returns:
            List of points in DICOM coordinates [[x1, y1, z1], [x2, y2, z2], ...].
        """
        return [
            self.transform_point_pinnacle_to_dicom(point) for point in contour_points
        ]

    def transform_contour_dicom_to_pinnacle(
        self, contour_points: List[List[float]]
    ) -> List[List[float]]:
        """
        Transform a list of contour points from DICOM coordinates to Pinnacle coordinates.

        Args:
            contour_points: List of points in DICOM coordinates [[x1, y1, z1], [x2, y2, z2], ...].

        Returns:
            List of points in Pinnacle coordinates [[x1, y1, z1], [x2, y2, z2], ...].
        """
        return [
            self.transform_point_dicom_to_pinnacle(point) for point in contour_points
        ]
