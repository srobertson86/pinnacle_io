"""
SQLAlchemy model for Pinnacle PatientLite data.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.institution import Institution


class PatientLite(PinnacleBase):
    """
    Represents a lightweight Pinnacle Patient record.

    This is used in Institution models to list available patients without
    loading the full patient data.
    """

    __tablename__ = "PatientLite"

    # Primary key is inherited from PinnacleBase
    patient_id: Mapped[int] = Column("PatientID", Integer, nullable=True)
    patient_path: Mapped[str] = Column("PatientPath", String, nullable=False)
    mount_point: Mapped[str] = Column("MountPoint", String, nullable=True)
    dir_size: Mapped[float] = Column("DirSize", Float, nullable=True)
    last_name: Mapped[str] = Column("LastName", String, nullable=True)
    first_name: Mapped[str] = Column("FirstName", String, nullable=True)
    middle_name: Mapped[str] = Column("MiddleName", String, nullable=True)
    medical_record_number: Mapped[str] = Column("MedicalRecordNumber", String, nullable=True)
    physician: Mapped[str] = Column("Physician", String, nullable=True)
    last_modified: Mapped[datetime] = Column("LastModified", DateTime, nullable=True)

    # Parent relationship
    institution_id: Mapped[int] = Column(Integer, ForeignKey("Institution.ID"))
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="patient_lite_list"
    )

    def __repr__(self) -> str:
        return f"<PatientLite(id={self.id}, patient_id={self.patient_id}, name='{self.last_name}, {self.first_name}')>"

    def __init__(self, **kwargs):
        """
        Initialize a PatientLite instance.

        Args:
            **kwargs: Keyword arguments used to initialize PatientLite attributes.

        Relationships:
            institution (Institution): The parent Institution to which this PatientLite belongs (many-to-one).

        Notes:
            If the keyword argument 'formatted_description' ('FormattedDescription') is provided,
            it should be a string containing patient details separated by '&&' in the following order:
                'LastName&&FirstName&&MiddleName&&MedicalRecordNumber&&Physician&&LastModified'

            The string is split on '&&' and mapped to the corresponding attributes:
                - last_name
                - first_name
                - middle_name
                - medical_record_number
                - physician
                - last_modified

            If fewer than 6 fields are present, missing fields are set to empty strings.
            The 'last_modified' field is converted to a datetime object if it is provided in the formatted description.
        """
        formatted_description = kwargs.pop(
            "formatted_description", kwargs.pop("FormattedDescription", None)
        )

        super().__init__(**kwargs)

        # Process formatted_description if provided
        if formatted_description:
            parts = formatted_description.split("&&")
            parts += [""] * (6 - len(parts))
            self.last_name = parts[0]
            self.first_name = parts[1]
            self.middle_name = parts[2]
            self.medical_record_number = parts[3]
            self.physician = parts[4]
            self.last_modified = parts[5]
