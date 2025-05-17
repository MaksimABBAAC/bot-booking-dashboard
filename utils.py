
from pydantic import BaseModel
import httpx

from config import settings

class Master(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    description: str
    specialty: int

async def get_Masters() -> list[Master]:
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.URL + settings.API_MASTERS)
        data = response.json()
        print(type(data))
        masters = [Master(**master) for master in data]
        return masters





