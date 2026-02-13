from datetime import datetime
from zoneinfo import ZoneInfo

# Fixed timezone so server clock never affects task logic
IST = ZoneInfo("Asia/Kolkata")

# Returns current IST time
def now_ist():
    return datetime.now(IST)

# Validates date format and ensures it is in the future
def validate_date(date_text):
    try:
        date_obj = datetime.strptime(date_text, "%Y-%m-%d %H:%M")
        date_obj = date_obj.replace(tzinfo=IST)
        if date_obj < now_ist():
            return None, "Due date must be in the future"
        return date_obj, None
    except ValueError:
        return  None, "invalid date format use YYYY-MM-DD HH:MM"
