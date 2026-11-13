import os,sys,uuid,random
from datetime import datetime,timedelta,timezone
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),"../apps/api")))
from app.core.database import Base,engine,SessionLocal
from app.models.event import Event
Base.metadata.create_all(bind=engine); db=SessionLocal(); random.seed(17); now=datetime.now(timezone.utc)
types=["page_view","form_start","form_submit","form_abandon","purchase","email_open","email_click","plugin_used","plugin_error"]
for i in range(500):
 typ=random.choices(types,weights=[35,15,8,7,4,12,5,12,2])[0]; props={}
 if typ in ("form_start","form_submit","form_abandon"):props["form_id"]=random.choice(["signup","demo_request"])
 if typ in ("email_open","email_click"):props["campaign_id"]=random.choice(["welcome","weekly_digest"])
 if typ in ("plugin_used","plugin_error"):props["plugin_id"]=random.choice(["reviews","chat_widget","recommendations"])
 db.add(Event(event_id=str(uuid.uuid4()),website_id="demo-store",visitor_id=f"visitor-{random.randint(1,180)}",session_id=f"session-{random.randint(1,260)}",event_type=typ,event_name=typ.replace("_"," ").title(),source="demo",properties=props,occurred_at=now-timedelta(days=random.randint(0,29),hours=random.randint(0,23))))
db.commit(); db.close(); print("Inserted 500 demo events for website_id=demo-store")
