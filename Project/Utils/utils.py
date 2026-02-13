from datetime import datetime


def validate_date(date_text):
    try:
        date_obj = datetime.strptime(date_text, "%Y-%m-%d %H:%M")
        return date_obj, None
    except ValueError:
        return None, "Invalid format! Use YYYY-MM-DD HH:MM"