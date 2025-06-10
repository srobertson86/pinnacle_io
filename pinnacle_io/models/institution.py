"""
SQLAlchemy model for Pinnacle Institution data.
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, relationship
from typing import Any, Optional

from pinnacle_io.models.versioned_base import VersionedBase

from pinnacle_io.models.patient import Patient
from pinnacle_io.models.patient_lite import PatientLite


class Institution(VersionedBase):
    """
    Model representing a Pinnacle Institution.

    This class serves as the top-level organizational entity in the Pinnacle system,
    containing all related patient data, treatment plans, and institutional settings.
    It represents a medical institution or department using the Pinnacle system.

    Attributes:
        id (int): Primary key
        institution_id (int): Institution ID from Pinnacle
        institution_path (str): Filesystem path to the institution data
        name (str): Name of the institution
        street_address (str): Primary street address
        city (str): City name
        state (str): State/province
        zip_code (str): Postal/ZIP code
        country (str): Country name
        
    Relationships:
        patient_lite_list (List[PatientLite]): List of lightweight patient records
        patient_list (List[Patient]): List of detailed patient records
    
    Backup and Storage Attributes:
        device_space_required_* (int): Space requirements for different data types
        default_mount_point (str): Default mount point for data storage
        backup_* (various): Backup configuration and status fields
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

    def __init__(self, **kwargs: Any) -> None:
        """Initialize an Institution instance.

        Args:
            **kwargs: Keyword arguments used to initialize Institution attributes.
                     Valid attributes include all column names and relationship names.
                     
        Example:
            >>> inst = Institution(
            ...     name="Example Medical Center",
            ...     street_address="123 Main St",
            ...     city="Anytown",
            ...     state="CA",
            ...     zip_code="12345",
            ...     country="USA"
            ... )
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this institution.
        """
        return f"<Institution(id={self.id}, institution_id={self.institution_id}, name='{self.name}')>"
