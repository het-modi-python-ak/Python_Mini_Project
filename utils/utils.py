from datetime import datetime

def validate_date(date_text):
    """Validates date format and ensures it is in the future."""
    try:
        date_obj = datetime.strptime(date_text, "%Y-%m-%d %H:%M")
        if date_obj < datetime.now():
            return None, "Due date must be in the future!"
        return date_obj, None
    except ValueError:
        return None, "Invalid format! Use YYYY-MM-DD HH:MM"
    