"""
SQLAlchemy model for Pinnacle Patient data.

This module defines the Patient model which represents a patient in the Pinnacle system.
A patient can have multiple plans and image sets associated with them.

Example:
    >>> patient = Patient(
    ...     first_name="John",
    ...     last_name="Doe",
    ...     medical_record_number="MRN12345",
    ...     date_of_birth=date(1980, 1, 1),
    ...     gender="M"
    ... )
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional, TYPE_CHECKING, Dict, Any, Union

from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import Mapped, relationship

from pinnacle_io.models.pinnacle_base import PinnacleBase

if TYPE_CHECKING:
    from pinnacle_io.models.plan import Plan
    from pinnacle_io.models.image_set import ImageSet
    from pinnacle_io.models.institution import Institution


class Patient(PinnacleBase):
    """
    Represents a Pinnacle Patient.

    Patients belong to an Institution and can have multiple Plans and ImageSets.
    This model maps to the Patient table in the Pinnacle database.

    Attributes:
        id (int): Primary key (inherited from PinnacleBase)
        patient_id (int): Patient ID in the Pinnacle system
        first_name (str): Patient's first name
        middle_name (str): Patient's middle name or initial
        last_name (str): Patient's last name
        patient_path (str): Path to the patient's data directory
        medical_record_number (str): Patient's medical record number
        encounter_number (str): Encounter or visit number
        primary_physician (str): Name of the primary physician
        attending_physician (str): Name of the attending physician
        referring_physician (str): Name of the referring physician
        radiation_oncologist (str): Name of the radiation oncologist
        oncologist (str): Name of the oncologist
        radiologist (str): Name of the radiologist
        prescription (str): Prescription details
        disease (str): Disease diagnosis
        diagnosis (str): Clinical diagnosis
        comment (str): Additional comments
        next_unique_plan_id (int): Next available plan ID
        next_unique_image_set_id (int): Next available image set ID
        gender (str): Patient's gender (M/F/Other)
        date_of_birth (datetime): Patient's date of birth
        dir_size (float): Size of the patient directory in bytes
        created_at (datetime): When the record was created
        updated_at (datetime): When the record was last updated
        
    Relationships:
        institution (Institution): The institution this patient belongs to
        image_set_list (List[ImageSet]): List of image sets for this patient
        plan_list (List[Plan]): List of treatment plans for this patient
    """

    __tablename__ = "Patient"

    # Identification and demographics
    patient_id: Mapped[Optional[int]] = Column("PatientID", Integer, nullable=True, doc="Patient ID in the Pinnacle system")
    first_name: Mapped[Optional[str]] = Column("FirstName", String(64), nullable=True, doc="Patient's first name")
    middle_name: Mapped[Optional[str]] = Column("MiddleName", String(64), nullable=True, doc="Patient's middle name or initial")
    last_name: Mapped[Optional[str]] = Column("LastName", String(64), nullable=True, doc="Patient's last name")
    patient_path: Mapped[Optional[str]] = Column("PatientPath", String(512), nullable=True, doc="Filesystem path to patient data")
    medical_record_number: Mapped[Optional[str]] = Column(
        "MedicalRecordNumber", String(64), nullable=True, doc="Patient's medical record number"
    )
    encounter_number: Mapped[Optional[str]] = Column("EncounterNumber", String(64), nullable=True, doc="Encounter or visit number")
    
    # Medical team
    primary_physician: Mapped[Optional[str]] = Column("PrimaryPhysician", String(128), nullable=True, doc="Name of primary physician")
    attending_physician: Mapped[Optional[str]] = Column("AttendingPhysician", String(128), nullable=True, doc="Name of attending physician")
    referring_physician: Mapped[Optional[str]] = Column("ReferringPhysician", String(128), nullable=True, doc="Name of referring physician")
    radiation_oncologist: Mapped[Optional[str]] = Column("RadiationOncologist", String(128), nullable=True, doc="Name of radiation oncologist")
    oncologist: Mapped[Optional[str]] = Column("Oncologist", String(128), nullable=True, doc="Name of oncologist")
    radiologist: Mapped[Optional[str]] = Column("Radiologist", String(128), nullable=True, doc="Name of radiologist")
    
    # Medical information
    prescription: Mapped[Optional[str]] = Column("Prescription", Text, nullable=True, doc="Prescription details")
    disease: Mapped[Optional[str]] = Column("Disease", String(256), nullable=True, doc="Disease diagnosis")
    diagnosis: Mapped[Optional[str]] = Column("Diagnosis", Text, nullable=True, doc="Clinical diagnosis")
    comment: Mapped[Optional[str]] = Column("Comment", Text, nullable=True, doc="Additional comments")
    
    # System fields
    next_unique_plan_id: Mapped[Optional[int]] = Column("NextUniquePlanID", Integer, nullable=True, doc="Next available plan ID")
    next_unique_image_set_id: Mapped[Optional[int]] = Column("NextUniqueImageSetID", Integer, nullable=True, doc="Next available image set ID")
    gender: Mapped[Optional[str]] = Column("Gender", String(16), nullable=True, doc="Patient's gender (M/F/Other)")
    date_of_birth: Mapped[Optional[datetime]] = Column("DateOfBirth", DateTime, nullable=True, doc="Patient's date of birth")
    dir_size: Mapped[Optional[float]] = Column("DirSize", Float, nullable=True, doc="Size of patient directory in bytes")

    # Relationships
    # Parent relationship - Patient belongs to an Institution
    institution_id: Mapped[Optional[int]] = Column(
        "InstitutionID", 
        Integer, 
        ForeignKey("Institution.ID", ondelete="CASCADE"),
        doc="Foreign key to the parent Institution"
    )
    institution: Mapped[Optional["Institution"]] = relationship(
        "Institution", 
        back_populates="patient_list",
        doc="The institution this patient belongs to"
    )

    # Child relationships
    image_set_list: Mapped[List["ImageSet"]] = relationship(
        "ImageSet", 
        back_populates="patient", 
        cascade="all, delete-orphan",
        doc="List of image sets for this patient"
    )
    
    plan_list: Mapped[List["Plan"]] = relationship(
        "Plan", 
        back_populates="patient", 
        cascade="all, delete-orphan",
        doc="List of treatment plans for this patient"
    )

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a new Patient instance.

        Args:
            **kwargs: Keyword arguments for setting attributes. Common attributes include:
                - first_name: Patient's first name
                - last_name: Patient's last name
                - middle_name: Patient's middle name/initial
                - medical_record_number: Patient's medical record number
                - date_of_birth: Patient's date of birth (datetime or date string)
                - gender: Patient's gender (M/F/Other)
                - institution_id: ID of the parent institution
                - Any other Patient attributes as defined in the model

        Example:
            >>> patient = Patient(
            ...     first_name="John",
            ...     last_name="Doe",
            ...     medical_record_number="MRN12345",
            ...     date_of_birth="1980-01-01",
            ...     gender="M"
            ... )
        """
        # Convert date string to datetime if needed
        if 'date_of_birth' in kwargs and isinstance(kwargs['date_of_birth'], str):
            try:
                from dateutil.parser import parse
                kwargs['date_of_birth'] = parse(kwargs['date_of_birth'])
            except (ValueError, TypeError):
                kwargs['date_of_birth'] = None
                
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of this Patient.
        
        Returns:
            str: A string containing the patient's ID, patient_id, and full name.
        """
        return f"<Patient(id={self.id}, patient_id='{self.patient_id}', name='{self.full_name}')>"

    @property
    def full_name(self) -> str:
        """
        Get the patient's full name.

        Returns:
            str: The patient's full name with components separated by spaces.
                
        Example:
            >>> patient = Patient(first_name="John", last_name="Doe")
            >>> patient.full_name
            'John Doe'
        """
        name_parts = []
        if self.first_name:
            name_parts.append(self.first_name.strip())
        if self.middle_name and self.middle_name.strip():
            name_parts.append(self.middle_name.strip())
        if self.last_name:
            name_parts.append(self.last_name.strip())

        return " ".join(name_parts).strip()

    @property
    def name(self) -> str:
        """
        Alias for full_name for backward compatibility.
        
        Returns:
            str: The patient's full name.
            
        .. deprecated:: 1.0.0
           Use :attr:`full_name` instead.
        """
        return self.full_name
        
    @property
    def dicom_name(self) -> str:
        """
        Get the patient's name in DICOM format: {last_name}^{first_name}^{middle_name}

        Returns:
            str: Patient's name formatted for DICOM.
                
        Example:
            >>> patient = Patient(first_name="John", middle_name="Q", last_name="Doe")
            >>> patient.dicom_name
            'Doe^John^Q'
        """
        return f"{self.last_name or ''}^{self.first_name or ''}^{self.middle_name or ''}"
    
    # For backward compatibility
    get_dicom_name = dicom_name.fget
    get_full_name = full_name.fget

    @property
    def age(self) -> Optional[int]:
        """
        Calculate the patient's current age in years based on date of birth.
        
        Returns:
            The patient's current age in years, or None if date of birth is not set.
            
        Example:
            >>> from datetime import date
            >>> patient = Patient(date_of_birth=date(1980, 1, 1))
            >>> # Assuming today's date is 2025-01-01
            >>> patient.age
            45
        """
        return self.get_age()
    
    def calculate_age(self, reference_date: Optional[date] = None) -> Optional[int]:
        """
        Calculate the patient's age based on birth date.
        
        Note: This is an alias for get_age() for backward compatibility.
        
        Args:
            reference_date: Optional date to calculate age against.
                         Defaults to today's date if not provided.

        Returns:
            The patient's age in years as of the reference date, or None if date of birth is not set.
        """
        return self.get_age(reference_date)
        
    def get_age(self, reference_date: Optional[date] = None) -> Optional[int]:
        """
        Calculate the patient's age in years as of a specific reference date.
        
        Args:
            reference_date: The date to calculate age as of. If None, uses today's date.
            
        Returns:
            The patient's age in years as of the reference date, or None if date of birth is not set.
            
        Example:
            >>> from datetime import date
            >>> patient = Patient(date_of_birth=date(1980, 1, 15))
            >>> patient.get_age(date(2025, 5, 21))  # After birthday
            45
            >>> patient.get_age(date(2024, 12, 31))  # Before birthday
            44
            >>> patient.get_age()  # Uses today's date
            45
        """
        if not self.date_of_birth:
            return None
            
        # Use provided date or today's date
        ref_date = reference_date if reference_date is not None else date.today()
        
        # If date_of_birth is a string, parse it (should be handled by the property setter)
        birth_date = self.date_of_birth
        if isinstance(birth_date, str):
            try:
                from dateutil.parser import parse
                birth_date = parse(birth_date).date()
            except (ValueError, TypeError):
                return None
        
        # If we have a datetime, convert to date
        if hasattr(birth_date, 'date'):
            birth_date = birth_date.date()
        
        # Calculate years difference
        years = ref_date.year - birth_date.year
        
        # Adjust if birthday hasn't occurred yet in the reference year
        if (ref_date.month, ref_date.day) < (birth_date.month, birth_date.day):
            years -= 1
            
        return years

    def get_plan_by_id(self, plan_id: Union[int, str]) -> Optional["Plan"]:
        """
        Get a plan by its ID.

        Args:
            plan_id: Plan ID to retrieve (can be int or string).

        Returns:
            Optional[Plan]: Plan with the specified ID, or None if not found.
            
        Example:
            >>> plan = patient.get_plan_by_id(1)
            >>> plan = patient.get_plan_by_id("1")
        """
        plan_id_str = str(plan_id)
        return next((p for p in self.plan_list if str(p.plan_id) == plan_id_str), None)

    def get_plan_by_name(self, plan_name: str) -> Optional["Plan"]:
        """
        Get a plan by its name (case-sensitive).

        Args:
            plan_name: Plan name to retrieve.

        Returns:
            Optional[Plan]: First plan with the specified name, or None if not found.
            
        Example:
            >>> plan = patient.get_plan_by_name("Prostate 78Gy")
        """
        return next((p for p in self.plan_list if p.name == plan_name), None)
        
    def get_plans_by_name(self, plan_name: str) -> List["Plan"]:
        """
        Get all plans with the given name (case-sensitive).
        
        Args:
            plan_name: Plan name to search for.
            
        Returns:
            List[Plan]: List of plans with the specified name (may be empty).
            
        Example:
            >>> plans = patient.get_plans_by_name("Prostate 78Gy")
        """
        return [p for p in self.plan_list if p.name == plan_name]

    def get_image_set_by_id(self, image_set_id: Union[int, str]) -> Optional["ImageSet"]:
        """
        Get an image set by its ID.

        Args:
            image_set_id: Image set ID to retrieve (can be int or string).

        Returns:
            Optional[ImageSet]: Image set with the specified ID, or None if not found.
            
        Example:
            >>> image_set = patient.get_image_set_by_id(1)
            >>> image_set = patient.get_image_set_by_id("1")
        """
        image_set_id_str = str(image_set_id)
        return next((i for i in self.image_set_list if str(i.image_set_id) == image_set_id_str), None)

    def get_image_set_by_name(self, image_set_name: str) -> Optional["ImageSet"]:
        """
        Get an image set by its name (case-sensitive).

        Args:
            image_set_name: Image set name to retrieve.

        Returns:
            Optional[ImageSet]: First image set with the specified name, or None if not found.
            
        Example:
            >>> image_set = patient.get_image_set_by_name("CT Simulation")
        """
        return next((i for i in self.image_set_list if i.name == image_set_name), None)
        
    def get_image_sets_by_name(self, image_set_name: str) -> List["ImageSet"]:
        """
        Get all image sets with the given name (case-sensitive).
        
        Args:
            image_set_name: Image set name to search for.
            
        Returns:
            List[ImageSet]: List of image sets with the specified name (may be empty).
            
        Example:
            >>> image_sets = patient.get_image_sets_by_name("CT Simulation")
        """
        return [i for i in self.image_set_list if i.name == image_set_name]
        
    def add_plan(self, plan: "Plan") -> None:
        """
        Add a plan to this patient.
        
        Args:
            plan: The Plan object to add.
            
        Raises:
            ValueError: If the plan is already associated with this patient.
            
        Example:
            >>> plan = Plan(name="New Plan")
            >>> patient.add_plan(plan)
        """
        if plan in self.plan_list:
            raise ValueError(f"Plan {plan.name} is already associated with this patient")
            
        self.plan_list.append(plan)
        plan.patient = self
        
    def add_image_set(self, image_set: "ImageSet") -> None:
        """
        Add an image set to this patient.
        
        Args:
            image_set: The ImageSet object to add.
            
        Raises:
            ValueError: If the image set is already associated with this patient.
            
        Example:
            >>> image_set = ImageSet(name="New CT")
            >>> patient.add_image_set(image_set)
        """
        if image_set in self.image_set_list:
            raise ValueError(f"Image set {image_set.name} is already associated with this patient")
            
        self.image_set_list.append(image_set)
        image_set.patient = self
        
    def to_dict(self, include_relationships: bool = False) -> Dict[str, Any]:
        """
        Convert the patient to a dictionary.
        
        Args:
            include_relationships: Whether to include related objects.
            
        Returns:
            Dict containing the patient's attributes.
            
        Example:
            >>> patient_dict = patient.to_dict()
        """
        data = {
            'id': self.id,
            'patient_id': self.patient_id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'medical_record_number': self.medical_record_number,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'institution_id': self.institution_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relationships:
            data['plans'] = [plan.to_dict() for plan in self.plan_list]
            data['image_sets'] = [image_set.to_dict() for image_set in self.image_set_list]
            
        return data
