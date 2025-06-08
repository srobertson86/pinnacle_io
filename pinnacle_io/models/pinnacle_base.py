"""
Base SQLAlchemy model for Pinnacle data models.

This module provides base classes and utilities for all Pinnacle data models,
including common fields and methods used throughout the application.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TypeVar
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.orm import Mapped, declarative_base

from pinnacle_io.utils.converters import (
    convert_integer,
    convert_float,
    convert_string,
    convert_boolean,
    convert_datetime,
)

# Create the base class
Base = declarative_base()

# Type variable for model instances
T = TypeVar('T', bound='PinnacleBase')


class PinnacleBase(Base):
    """
    Base class for all Pinnacle models.

    This class provides common functionality and fields for all models.
    It is defined as abstract so it won't create its own table.

    Attributes:
        id (int): Primary key for the model.
        created_at (datetime): When the record was created.
        updated_at (datetime): When the record was last updated.
    """

    __abstract__ = True

    # Common primary key for all models - using 'ID' to match database schema
    id: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)

    # Common tracking fields with proper type hints
    created_at: Mapped[datetime] = Column(
        "CreatedAt", 
        DateTime, 
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        doc="Timestamp when the record was created"
    )
    
    updated_at: Mapped[datetime] = Column(
        "UpdatedAt", 
        DateTime, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        doc="Timestamp when the record was last updated"
    )

    def __repr__(self) -> str:
        """
        Return a string representation of the model instance.
        
        Returns:
            str: A string representation including the class name and primary key.
        """
        return f"<{self.__class__.__name__}(id={self.id})>"

    def to_dict(self, exclude: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Convert the model instance to a dictionary.
        
        Args:
            exclude: Optional list of field names to exclude from the result.
            
        Returns:
            Dict containing the model's field names and values.
        """
        if exclude is None:
            exclude = []
            
        result = {}
        for column in self.__table__.columns:
            # Skip excluded fields
            if column.name in exclude or column.name in ['ID', 'CreatedAt', 'UpdatedAt']:
                continue
                
            # Get the value and handle special cases
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            
            result[column.name] = value
            
        return result

    @classmethod
    def _get_column_to_field_mapping(cls) -> Dict[str, str]:
        """
        Get mapping from database column names to model field names.
        
        Returns:
            Dict mapping database column names to model field names.
        """
        mapping = {}
        for class_field_name in cls.__mapper__.attrs.keys():
            attr = getattr(cls, class_field_name)

            if hasattr(attr, "property") and hasattr(attr.property, "columns"):
                column = attr.property.columns[0]
                db_column_name = column.name
                mapping[db_column_name] = class_field_name

        return mapping

    @classmethod
    def _get_relationship_mapping(cls):
        """
        Get mapping of relationship attributes in the model
        Returns: {"relationship_name": {"type": "one-to-many"|"many-to-one"|"one-to-one", "target_class": Class}}
        """
        mapping = {}

        for class_field_name in cls.__mapper__.attrs.keys():
            attr = getattr(cls, class_field_name)

            if hasattr(attr, "property") and hasattr(attr.property, "direction"):
                # This is a relationship attribute
                relationship_info = {}

                # Determine relationship type based on uselist property
                if hasattr(attr.property, "uselist"):
                    if attr.property.uselist:
                        relationship_info["type"] = "one-to-many"
                    else:
                        relationship_info["type"] = "one-to-one"
                else:
                    # Default to one-to-many if uselist not specified
                    relationship_info["type"] = "one-to-many"

                # Get the target class
                if hasattr(attr.property, "mapper") and hasattr(
                    attr.property.mapper, "class_"
                ):
                    relationship_info["target_class"] = attr.property.mapper.class_

                mapping[class_field_name] = relationship_info

        return mapping

    @staticmethod
    def _normalize_key(key):
        """
        Normalize a key by converting to lowercase and removing underscores.

        Args:
            key (str): The key to normalize

        Returns:
            str: The normalized key
        """
        return key.lower().replace("_", "")

    def _get_mapped_kwargs(
        self,
        kwargs: Dict[str, Any],
        model_fields: Dict[str, str],
        database_columns: Dict[str, str],
        relationship_mapping: Dict[str, Dict[str, Any]]
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """Process and map regular field kwargs to their database column names.
        
        This method separates relationship fields from regular fields and normalizes
        the field names to handle case and underscore differences between the Python
        model attributes and database column names.
        
        Args:
            kwargs: Original keyword arguments passed to the model constructor
            model_fields: Mapping of model field names to database column names
            database_columns: Mapping of database column names to model field names
            relationship_mapping: Mapping of relationship configurations
            
        Returns:
            A tuple containing two dictionaries:
            - mapped_kwargs: Regular field names mapped to their values
            - relationship_kwargs: Relationship field names mapped to their values
            
        Example:
            >>> model_fields = {'name': 'Name', 'description': 'Description'}
            >>> db_columns = {'name': 'Name', 'description': 'Description'}
            >>> rel_mapping = {'relationship_field': {'type': 'one-to-many'}}
            >>> model._get_mapped_kwargs(
            ...     {'Name': 'test', 'relationship_field': [...]},
            ...     model_fields,
            ...     db_columns,
            ...     rel_mapping
            ... )
            ({'name': 'test'}, {'relationship_field': [...]})
        """
        mapped_kwargs: Dict[str, Any] = {}
        relationship_kwargs: Dict[str, Any] = {}
        
        for key, value in kwargs.items():
            if value is None:
                continue
                
            # Normalize the key (lowercase and remove underscores)
            normalized_key = self._normalize_key(key)

            # Try to find a matching relationship field (case-insensitive and no underscores)
            relationship_field = next(
                (k for k in relationship_mapping.keys() 
                 if self._normalize_key(k) == normalized_key),
                None,
            )
            
            if relationship_field:
                # This is a relationship field
                relationship_kwargs[relationship_field] = value
            else:
                # This is a regular field, map to database column name
                if key in model_fields:
                    mapped_kwargs[key] = value
                else:
                    mapped_key = database_columns.get(normalized_key, normalized_key)
                    if mapped_key in model_fields:
                        mapped_kwargs[mapped_key] = value
                        
        return mapped_kwargs, relationship_kwargs
    
    def _process_relationships(
        self,
        relationship_kwargs: Dict[str, Any],
        relationship_mapping: Dict[str, Dict[str, Any]]
    ) -> None:
        """Process relationship attributes after parent initialization.
        
        This method processes relationship fields that were separated from regular
        fields during initialization. It handles different types of relationships
        (one-to-many, one-to-one) by delegating to the appropriate handler method.
        
        Args:
            relationship_kwargs: Dictionary mapping relationship field names to their values
            relationship_mapping: Dictionary containing relationship configurations
            
        Raises:
            AttributeError: If a relationship field exists in the mapping but not on the model
            ValueError: If an unknown relationship type is encountered
            
        Example:
            >>> rel_kwargs = {'beams': [beam1, beam2], 'dose': dose_obj}
            >>> rel_mapping = {
            ...     'beams': {'type': 'one-to-many', 'target_class': Beam},
            ...     'dose': {'type': 'one-to-one', 'target_class': Dose}
            ... }
            >>> model._process_relationships(rel_kwargs, rel_mapping)
        """
        for rel_field, rel_value in relationship_kwargs.items():
            if rel_value is None:
                continue
                
            if rel_field not in relationship_mapping:
                continue
                
            if not hasattr(self, rel_field):
                raise AttributeError(
                    f"Relationship field '{rel_field}' not found on {self.__class__.__name__}"
                )
                
            rel_info = relationship_mapping[rel_field]
            rel_type = rel_info.get("type")
            target_class = rel_info.get("target_class")
            
            if rel_type == "one-to-many":
                self._process_one_to_many_relationship(rel_field, rel_value, target_class)
            elif rel_type == "one-to-one":
                self._process_one_to_one_relationship(rel_field, rel_value, target_class)
            else:
                raise ValueError(f"Unknown relationship type: {rel_type}")
    
    def _process_one_to_many_relationship(
        self,
        rel_field: str,
        rel_value: Any,
        target_class: Optional[type] = None
    ) -> None:
        """Process a one-to-many relationship.
        
        This method handles setting up one-to-many relationships. It can process
        both model instances and dictionaries that should be converted to model
        instances.
        
        Args:
            rel_field: Name of the relationship field on the model
            rel_value: Single item or list of items to add to the relationship
            target_class: The target model class for the relationship
            
        Raises:
            TypeError: If rel_value is not iterable or items cannot be converted
                     to the target class
            
        Example:
            >>> model._process_one_to_many_relationship(
            ...     'beams',
            ...     [{'name': 'Beam1'}, beam2],
            ...     target_class=Beam
            ... )
        """
        if not rel_value:
            return
            
        # Convert single item to list for uniform processing
        if not isinstance(rel_value, (list, tuple, set)):
            rel_value = [rel_value]
            
        # Initialize the list if it doesn't exist
        if getattr(self, rel_field) is None:
            setattr(self, rel_field, [])
        
        # Get the current relationship collection
        relationship = getattr(self, rel_field)
        
        # Add items to the relationship list
        for item in rel_value:
            if item is None:
                continue
                
            # Convert dict to model instance if target class is provided
            if target_class and not isinstance(item, target_class) and isinstance(item, dict):
                try:
                    item = target_class(**item)
                except Exception as e:
                    raise TypeError(
                        f"Failed to convert dict to {target_class.__name__} for "
                        f"field '{rel_field}': {str(e)}"
                    ) from e
            
            # Ensure the item is of the correct type
            if target_class and not isinstance(item, target_class):
                raise TypeError(
                    f"Expected {target_class.__name__} for field '{rel_field}', "
                    f"got {type(item).__name__}"
                )
                
            relationship.append(item)
    
    def _process_one_to_one_relationship(
        self,
        rel_field: str,
        rel_value: Any,
        target_class: Optional[type] = None
    ) -> None:
        """Process a one-to-one relationship.
        
        This method handles setting up one-to-one relationships. It can process
        both model instances and dictionaries that should be converted to model
        instances.
        
        Args:
            rel_field: Name of the relationship field on the model
            rel_value: The value to set for the relationship
            target_class: The target model class for the relationship
            
        Raises:
            TypeError: If rel_value cannot be converted to the target class
            
        Example:
            >>> model._process_one_to_one_relationship(
            ...     'dose',
            ...     {'value': 50.0, 'unit': 'cGy'},
            ...     target_class=Dose
            ... )
        """
        if rel_value is None:
            return
            
        # Convert dict to model instance if target class is provided
        if target_class and not isinstance(rel_value, target_class):
            if isinstance(rel_value, dict):
                try:
                    rel_value = target_class(**rel_value)
                except Exception as e:
                    raise TypeError(
                        f"Failed to convert dict to {target_class.__name__} for "
                        f"field '{rel_field}': {str(e)}"
                    ) from e
            else:
                raise TypeError(
                    f"Expected {target_class.__name__} or dict for field "
                    f"'{rel_field}', got {type(rel_value).__name__}"
                )
        
        setattr(self, rel_field, rel_value)
    
    def __init__(self, **kwargs):
        """Initialize a new instance with the given keyword arguments."""
        # Ensure created_at is set if not provided
        now = datetime.now(timezone.utc)
        created_at = kwargs.pop('created_at', kwargs.pop('CreatedAt', None))
        updated_at = kwargs.pop('updated_at', kwargs.pop('UpdatedAt', None))
        if created_at is None:
            kwargs['created_at'] = now
        if updated_at is None:
            kwargs['updated_at'] = now
        
        # Get database column and relationship mappings
        database_columns = {
            self._normalize_key(k): v
            for k, v in self._get_column_to_field_mapping().items()
        }
        model_fields = {v: k for k, v in database_columns.items()}
        relationship_mapping = self._get_relationship_mapping()
        
        # Process and separate regular fields from relationships
        mapped_kwargs, relationship_kwargs = self._get_mapped_kwargs(
            kwargs, model_fields, database_columns, relationship_mapping
        )
        
        # Initialize the model with the mapped fields
        super().__init__(**mapped_kwargs)
        
        # Process relationships after parent initialization
        self._process_relationships(relationship_kwargs, relationship_mapping)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an attribute on the model with type conversion.
        
        This method is called when setting attributes on the model instance.
        It performs type conversion for SQLAlchemy columns based on their
        column types before setting the value.
        
        Args:
            name: The name of the attribute to set
            value: The value to set
            
        Raises:
            ValueError: If the value cannot be converted to the column type
            TypeError: If the value is of an incompatible type
            
        Example:
            >>> model = MyModel()
            >>> model.some_field = "123"  # Will be converted to int if column is Integer
        """
        # Skip private attributes and SQLAlchemy internals
        if name.startswith("_") or name in ["metadata", "registry"]:
            super().__setattr__(name, value)
            return

        # Get the attribute from the class if it exists
        if hasattr(self.__class__, name):
            attr = getattr(self.__class__, name)

            # Check if this is a SQLAlchemy column
            if hasattr(attr, "property") and hasattr(attr.property, "columns"):
                column = attr.property.columns[0]
                value = self._convert_value_for_column(column, value, name)

        # Set the converted value
        super().__setattr__(name, value)

    def _convert_value_for_column(self, column, value: Any, field_name: str) -> Any:
        """Convert value based on SQLAlchemy column type.

        Args:
            column: SQLAlchemy column definition
            value: Value to convert
            field_name: Name of the field (for error messages)

        Returns:
            Converted value

        Raises:
            ValueError: If conversion fails for a non-nullable column
        """
        # Handle None values
        if value is None:
            if (
                not column.nullable
                and column.default is None
                and not column.server_default
            ):
                raise ValueError(
                    f"Cannot set NULL for non-nullable column '{field_name}'. "
                    "No default value is specified."
                )
            return value

        column_type = column.type
        converted_value = None

        try:
            # Integer conversion
            if isinstance(column_type, Integer):
                converted_value = convert_integer(value)

            # Float/Numeric conversion
            elif isinstance(column_type, Float):
                converted_value = convert_float(value)

            # String/Text conversion
            elif isinstance(column_type, (String, Text)):
                converted_value = convert_string(value, field_name)
                # Check max length
                if (
                    converted_value
                    and column_type
                    and hasattr(column_type, "length")
                    and column_type.length
                ):
                    if len(converted_value) > column_type.length:
                        print(
                            f"Warning: Truncating {field_name} from {len(converted_value)} to {column_type.length} characters"
                        )
                        converted_value = converted_value[: column_type.length]

            # Boolean conversion
            elif isinstance(column_type, Boolean):
                converted_value = convert_boolean(value)

            # DateTime conversion
            elif isinstance(column_type, DateTime):
                converted_value = convert_datetime(value)

            # Default: return as-is
            else:
                converted_value = value

            # Check if conversion returned None for a non-nullable column
            if converted_value is None and not column.nullable:
                if column.default is not None or column.server_default is not None:
                    # Let SQLAlchemy handle the default value
                    return None
                raise ValueError(
                    f"Conversion of value '{value}' for non-nullable column '{field_name}' "
                    f"resulted in NULL. Column type: {column_type}"
                )

            return converted_value

        except (ValueError, TypeError) as e:
            if (
                not column.nullable
                and column.default is None
                and not column.server_default
            ):
                raise ValueError(
                    f"Failed to convert value '{value}' for non-nullable column "
                    f"'{field_name}': {str(e)}"
                ) from e

            print(
                f"Warning: Could not convert {field_name}='{value}' to {column_type}: {e}"
            )
            return value  # Return original value if conversion fails
