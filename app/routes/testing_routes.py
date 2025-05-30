
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.database import get_db
from app.models.test_entry import TestEntry
from app.schemas.test_entry import TestEntryCreate, TestEntryOut

router = APIRouter()

@router.post("/entries", response_model=TestEntryOut)
# Define an endpoint that handles POST requests to /entries.
# The returned response will be validated and serialized using the TestEntryOut schema.

def create_entry(entry: TestEntryCreate, db: Session = Depends(get_db)):
    """
    entry: This is the parsed request body validated against the TestEntryCreate schema.
    db: A database session provided via dependency injection using FastAPI's Depends.
    """

    # Convert the validated Pydantic model to a dictionary and unpack it as keyword arguments
    # This allows you to initialize your SQLAlchemy model with matching fields.
    db_entry = TestEntry(**entry.model_dump())

    # Add the new entry object to the current database session
    db.add(db_entry)

    # Commit the transaction — this writes the new entry to the database
    db.commit()

    # Refresh the session to get the newly generated fields (like auto-incremented id)
    db.refresh(db_entry)
 
    # Return the created object — FastAPI will automatically serialize it to JSON
    # using the TestEntryOut Pydantic model
    return db_entry


@router.get("/entries", response_model=List[TestEntryOut])
def get_entries(db:Session = Depends(get_db)):
    return db.query(TestEntry).all()

@router.delete("/entries/{entry_id}", status_code=200)
def delete_entry(entry_id: UUID, db: Session = Depends(get_db)):
    db_entry = db.query(TestEntry).filter(TestEntry.id == entry_id).first()
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Entry deleted successfully"}