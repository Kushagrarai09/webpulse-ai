from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import analytics
from app.services.insights import generate_insights

router = APIRouter(prefix="/insights", tags=["insights"])

@router.get("")
def get_insights(website_id: str, db: Session = Depends(get_db)):
    ov = analytics.overview(db, website_id)
    return generate_insights(ov, analytics.forms(db, website_id), analytics.funnel(db, website_id))
