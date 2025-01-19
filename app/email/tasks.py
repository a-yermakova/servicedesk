from app.celery_app import celery_app
from app.db import get_session_context_manager
from app.email.handlers import send_email
from app.models import Ticket, Message
import asyncio


@celery_app.task
def process_new_email_task(message_id, from_email, subject, content):
    """
    Подготавливает задачу для обработки нового письма.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_new_email_async(message_id, from_email, subject, content))


async def process_new_email_async(message_id, from_email, subject, content):
    """
    Обрабатывает новое письмо.
    """
    async with get_session_context_manager() as session:
        ticket = await Ticket.get_or_create(session, from_email, subject)

        await Message.create(session, subject, content, ticket.id)

    send_email(to_email=from_email, subject=subject, message_id=message_id, email_type="auto_reply")
