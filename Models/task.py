from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from zoneinfo import ZoneInfo

KOLKATA_TZ = ZoneInfo("Asia/Kolkata")

class Task(BaseModel):
    id: int
    title:str
    description: str
    start_date: str = Field(default_factory=lambda: datetime.now(tz=KOLKATA_TZ).strftime("%Y-%m-%d"))
    due_date: str 
    status: str = Field(default='Pending') 
    
    @field_validator("due_date")
    @classmethod
    def due_validator(cls, value):
        try:
            due_date_obj = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid format! Use YYYY-MM-DD")

        today = datetime.now(tz=KOLKATA_TZ).date()
        if due_date_obj <= today:
            raise ValueError("Due date must be in the future!")
        return value
