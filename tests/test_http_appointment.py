import pytest
from bot.utils.http_appointment import book_appointment, delete_book_appointment, get_available_appointment_all_masters, get_available_appointment_by_master_id, get_booking_appointment_by_tg_id
from datetime import date


@pytest.mark.asyncio
async def test_get_available_appointment_all_masters(httpx_mock):
    mock_response = [
        {
            "id": 1,
            "master": 1,
            "client": None,
            "date": "2023-10-01",
            "start_time": "10:00",
            "end_time": "11:00",
            "is_available": True,
        }
    ]
    httpx_mock.add_response(
        url="http://127.0.0.1:8000/API/available/",
        json=mock_response,
    )

    result = await get_available_appointment_all_masters()
    print("Реальный результат тест test_get_available_appointment_all_masters: ", result)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].master == 1
    assert result[0].is_available is True


@pytest.mark.asyncio
async def test_get_available_appointment_by_master_id(httpx_mock):
    mock_response = [
        {
            "id": 2,
            "master": 2,
            "client": None,
            "date": "2023-10-02",
            "start_time": "12:00",
            "end_time": "13:00",
            "is_available": True,
        }
    ]
    httpx_mock.add_response(
        url="http://127.0.0.1:8000/API/available/?master_id=2",
        json=mock_response,
    )

    result = await get_available_appointment_by_master_id(master_id=2)
    print("Реальный результат тест get_available_appointment_by_master_id: ", result)
    assert result[0].master == 2
    assert result[0].date == date(2023, 10, 2)


@pytest.mark.asyncio
async def test_get_booking_appointment_by_tg_id(httpx_mock):
    mock_response = [
        {
            "id": 3,
            "master": 1,
            "client": 123,  # Здесь client — это tg_id
            "date": "2023-10-03",
            "start_time": "14:00",
            "end_time": "15:00",
            "is_available": False,  # Запись уже занята
        }
    ]
    httpx_mock.add_response(
        url="http://127.0.0.1:8000/API/booking/?tg_id=123",
        json=mock_response,
    )

    result = await get_booking_appointment_by_tg_id(tg_id=123)
    print("Реальный результат тест get_booking_appointment_by_tg_id: ", result)
    assert result[0].client == 123
    assert result[0].is_available is False


@pytest.mark.asyncio
async def test_book_appointment_success(httpx_mock):
    mock_response = {
        "status": "success",
        "appointment_id": 1,
        "master": 1,
        "client": 123,
        "date": "2023-10-01",
        "start_time": "10:00",
        "end_time": "11:00",
    }
    httpx_mock.add_response(
        url="http://127.0.0.1:8000/API/book/",
        method="POST",
        json=mock_response,
    )

    result = await book_appointment(tg_id=123, appointment_id=1)
    print("Реальный результат:", result)
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_delete_book_appointment(httpx_mock):
    mock_response = {
        "status": "deleted",
        "appointment_id": 1,
        "client": 123,
    }
    httpx_mock.add_response(
        url="http://127.0.0.1:8000/API/appointment/delete",
        method="POST",
        json=mock_response,
    )

    result = await delete_book_appointment(tg_id=123, appointment_id=1)
    print("Реальный результат:", result)
    assert result["status"] == "deleted"


@pytest.mark.asyncio
async def test_invalid_api_response(httpx_mock):
    mock_response = [
        {
            "id": 1,
            "client": None,
            "date": "2023-10-01",
            "start_time": "10:00",
            "end_time": "11:00",
            "is_available": True,
        }
    ]
    httpx_mock.add_response(
        url="http://127.0.0.1:8000/API/available/",
        json=mock_response,
    )

    result = await get_available_appointment_all_masters()
    assert result is None