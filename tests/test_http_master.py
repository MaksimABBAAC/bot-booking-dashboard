import pytest

from bot.config import settings
from bot.utils.http_master import get_master_by_id, get_masters_list
from bot.utils.model import Master


@pytest.mark.asyncio
async def test_get_masters_list_success(httpx_mock):
    mock_masters = [
        {
            "id": 1,
            "name": "Master One",
            "surname": "Surname One",
            "patronymic": "Patronymic One",
            "description": "Description One",
            "specialty": "Specialty One",
        },
        {
            "id": 2,
            "name": "Master Two",
            "surname": "Surname Two",
            "patronymic": "Patronymic Two",
            "description": "Description Two",
            "specialty": "Specialty Two",
        },
    ]
    url = settings.BASE_URL + settings.API_MASTERS

    httpx_mock.add_response(
        method="GET",
        url=url,
        json=mock_masters,
        status_code=200,
    )

    result = await get_masters_list()

    assert isinstance(result, list)
    assert all(isinstance(m, Master) for m in result)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "Master One"
    assert result[0].surname == "Surname One"
    assert result[0].patronymic == "Patronymic One"
    assert result[0].description == "Description One"
    assert result[0].specialty == "Specialty One"


@pytest.mark.asyncio
async def test_get_masters_list_failure(httpx_mock):
    url = settings.BASE_URL + settings.API_MASTERS

    httpx_mock.add_response(
        method="GET",
        url=url,
        status_code=500,
    )

    result = await get_masters_list()
    assert result is None


@pytest.mark.asyncio
async def test_get_master_by_id_success(httpx_mock):
    master_id = 1
    mock_response = [
        {
            "id": 1,
            "name": "Master One",
            "surname": "Surname One",
            "patronymic": "Patronymic One",
            "description": "Description One",
            "specialty": "Specialty One",
        },
        {
            "id": 2,
            "name": "Master Two",
            "surname": "Surname Two",
            "patronymic": "Patronymic Two",
            "description": "Description Two",
            "specialty": "Specialty Two",
        },
    ]

    url = f"{settings.BASE_URL + settings.API_MASTERS}?master_id={master_id}"

    httpx_mock.add_response(
        method="GET",
        url=url,
        json=mock_response,
        status_code=200,
    )

    result = await get_master_by_id(master_id)

    assert isinstance(result, Master)
    assert result.id == master_id
    assert result.name == "Master One"
    assert result.surname == "Surname One"
    assert result.patronymic == "Patronymic One"
    assert result.description == "Description One"
    assert result.specialty == "Specialty One"


@pytest.mark.asyncio
async def test_get_master_by_id_not_found(httpx_mock):
    master_id = 3
    mock_response = [
        {
            "id": 1,
            "name": "Master One",
            "surname": "Surname One",
            "patronymic": "Patronymic One",
            "description": "Description One",
            "specialty": "Specialty One",
        },
        {
            "id": 2,
            "name": "Master Two",
            "surname": "Surname Two",
            "patronymic": "Patronymic Two",
            "description": "Description Two",
            "specialty": "Specialty Two",
        },
    ]
    url = f"{settings.BASE_URL + settings.API_MASTERS}?master_id={master_id}"

    httpx_mock.add_response(
        method="GET",
        url=url,
        json=mock_response,
        status_code=200,
    )

    result = await get_master_by_id(master_id)
    assert result is None


@pytest.mark.asyncio
async def test_get_master_by_id_http_error(httpx_mock):
    master_id = 1
    url = f"{settings.BASE_URL + settings.API_MASTERS}?master_id={master_id}"

    httpx_mock.add_response(
        method="GET",
        url=url,
        status_code=404,
    )

    result = await get_master_by_id(master_id)
    assert result is None
