from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class Master(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    description: str
    specialty: str


class AvailablAppointment(BaseModel):
    id: int
    master: int
    client: Optional[int] = None
    date: date
    start_time: time
    end_time: time
    is_available: bool
