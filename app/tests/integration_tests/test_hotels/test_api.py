from httpx import AsyncClient
import pytest


# Тест получение отеля по месту и датам проживания
@pytest.mark.parametrize("location, date_from, date_to, status_code", [
    ("Алтай", "2023-10-01", "2023-10-15", 200),
    ("Алтай", "2023-10-15", "2023-10-01", 400),
    ("Алтай", "2023-10-01", "2023-11-10", 400)
])
async def test_get_hotels_location_dates(
        location,
        date_from,
        date_to,
        status_code,
        ac: AsyncClient
):
    response = await ac.get("hotels/location", params={
        "location": location,
        "date_from": date_from,
        "date_to": date_to 
    })

    assert response.status_code == status_code