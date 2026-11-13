from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/overview")
def get_overview(website_id: str = Query(...), days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    return analytics.overview(db, website_id, days)

@router.get("/funnel")
def get_funnel(website_id: str = Query(...), db: Session = Depends(get_db)):
    return analytics.funnel(db, website_id)

@router.get("/forms")
def get_forms(website_id: str = Query(...), db: Session = Depends(get_db)):
    return analytics.forms(db, website_id)

@router.get("/email")
def get_email(website_id: str = Query(...), db: Session = Depends(get_db)):
    return analytics.email(db, website_id)

@router.get("/plugins")
def get_plugins(website_id: str = Query(...), db: Session = Depends(get_db)):
    return analytics.plugins(db, website_id)
