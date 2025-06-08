from httpx import AsyncClient, HTTPError

from ..config import settings
from .model import Master


async def get_masters_list() -> list[Master]:
    async with AsyncClient() as client:
        try:
            response = await client.get(settings.BASE_URL + settings.API_MASTERS)
            response.raise_for_status()
            return [Master(**master) for master in response.json()]

        except (HTTPError, ValueError, KeyError):
            return None


async def get_master_by_id(master_id) -> Master:
    async with AsyncClient() as client:
        try:
            response = await client.get(
                settings.BASE_URL + settings.API_MASTERS + f"?master_id={master_id}"
            )
            response.raise_for_status()
            masters = response.json()
            master_dict = {m["id"]: m for m in masters}
            return Master(**master_dict[master_id])

        except (HTTPError, ValueError, KeyError):
            return None
