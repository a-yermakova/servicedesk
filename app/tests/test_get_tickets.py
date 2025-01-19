import pytest
from starlette import status

first_fake_ticket = {
    "id": 1,
    "email": "test1@example.com",
    "subject": "Subject 1",
    "status": "open",
    "created_at": "2025-01-01T00:00:00",
    "operator_id": 1
}

second_fake_ticket = {
    "id": 2,
    "email": "test2@example.com",
    "subject": "Subject 2",
    "status": "closed",
    "created_at": "2025-01-02T00:00:00",
    "operator_id": 2
}


@pytest.mark.asyncio
async def test_get_tickets(
        async_client,
        dependency_override,
        mock_ticket_get_tickets
):
    mock_ticket_get_tickets.return_value = [
        first_fake_ticket,
        second_fake_ticket
    ]

    response = await async_client.get('/api/tickets', params={"status": "open", "sort": "asc"})

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        first_fake_ticket,
        second_fake_ticket
    ]

    mock_ticket_get_tickets.assert_called_once_with(
        session=dependency_override,
        status="open",
        sort="asc"
    )
