"""
SQLAlchemy model for Pinnacle Institution data.
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, relationship
from typing import Optional

from pinnacle_io.models.versioned_base import VersionedBase

from pinnacle_io.models.patient import Patient
from pinnacle_io.models.patient_lite import PatientLite


class Institution(VersionedBase):
    """
    Represents a Pinnacle Institution.

    This is typically the top-level entity in the Pinnacle hierarchy.
    """

    __tablename__ = "Institution"

    # Primary key is inherited from PinnacleBase
    institution_id: Mapped[Optional[int]] = Column("InstitutionID", Integer)
    institution_path: Mapped[Optional[str]] = Column(
        "InstitutionPath", String, nullable=True
    )
    pinn_institution_path: Mapped[Optional[str]] = Column(
        "PinnInstitutionPath", String, nullable=True
    )
    name: Mapped[Optional[str]] = Column("Name", String, nullable=True)
    street_address: Mapped[Optional[str]] = Column(
        "StreetAddress", String, nullable=True
    )
    street_address_2: Mapped[Optional[str]] = Column(
        "StreetAddress2", String, nullable=True
    )
    city: Mapped[Optional[str]] = Column("City", String, nullable=True)
    state: Mapped[Optional[str]] = Column("State", String, nullable=True)
    zip_code: Mapped[Optional[str]] = Column("ZipCode", String, nullable=True)
    country: Mapped[Optional[str]] = Column("Country", String, nullable=True)

    # Device space requirements
    device_space_required_patients: Mapped[Optional[int]] = Column(
        "DeviceSpaceRequiredPatients", Integer, nullable=True
    )
    device_space_required_physics: Mapped[Optional[int]] = Column(
        "DeviceSpaceRequiredPhysics", Integer, nullable=True
    )
    device_space_required_scripts: Mapped[Optional[int]] = Column(
        "DeviceSpaceRequiredScripts", Integer, nullable=True
    )
    device_space_required_organ_models: Mapped[Optional[int]] = Column(
        "DeviceSpaceRequiredOrganModels", Integer, nullable=True
    )
    device_space_required_atlas: Mapped[Optional[int]] = Column(
        "DeviceSpaceRequiredAtlas", Integer, nullable=True
    )
    # Backup information
    default_mount_point: Mapped[Optional[str]] = Column(
        "DefaultMountPoint", String, nullable=True
    )
    backup_description: Mapped[Optional[str]] = Column(
        "BackupDescription", String, nullable=True
    )
    backup_volume: Mapped[Optional[str]] = Column("BackupVolume", String, nullable=True)
    backup_file_name: Mapped[Optional[str]] = Column(
        "BackupFileName", String, nullable=True
    )
    session: Mapped[Optional[str]] = Column("Session", String, nullable=True)
    scripts_dir: Mapped[Optional[str]] = Column("ScriptsDir", String, nullable=True)
    organ_models_dir: Mapped[Optional[str]] = Column(
        "OrganModelsDir", String, nullable=True
    )
    atlas_file: Mapped[Optional[str]] = Column("AtlasFile", String, nullable=True)
    backup_time_stamp: Mapped[Optional[str]] = Column(
        "BackupTimeStamp", String, nullable=True
    )
    backup_device_type: Mapped[Optional[str]] = Column(
        "BackupDeviceType", String, nullable=True
    )

    # Backup flags
    is_patient_backup: Mapped[Optional[int]] = Column(
        "IsPatientBackup", Integer, nullable=True
    )
    is_physics_machines_backup: Mapped[Optional[int]] = Column(
        "IsPhysicsMachinesBackup", Integer, nullable=True
    )
    include_physics_data: Mapped[Optional[int]] = Column(
        "IncludePhysicsData", Integer, nullable=True
    )
    machines_in_v7_format: Mapped[Optional[int]] = Column(
        "MachinesInV7Format", Integer, nullable=True
    )
    is_solaris_format: Mapped[Optional[int]] = Column(
        "IsSolarisFormat", Integer, nullable=True
    )
    include_all_patients: Mapped[Optional[int]] = Column(
        "IncludeAllPatients", Integer, nullable=True
    )
    full_file_name_included: Mapped[Optional[int]] = Column(
        "FullFileNameIncluded", Integer, nullable=True
    )
    backup_id: Mapped[Optional[int]] = Column("BackupID", Integer, nullable=True)
    dynamic_rebuild: Mapped[Optional[int]] = Column(
        "DynamicRebuild", Integer, nullable=True
    )

    # Child Relationships
    patient_lite_list: Mapped[list["PatientLite"]] = relationship(
        "PatientLite", back_populates="institution", cascade="all, delete-orphan"
    )
    patient_list: Mapped[list["Patient"]] = relationship(
        "Patient",
        back_populates="institution",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def __init__(self, **kwargs):
        """
        Initialize an Institution instance.

        Args:
            **kwargs: Keyword arguments used to initialize Institution attributes.

        Relationships:
            patient_lite_list (list[PatientLite]): List of PatientLite objects associated with this institution (one-to-many).
            patients (list[Patient]): List of Patient objects associated with this institution (one-to-many).
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this institution.
        """
        return f"<Institution(id={self.id}, institution_id={self.institution_id}, name='{self.name}')>"
