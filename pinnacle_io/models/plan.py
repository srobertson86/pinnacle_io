"""
SQLAlchemy model for Pinnacle Plan data.

This module defines the Plan model which represents a treatment plan in the Pinnacle system.
A Plan is a container for one or more treatment Trials and is associated with a single Patient.
"""

from typing import Optional, List, Dict, Any, Union, TYPE_CHECKING

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime

from pinnacle_io.models.versioned_base import VersionedBase
from pinnacle_io.utils.patient_enum import PatientSetupEnum

if TYPE_CHECKING:
    from pinnacle_io.models.patient import Patient
    from pinnacle_io.models.patient_setup import PatientSetup
    from pinnacle_io.models.point import Point
    from pinnacle_io.models.roi import ROI
    from pinnacle_io.models.trial import Trial
    from pinnacle_io.models.image_set import ImageSet


class Plan(VersionedBase):
    """
    Model representing a Pinnacle treatment plan.

    A Plan is a container for one or more treatment Trials and is associated with a single Patient.
    It contains plan-specific information including metadata, status, and references to related
    entities like the primary CT image set and patient setup.

    Attributes:
        id (int): Primary key, inherited from VersionedBase.
        plan_id (int): The Pinnacle plan ID.
        name (str): The name of the plan.
        tool_type (str): Type of planning tool used.
        comment (str): Optional comments about the plan.
        physicist (str): Name of the physicist associated with the plan.
        dosimetrist (str): Name of the dosimetrist associated with the plan.
        primary_ct_image_set_id (Optional[int]): Foreign key to the primary CT image set.
        primary_image_type (str): Type of the primary image (e.g., 'CT', 'MR').
        pinnacle_version_description (str): Version of Pinnacle used to create the plan.
        is_new_plan_prefix (bool): Flag indicating if this is a new plan prefix.
        plan_is_locked (bool): Flag indicating if the plan is locked.
        ok_for_syntegra_in_launchpad (bool): Flag for Syntegra integration.
        fusion_id_array (str): Array of fusion IDs.
        created_date (datetime): When the plan was created.
        modified_date (datetime): When the plan was last modified.
        patient_id (int): Foreign key to the associated Patient.
        patient (Patient): The associated Patient object.
        primary_ct_image_set (Optional[ImageSet]): The primary CT image set.
        _patient_position (PatientSetup): The patient setup information.
        point_list (List[Point]): List of points associated with the plan.
        roi_list (List[ROI]): List of ROIs associated with the plan.
        trial_list (List[Trial]): List of trials associated with the plan.

    Example:
        ```python
        # Create a new plan
        plan = Plan(
            plan_id=1,
            name='Prostate SBRT',
            tool_type='IMRT',
            comment='Initial plan for review',
            physicist='John Smith',
            dosimetrist='Jane Doe',
            primary_image_type='CT',
            pinnacle_version_description='16.0.0',
            is_new_plan_prefix=True,
            plan_is_locked=False,
            ok_for_syntegra_in_launchpad=True
        )
        
        # Add plan to a patient
        patient.add_plan(plan)
        
        # Get a trial by ID
        trial = plan.get_trial_by_id(1)
        
        # Get a trial by name
        trial = plan.get_trial_by_name('Trial 1')
        ```
    """

    __tablename__ = "Plan"
    __mapper_args__ = {'eager_defaults': True}

    # Primary key is inherited from PinnacleBase
    plan_id: Mapped[Optional[int]] = Column("PlanID", Integer, nullable=True, index=True)
    name: Mapped[Optional[str]] = Column("PlanName", String(255), nullable=True)

    # Plan metadata
    tool_type: Mapped[Optional[str]] = Column("ToolType", String(64), nullable=True)
    comment: Mapped[Optional[str]] = Column("Comment", String(1024), nullable=True)
    physicist: Mapped[Optional[str]] = Column("Physicist", String(128), nullable=True)
    dosimetrist: Mapped[Optional[str]] = Column("Dosimetrist", String(128), nullable=True)
    primary_ct_image_set_id: Mapped[Optional[int]] = Column(
        "PrimaryCTImageSetID", Integer, ForeignKey("ImageSet.ID"), nullable=True, index=True
    )
    primary_image_type: Mapped[Optional[str]] = Column("PrimaryImageType", String(64), nullable=True)
    pinnacle_version_description: Mapped[Optional[str]] = Column(
        "PinnacleVersionDescription", String(128), nullable=True
    )

    # Plan status
    is_new_plan_prefix: Mapped[Optional[bool]] = Column("IsNewPlanPrefix", Boolean, default=False, nullable=True)
    plan_is_locked: Mapped[Optional[bool]] = Column("PlanIsLocked", Boolean, default=False, nullable=True)
    ok_for_syntegra_in_launchpad: Mapped[Optional[bool]] = Column(
        "OkForSyntegraInLaunchpad", Boolean, default=False, nullable=True
    )

    # Fusion information
    fusion_id_array: Mapped[Optional[str]] = Column("FusionIDArray", String(255), nullable=True)

    # Timestamps
    created_date: Mapped[Optional[datetime]] = Column("CreatedDate", DateTime, default=datetime.utcnow, nullable=True)
    modified_date: Mapped[Optional[datetime]] = Column(
        "ModifiedDate", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )

    # Parent Relationships
    patient_id: Mapped[Optional[int]] = Column(
        "PatientID", Integer, ForeignKey("Patient.ID", ondelete="CASCADE"), nullable=True, index=True
    )
    patient: Mapped[Optional["Patient"]] = relationship(
        "Patient", back_populates="plan_list", lazy="selectin"
    )
    
    primary_ct_image_set: Mapped[Optional["ImageSet"]] = relationship(
        "ImageSet",
        back_populates="plan_list",
        foreign_keys=[primary_ct_image_set_id],
        primaryjoin="Plan.primary_ct_image_set_id == ImageSet.id",
        lazy="selectin"
    )

    # Child Relationships
    _patient_position: Mapped[Optional["PatientSetup"]] = relationship(
        "PatientSetup",
        back_populates="plan",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    point_list: Mapped[List["Point"]] = relationship(
        "Point", back_populates="plan", cascade="all, delete-orphan", lazy="selectin"
    )
    roi_list: Mapped[List["ROI"]] = relationship(
        "ROI", back_populates="plan", cascade="all, delete-orphan", lazy="selectin"
    )
    trial_list: Mapped[List["Trial"]] = relationship(
        "Trial", back_populates="plan", cascade="all, delete-orphan", lazy="selectin"
    )

    def __init__(self, **kwargs):
        """
        Initialize a Plan instance.

        Args:
            **kwargs: Keyword arguments to set attributes on the new instance.
        """
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        """Return a string representation of the Plan."""
        return f"<Plan(id={self.id}, plan_id={self.plan_id}, name='{self.name}')>"

    def get_trial_by_id(self, trial_id: Union[int, str]) -> Optional["Trial"]:
        """
        Get a trial by its ID.

        Args:
            trial_id: The ID of the trial to retrieve. Can be an integer or string.

        Returns:
            The Trial object if found, None otherwise.

        Example:
            ```python
            # Get a trial by ID (works with string or int)
            trial = plan.get_trial_by_id(1)
            trial = plan.get_trial_by_id('1')
            
            if trial:
                print(f"Found trial: {trial.name}")
            else:
                print("Trial not found")
            ```
        """
        for trial in self.trial_list:
            if str(trial.trial_id) == str(trial_id):
                return trial
        return None

    def get_trial_by_name(self, trial_name: str) -> Optional["Trial"]:
        """
        Get a trial by its name.

        Args:
            trial_name: The name of the trial to retrieve.

        Returns:
            The Trial object if found, None otherwise.

        Example:
            ```python
            # Get a trial by name
            trial = plan.get_trial_by_name('Trial 1')
            
            if trial:
                print(f"Found trial with ID: {trial.trial_id}")
            else:
                print("Trial not found")
            ```
        """
        trial_name_lower = trial_name.lower()
        for trial in self.trial_list:
            if trial.name and trial.name.lower() == trial_name_lower:
                return trial
        return None

    def get_roi_by_id(self, roi_id: Union[int, str]) -> Optional["ROI"]:
        """
        Get an ROI by its ID.

        Args:
            roi_id: The ID of the ROI to retrieve. Can be an integer or string.

        Returns:
            The ROI object if found, None otherwise.
        """
        for roi in self.roi_list:
            if str(roi.id) == str(roi_id):
                return roi
        return None

    def get_roi_by_name(self, roi_name: str) -> Optional["ROI"]:
        """
        Get an ROI by its name (case-insensitive).

        Args:
            roi_name: The name of the ROI to retrieve.

        Returns:
            The ROI object if found, None otherwise.
        """
        roi_name_lower = roi_name.lower()
        for roi in self.roi_list:
            if roi.name and roi.name.lower() == roi_name_lower:
                return roi
        return None

    def get_point_by_id(self, point_id: Union[int, str]) -> Optional["Point"]:
        """
        Get a point by its ID.

        Args:
            point_id: The ID of the point to retrieve. Can be an integer or string.

        Returns:
            The Point object if found, None otherwise.
        """
        for point in self.point_list:
            if str(point.id) == str(point_id):
                return point
        return None

    def get_point_by_name(self, point_name: str) -> Optional["Point"]:
        """
        Get a point by its name (case-insensitive).

        Args:
            point_name: The name of the point to retrieve.

        Returns:
            The Point object if found, None otherwise.
        """
        point_name_lower = point_name.lower()
        for point in self.point_list:
            if point.name and point.name.lower() == point_name_lower:
                return point
        return None

    @property
    def patient_position(self) -> Optional[PatientSetupEnum]:
        """
        Get the patient position as a PatientSetupEnum.

        Returns:
            The patient position as a PatientSetupEnum, or None if not set.
            If the position cannot be determined, returns PatientSetupEnum.Unknown.

        Example:
            ```python
            position = plan.patient_position
            if position == PatientSetupEnum.HFS:
                print("Patient is in Head First Supine position")
            ```
        """
        if not self._patient_position:
            return None
            
        val = self._patient_position.patient_setup
        
        # If already a PatientSetupEnum, return as is
        if isinstance(val, PatientSetupEnum):
            return val
            
        # If string, try to convert to enum
        try:
            return PatientSetupEnum(val)
        except (ValueError, TypeError):
            return PatientSetupEnum.Unknown

    @property
    def plan_folder(self) -> str:
        """
        Get the folder name for this plan based on its plan_id.

        Returns:
            A string in the format 'Plan_X' where X is the plan_id.
            
        Example:
            ```python
            # For a plan with plan_id=3
            folder = plan.plan_folder  # Returns 'Plan_3'
            ```
        """
        return f"Plan_{self.plan_id}"

    def to_dict(self, include_related: bool = False) -> Dict[str, Any]:
        """
        Convert the Plan object to a dictionary.

        Args:
            include_related: If True, include related objects in the output.

        Returns:
            A dictionary representation of the Plan.
            
        Example:
            ```python
            # Get basic plan info
            plan_dict = plan.to_dict()
            
            # Get plan info with related objects
            plan_dict_full = plan.to_dict(include_related=True)
            ```
        """
        data = {
            'id': self.id,
            'plan_id': self.plan_id,
            'name': self.name,
            'tool_type': self.tool_type,
            'comment': self.comment,
            'physicist': self.physicist,
            'dosimetrist': self.dosimetrist,
            'primary_image_type': self.primary_image_type,
            'pinnacle_version_description': self.pinnacle_version_description,
            'is_new_plan_prefix': self.is_new_plan_prefix,
            'plan_is_locked': self.plan_is_locked,
            'ok_for_syntegra_in_launchpad': self.ok_for_syntegra_in_launchpad,
            'fusion_id_array': self.fusion_id_array,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'modified_date': self.modified_date.isoformat() if self.modified_date else None,
            'patient_position': self.patient_position.value if self.patient_position else None,
            'plan_folder': self.plan_folder
        }
        
        if include_related:
            if self.primary_ct_image_set:
                data['primary_ct_image_set'] = self.primary_ct_image_set.to_dict()
            if self.patient:
                data['patient'] = {'id': self.patient.id, 'patient_id': self.patient.patient_id}
                
            data['trial_count'] = len(self.trial_list)
            data['roi_count'] = len(self.roi_list)
            data['point_count'] = len(self.point_list)
            
            if include_related == 'full':
                data['trials'] = [trial.to_dict() for trial in self.trial_list]
                data['rois'] = [roi.to_dict() for roi in self.roi_list]
                data['points'] = [point.to_dict() for point in self.point_list]
        
        return data

    def add_trial(self, trial: "Trial") -> None:
        """
        Add a trial to this plan.

        Args:
            trial: The Trial object to add.
            
        Raises:
            ValueError: If the trial is already associated with this plan.
            
        Example:
            ```python
            # Create a new trial
            trial = Trial(trial_id=1, name='Trial 1')
            
            # Add it to the plan
            plan.add_trial(trial)
            ```
        """
        if trial in self.trial_list:
            raise ValueError(f"Trial with ID {trial.trial_id} is already associated with this plan")
            
        self.trial_list.append(trial)
        trial.plan = self

    def add_roi(self, roi: "ROI") -> None:
        """
        Add an ROI to this plan.

        Args:
            roi: The ROI object to add.
            
        Raises:
            ValueError: If the ROI is already associated with this plan.
        """
        if roi in self.roi_list:
            raise ValueError(f"ROI with ID {roi.id} is already associated with this plan")
            
        self.roi_list.append(roi)
        roi.plan = self

    def add_point(self, point: "Point") -> None:
        """
        Add a point to this plan.

        Args:
            point: The Point object to add.
            
        Raises:
            ValueError: If the point is already associated with this plan.
        """
        if point in self.point_list:
            raise ValueError(f"Point with ID {point.id} is already associated with this plan")
            
        self.point_list.append(point)
        point.plan = self
