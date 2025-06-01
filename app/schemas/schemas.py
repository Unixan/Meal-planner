from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime
import re
from uuid import UUID


# USER:
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        errors = []

        if len(v) < 8:
            errors.append("at least 8 characters")
        if not re.search(r"[A-Z]", v):
            errors.append("at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            errors.append("at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            errors.append("at least one digit")
        if not re.search(r"[\W_]", v):
            errors.append("at least one special character")

        if errors:
            raise ValueError("Password must contain " + ", ".join(errors))

        return v


    @field_validator("username")
    def validate_username(cls, value):
        if value is None:
            return value

        cleaned = value.strip()
        letter_count = sum(1 for c in cleaned if c.isalpha())
        if letter_count < 3:
            raise ValueError("Username must contain at least 3 letters.")

        for char in cleaned:
            if not (char.isalpha() or char.isspace()):
                raise ValueError("Username can only contain letters and spaces.")

        return cleaned



class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

#FRIENDSHIPS

class FriendshipStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    blocked = "blocked"

class FriendshipCreate(BaseModel):
    friend_id: UUID

class FriendshipOut(BaseModel):
    id: UUID
    user_id: UUID
    friend_id: UUID
    status: FriendshipStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)