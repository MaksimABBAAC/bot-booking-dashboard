import datetime
from aiogram.filters.callback_data import CallbackData


class MastersCallbackFactory(CallbackData, prefix="master_"):
    master_id: int

class DateCallbackFactory(CallbackData, prefix="date"):
    master_id: int
    date: str

    @classmethod
    def from_date_obj(cls, master_id: int, date_obj: datetime.date):
        return cls(master_id=master_id, date=date_obj.isoformat())

class TimeCallbackFactory(CallbackData, prefix="time"):
    appointment_id: int = None

class DeleteEditCallbackFactory(CallbackData, prefix="appoiment"):
    appointment_id: int
    action: str