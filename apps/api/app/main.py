from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.core.config import APP_NAME
from app.api.routes import events, analytics, insights

Base.metadata.create_all(bind=engine)
app = FastAPI(title=APP_NAME, version="0.1.0", description="Website behaviour analytics MVP")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(events.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(insights.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok", "service": "webpulse-api"}
