from httpx import AsyncClient, HTTPError, HTTPStatusError, RequestError

from config import settings
from utils.model import Availabl_appointment


async def get_available_appointment_all_masters(date = None) -> list[Availabl_appointment]:
    async with AsyncClient() as client:
        try:
            url  = settings.BASE_URL + settings.API_APPOINTMENTS
            if date != None:
                f'?date={date}'
            response = await client.get(url)
            response.raise_for_status()
            return [Availabl_appointment(**appointment) 
                    for appointment in response.json()]
        except (HTTPError, ValueError, KeyError):
            return None

async def get_available_appointment_by_master_id(master_id = None, date = None) -> list[Availabl_appointment]:
    async with AsyncClient() as client:
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
        except (HTTPError, ValueError, KeyError):
            return None

async def get_booking_appointment_by_tg_id(tg_id: int) -> list[Availabl_appointment]:
    async with AsyncClient() as client:
        try:
            url = settings.BASE_URL + settings.API_BOOKING + f'?tg_id={tg_id}'
            response = await client.get(url)
            response.raise_for_status()
            return [Availabl_appointment(**appointment) for appointment in response.json()]
        except (HTTPError, ValueError, KeyError):
            return 'error'


async def book_appointment(tg_id: int, appointment_id: int) -> dict:
    async with AsyncClient() as client:
        try:
            url = settings.BASE_URL + settings.API_BOOK
            
            data = {
                "appointment_id": appointment_id,
                "tg_id": int(tg_id)
            }
            
            response = await client.post(url, data=data, timeout=100.0)
            
            response.raise_for_status()
            
            return response.json()
            
        except HTTPStatusError as e:
            error_message = f"Ошибка сервера: {e.response.status_code}"
            if e.response.text:
                error_message += f" - {e.response.text}"
            return {"error": error_message}
            
        except RequestError as e:
            return {"error": f"Ошибка подключения: {str(e)}"}
            
        except Exception as e:
            return {"error": f"Неизвестная ошибка: {str(e)}"}

async def delete_book_appointment(tg_id: int, appointment_id: int) -> dict:
    async with AsyncClient() as client:
        try:
            url = settings.BASE_URL + settings.API_DELETE_BOOK

            data = {
                'appointment_id': appointment_id,
                "tg_id": tg_id
            }

            response = await client.post(url, data=data, timeout=100.0)

            response.raise_for_status()

            return response.json()
        
        except HTTPStatusError as e:
            error_message = f"Ошибка сервера: {e.response.status_code}"
            if e.response.text:
                error_message += f" - {e.response.text}"
            return {"error": error_message}
            
        except RequestError as e:
            return {"error": f"Ошибка подключения: {str(e)}"}
            
        except Exception as e:
            return {"error": f"Неизвестная ошибка: {str(e)}"}