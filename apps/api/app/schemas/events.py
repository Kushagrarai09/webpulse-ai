from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from typing import Any

class EventIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: str = Field(min_length=1, max_length=120)
    website_id: str = Field(min_length=1, max_length=120)
    visitor_id: str = Field(min_length=1, max_length=120)
    session_id: str = Field(min_length=1, max_length=120)
    event_type: str = Field(min_length=1, max_length=60)
    event_name: str = Field(default="", max_length=200)
    source: str = Field(default="web", max_length=40)
    properties: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BatchIn(BaseModel):
    events: list[EventIn] = Field(min_length=1, max_length=1000)
