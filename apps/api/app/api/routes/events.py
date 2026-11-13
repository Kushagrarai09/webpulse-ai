from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.models.event import Event
from app.schemas.events import EventIn, BatchIn

router = APIRouter(prefix="/events", tags=["events"])

def save_event(db: Session, item: EventIn):
    existing = db.scalar(select(Event).where(Event.event_id == item.event_id))
    if existing:
        return False
    db.add(Event(**item.model_dump()))
    return True

@router.post("")
def ingest(item: EventIn, db: Session = Depends(get_db)):
    created = save_event(db, item)
    db.commit()
    return {"accepted": 1 if created else 0, "duplicates": 0 if created else 1}

@router.post("/batch")
def ingest_batch(batch: BatchIn, db: Session = Depends(get_db)):
    accepted = sum(save_event(db, item) for item in batch.events)
    db.commit()
    return {"accepted": accepted, "duplicates": len(batch.events) - accepted}
