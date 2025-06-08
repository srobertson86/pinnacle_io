"""Test configuration and fixtures for Pinnacle I/O tests."""

import pytest
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker

from pinnacle_io.models.pinnacle_base import PinnacleBase
from pinnacle_io.models.versioned_base import VersionedBase

# Create an in-memory SQLite database for testing
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

# Test models
class TestModel(PinnacleBase):
    """Test model that inherits from PinnacleBase."""
    __tablename__ = 'test_model'
    
    name = Column("Name", String, nullable=False)
    description = Column("Description", String, nullable=True)

class TestVersionedModel(VersionedBase):
    """Test model that inherits from VersionedBase."""
    __tablename__ = 'test_versioned_model'
    
    name = Column("Name", String, nullable=False)

@pytest.fixture(scope="module")
def setup_database():
    """Set up test database and create tables."""
    PinnacleBase.metadata.create_all(engine)
    VersionedBase.metadata.create_all(engine)
    yield
    PinnacleBase.metadata.drop_all(engine)
    VersionedBase.metadata.drop_all(engine)

@pytest.fixture
def db_session(setup_database):
    """Create a new database session for a test."""
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
