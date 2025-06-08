"""
Base SQLAlchemy model for Pinnacle data models.

This module provides base classes and utilities for all Pinnacle data models,
including common fields, methods, and custom types used throughout the application.
"""

from datetime import datetime, timezone
from typing import Any
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, declarative_base

from pinnacle_io.models.pinnacle_base import PinnacleBase


# Create the base class
Base = declarative_base()


class VersionedBase(PinnacleBase):
    """
    Base class for all Pinnacle versioned models.

    This class extends PinnacleBase with version tracking fields that are common
    across versioned models in the Pinnacle system. It provides automatic handling
    of version information and timestamps.

    Attributes:
        write_version (str): Version string used when the record was last written.
        create_version (str): Version string used when the record was created.
        login_name (str): Name of the user who last modified the record.
        create_time_stamp (datetime): When the record was created.
        write_time_stamp (datetime): When the record was last written.
        last_modified_time_stamp (datetime): When the record was last modified.

    Example:
        >>> class MyModel(VersionedBase):
        ...     __tablename__ = "my_models"
        ...     name: Mapped[str] = Column(String(100))
        ...
        >>> model = MyModel(
        ...     name="Test",
        ...     write_version="3.0.0",
        ...     login_name="user123"
        ... )
    """

    __abstract__ = True

    write_version: Mapped[str] = Column(
        "WriteVersion", 
        String(50), 
        default="",
        nullable=True,
        doc="Version string (e.g., '3.0.0') used when the record was last written"
    )
    
    create_version: Mapped[str] = Column(
        "CreateVersion", 
        String(50), 
        default="",
        nullable=True,
        doc="Version string (e.g., '3.0.0') used when the record was created"
    )
    
    login_name: Mapped[str] = Column(
        "LoginName", 
        String(100), 
        default="",
        nullable=True,
        doc="Name of the user who last modified the record (e.g., 'DOMAIN\\username')"
    )
    
    create_time_stamp: Mapped[datetime] = Column(
        "CreateTimeStamp", 
        DateTime, 
        default=lambda: datetime.now(timezone.utc),
        nullable=True,
        doc="Timestamp when the record was created (automatically set on creation)"
    )
    
    write_time_stamp: Mapped[datetime] = Column(
        "WriteTimeStamp", 
        DateTime, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
        doc="Timestamp when the record was last written (automatically updated on save)"
    )
    
    last_modified_time_stamp: Mapped[datetime] = Column(
        "LastModifiedTimeStamp", 
        DateTime, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
        doc="Timestamp when the record was last modified (automatically updated on change)"
    )

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a new versioned model instance.
        
        This constructor handles special cases for version-related fields, including:
        - Processing of 'object_version' or 'ObjectVersion' dictionary
        - Automatic timestamp initialization
        - Version string handling
        
        Args:
            **kwargs: Field values to set on the model. Can include:
                - object_version or ObjectVersion: Dictionary of version-related fields
                - write_version: Version string for when the record was last written
                - create_version: Version string for when the record was created
                - login_name: Name of the user who last modified the record
                - create_time_stamp: When the record was created
                - write_time_stamp: When the record was last written
                - last_modified_time_stamp: When the record was last modified
                - Any other fields defined on the model
                
        Example:
            >>> model = VersionedModel(
            ...     name="Test",
            ...     object_version={
            ...         "WriteVersion": "3.0.0",
            ...         "LoginName": "DOMAIN\\user123"
            ...     }
            ... )
        """
        # Handle object_version dictionary if present (case-insensitive)
        object_version = kwargs.pop("object_version", kwargs.pop("ObjectVersion", None))
        if object_version and isinstance(object_version, dict):
            # Convert all keys to lowercase for case-insensitive matching
            version_data = {k.lower(): v for k, v in object_version.items()}
            
            # Map version fields to their corresponding kwargs
            version_mapping = {
                'writeversion': 'write_version',
                'createversion': 'create_version',
                'loginname': 'login_name',
                'createtimestamp': 'create_time_stamp',
                'writetimestamp': 'write_time_stamp',
                'lastmodifiedtimestamp': 'last_modified_time_stamp',
            }
            
            # Update kwargs with version data, preserving any explicitly passed values
            for src, dest in version_mapping.items():
                if src in version_data and dest not in kwargs:
                    kwargs[dest] = version_data[src]

        # Set default timestamps if not provided
        now = datetime.now(timezone.utc)
        if 'create_time_stamp' not in kwargs:
            kwargs['create_time_stamp'] = now
        if 'write_time_stamp' not in kwargs:
            kwargs['write_time_stamp'] = now
        if 'last_modified_time_stamp' not in kwargs:
            kwargs['last_modified_time_stamp'] = now

        super().__init__(**kwargs)
        
        # Set timestamps if not provided
        now = datetime.now(timezone.utc)
        if self.create_time_stamp is None:
            self.create_time_stamp = now
        if self.write_time_stamp is None:
            self.write_time_stamp = now
        if self.last_modified_time_stamp is None:
            self.last_modified_time_stamp = now

