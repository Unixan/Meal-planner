from sqlalchemy import Column, String
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class TestEntry(Base):
    __tablename__ = "test_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    note = Column(String, nullable=True)
