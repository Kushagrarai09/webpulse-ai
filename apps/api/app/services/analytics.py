from sqlalchemy import select
from sqlalchemy.orm import Session
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from app.models.event import Event

def events_for(db: Session, website_id: str, days: int = 30):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    return list(db.scalars(select(Event).where(Event.website_id == website_id, Event.occurred_at >= since)))

def overview(db: Session, website_id: str, days: int = 30):
    events = events_for(db, website_id, days)
    visitors = {e.visitor_id for e in events}; sessions = {e.session_id for e in events}
    purchases = sum(e.event_type == "purchase" for e in events)
    submits = sum(e.event_type == "form_submit" for e in events); starts = sum(e.event_type == "form_start" for e in events)
    opens = sum(e.event_type == "email_open" for e in events); clicks = sum(e.event_type == "email_click" for e in events)
    return {"website_id":website_id,"period_days":days,"events":len(events),"visitors":len(visitors),"sessions":len(sessions),"purchases":purchases,"conversion_rate":round(purchases/max(len(sessions),1)*100,2),"form_starts":starts,"form_submissions":submits,"form_abandonment_rate":round(max(starts-submits,0)/max(starts,1)*100,2),"email_opens":opens,"email_clicks":clicks,"email_click_rate":round(clicks/max(opens,1)*100,2)}

def funnel(db: Session, website_id: str):
    events=events_for(db,website_id,30); steps=["page_view","form_start","form_submit","purchase"]; result=[]; previous=None
    for step in steps:
        count=len({e.session_id for e in events if e.event_type==step})
        result.append({"step":step,"sessions":count,"conversion_from_previous":round(count/previous*100,1) if previous else 100.0}); previous=max(count,1)
    return result

def forms(db: Session, website_id: str):
    events=events_for(db,website_id,30); stats=defaultdict(lambda:{"starts":0,"submissions":0,"abandons":0})
    for e in events:
        key=e.properties.get("form_id","unknown")
        if e.event_type=="form_start":stats[key]["starts"]+=1
        elif e.event_type=="form_submit":stats[key]["submissions"]+=1
        elif e.event_type=="form_abandon":stats[key]["abandons"]+=1
    return [{"form_id":k,**v,"abandonment_rate":round(v["abandons"]/max(v["starts"],1)*100,1)} for k,v in stats.items()]

def email(db: Session, website_id: str):
    events=[e for e in events_for(db,website_id,30) if e.event_type in ("email_open","email_click")]; campaigns=defaultdict(lambda:{"opens":0,"clicks":0})
    for e in events:
        key=e.properties.get("campaign_id","default"); campaigns[key]["opens" if e.event_type=="email_open" else "clicks"]+=1
    return [{"campaign_id":k,**v,"click_to_open_rate":round(v["clicks"]/max(v["opens"],1)*100,1)} for k,v in campaigns.items()]

def plugins(db: Session, website_id: str):
    events=[e for e in events_for(db,website_id,30) if e.event_type in ("plugin_used","plugin_error")]; stats=defaultdict(lambda:{"uses":0,"errors":0})
    for e in events:
        key=e.properties.get("plugin_id","unknown"); stats[key]["uses" if e.event_type=="plugin_used" else "errors"]+=1
    return [{"plugin_id":k,**v} for k,v in stats.items()]
