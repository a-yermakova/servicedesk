from fastapi import APIRouter, Query, Depends, HTTPException, Body
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app import db
from app.email import handlers
from app.models import Ticket, Message
from app.schemas.reply import ReplyRequest
from app.schemas.ticket import TicketResponse

router = APIRouter()


@router.get("/tickets", response_model=List[TicketResponse])
async def get_tickets(
        status: Optional[str] = Query(None, description="Фильтрация по статусу"),
        sort: Optional[str] = Query("asc", description="Сортировка: 'asc' или 'desc'"),
        session: AsyncSession = Depends(db.get_session)
):
    """
    Получение списка обращений с фильтрацией по статусу и сортировкой по времени создания.
    """
    tickets = await Ticket.get_tickets(session=session, status=status, sort=sort)
    return tickets


@router.post("/tickets/{ticket_id}/assign", response_model=TicketResponse)
async def assign_ticket_to_operator(
        ticket_id: int,
        operator_id: int,
        session: AsyncSession = Depends(db.get_session),
):
    """
    Назначить оператору обращение.
    """
    try:
        ticket = await Ticket.assign_to_operator(session=session, ticket_id=ticket_id, operator_id=operator_id)
        return ticket
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Ticket with id {ticket_id} not found")


@router.put("/tickets/{ticket_id}/close", response_model=TicketResponse)
async def close_ticket(
        ticket_id: int,
        session: AsyncSession = Depends(db.get_session),
):
    """
    Закрыть обращение.
    """
    try:
        ticket = await Ticket.close_ticket(session=session, ticket_id=ticket_id)

        # Отправить уведомление о закрытии обращения на email
        handlers.send_email(
            to_email=ticket.email,
            email_type="closure_notification"
        )
        return ticket
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Ticket with id {ticket_id} not found")


@router.post("/reply")
async def reply_to_ticket(
        request: ReplyRequest = Body(),
        session: AsyncSession = Depends(db.get_session)
):
    """
    Ответить на тикет через API и отправить ответ на email пользователя.
    """
    ticket = await Ticket.get(session, request.ticket_id)
    if not ticket:
        raise HTTPException(status_code=402, detail="Ticket not found")

    await Message.create(
        session=session,
        subject=ticket.subject,
        content=request.response_text,
        ticket_id=ticket.id
    )

    try:
        handlers.send_email(
            to_email=ticket.email,
            subject=f"Ответ на ваше обращение: {ticket.subject}",
            body=request.response_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    return {"message": "Response sent and saved successfully"}
