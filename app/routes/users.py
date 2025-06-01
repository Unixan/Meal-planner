from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Friendship
from app.schemas.schemas import (
    UserCreate,
    UserOut,
    UserLogin,
    FriendshipOut,
    FriendshipCreate,
)
from app.security import hash_password, verify_password
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    normalized_email = user.email.lower()
    db_user = db.query(User).filter(User.email == normalized_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    username = user.username or normalized_email.split("@")[0]

    new_user = User(email=normalized_email, password_hash=hashed_pw, username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    normalized_email = user.email.lower()
    db_user = db.query(User).filter(User.email == normalized_email).first()
    if not db_user or not verify_password(user.password, str(db_user.password_hash)):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not bool(db_user.is_verified):
        raise HTTPException(status_code=403, detail="Email not verified.")
    fake_token = "abc123token"

    return {"token": fake_token, "message": "Login successful"}


@router.post("/{user_id}/friends", response_model=FriendshipOut)
def send_friend_request(
    user_id: UUID, request: FriendshipCreate, db: Session = Depends(get_db)
):
    if user_id == request.friend_id:
        raise HTTPException(status_code=400, detail="You cannot friend yourself.")

    # Check if friend exists
    target_user = db.query(User).filter(User.id == request.friend_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Check for existing friendship
    existing = (
        db.query(Friendship)
        .filter(
            Friendship.user_id == user_id, Friendship.friend_id == request.friend_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="Friend request already sent or already friends"
        )

    # Create friendship request
    friendship = Friendship(
        user_id=user_id, friend_id=request.friend_id, status="pending"
    )
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship
