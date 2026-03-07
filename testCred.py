import os

# 1. Manually force the environment variable so the code finds your credentials
os.environ["GOOGLE_CREDENTIALS_PATH"] = "client_secret_792757793166-8v3pal4d0jpha3eurppus0ed7f25kg1l.apps.googleusercontent.com.json"

# 2. Import and initialize the calendar
from src.utils.google_calendar import get_calendar

print("🔄 Starting Google Calendar authentication...")
calendar = get_calendar()

# 3. Check if it worked
if calendar.is_available():
    print("✅ Success! token.json has been generated.")
else:
    print("❌ Failed to authenticate. Check if credentials.json is in this folder.")