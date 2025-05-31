from sqlalchemy import Column, ForeignKey, String, Enum, DateTime, Boolean
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import enum
import uuid


def round_to_minute(dt: datetime) -> datetime:
    return dt.replace(microsecond=0)


# USER:
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(
        DateTime, default=lambda: round_to_minute(datetime.now(timezone.utc))
    )
    is_verified = Column(Boolean, default=False)


# FRIENDSHIPS


class FriendshipStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    blocked = "blocked"


class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    friend_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(
        Enum(FriendshipStatus), default=FriendshipStatus.pending, nullable=False
    )
    created_at = Column(
        DateTime, default=lambda: round_to_minute(datetime.now(timezone.utc))
    )

    user = relationship("User", foreign_keys=[user_id], backref="friends_sent")
    friend = relationship("User", foreign_keys=[friend_id], backref="friends_received")
