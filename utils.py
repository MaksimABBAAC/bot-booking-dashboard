
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
        try:
            response = await client.get(settings.URL + settings.API_MASTERS)
            response.raise_for_status()
            return [Master(**master) for master in response.json()]
        
        except (httpx.HTTPError, ValueError, KeyError) as e:
            return None
