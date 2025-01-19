from unittest.mock import patch
import pytest
from starlette import status

TEST_TICKET_ID = 1
TEST_SUBJECT = "Test Subject"
TEST_EMAIL = "test_user@example.com"
TEST_RESPONSE_TEXT = "This is a test response."


@pytest.mark.asyncio
async def test_reply_to_ticket(
        mock_send_email,
        mock_message_create,
        mock_ticket_get,
        async_client,
        dependency_override
) -> None:

    mock_ticket_get.return_value.id = TEST_TICKET_ID
    mock_ticket_get.return_value.subject = TEST_SUBJECT
    mock_ticket_get.return_value.email = TEST_EMAIL
    payload = {
        "ticket_id": TEST_TICKET_ID,
        "response_text": TEST_RESPONSE_TEXT,
    }

    response = await async_client.post('/api/reply', json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Response sent and saved successfully"}
    mock_send_email.assert_called_once_with(
        to_email=TEST_EMAIL,
        subject=f"Ответ на ваше обращение: {TEST_SUBJECT}",
        body=payload["response_text"]
    )
    mock_ticket_get.assert_called_once_with(
        dependency_override,
        TEST_TICKET_ID
    )
    mock_message_create.assert_called_once_with(
        session=dependency_override,
        subject=TEST_SUBJECT,
        content=TEST_RESPONSE_TEXT,
        ticket_id=TEST_TICKET_ID
    )
