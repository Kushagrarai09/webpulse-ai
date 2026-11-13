import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./webpulse.db")
APP_NAME = "WebPulse AI API"
