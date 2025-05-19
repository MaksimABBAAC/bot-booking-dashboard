from typing import Optional
from pydantic import BaseModel
import httpx
from datetime import date, time
from config import settings


class Master(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    description: str
    specialty: str

async def get_masters_list() -> list[Master]:
    async with httpx.AsyncClient() as client:
        try:
            url = settings.BASE_URL + settings.API_MASTERS
            response = await client.get(settings.BASE_URL + settings.API_MASTERS)
            response.raise_for_status()
            return [Master(**master) for master in response.json()]
        
        except (httpx.HTTPError, ValueError, KeyError) as e:
            return None

async def get_master_by_id(master_id) -> Master:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(settings.BASE_URL + settings.API_MASTERS + f'?master_id={master_id}')
            response.raise_for_status()
            masters = response.json()
            master_dict = {m['id']: m for m in masters}
            return Master(**master_dict[master_id])
        
        except (httpx.HTTPError, ValueError, KeyError) as e:
            return None


class Availabl_appointment(BaseModel):
    id: int
    master: int
    client: Optional[int] = None
    date: date
    start_time: time
    end_time: time
    is_available: bool

async def get_available_appointment_all_masters(date = None) -> list[Availabl_appointment]:
    async with httpx.AsyncClient() as client:
        try:
            url  = settings.BASE_URL + settings.API_APPOINTMENTS
            if date != None:
                f'?date={date}'
            response = await client.get(url)
            response.raise_for_status()
            return [Availabl_appointment(**appointment) 
                    for appointment in response.json()]
        except (httpx.HTTPError, ValueError, KeyError) as e:
            return None

async def get_available_appointment_by_master_id(master_id = None, date = None) -> list[Availabl_appointment]:
    async with httpx.AsyncClient() as client:
        try:
            url = settings.BASE_URL + settings.API_APPOINTMENTS
            if master_id and date:
                url += f'?master_id={master_id}&date={date}'
            elif master_id != None:
                url += f'?master_id={master_id}'
            elif date != None:
                f'?date={date}'
            response = await client.get(url)
            response.raise_for_status()
            return [Availabl_appointment(**appointment) for appointment in response.json()]
        except (httpx.HTTPError, ValueError, KeyError) as e:
            return None


async def book_appointment(tg_id: int, appointment_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            url = f"{settings.BASE_URL}API/book/"
            
            data = {
                "appointment_id": appointment_id,
                "tg_id": int(tg_id)
            }
            
            response = await client.post(url, data=data, timeout=100.0)
            
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPStatusError as e:
            error_message = f"Ошибка сервера: {e.response.status_code}"
            if e.response.text:
                error_message += f" - {e.response.text}"
            return {"error": error_message}
            
        except httpx.RequestError as e:
            return {"error": f"Ошибка подключения: {str(e)}"}
            
        except Exception as e:
            return {"error": f"Неизвестная ошибка: {str(e)}"}