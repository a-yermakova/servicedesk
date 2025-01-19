from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List, Optional
from sqlalchemy.orm.exc import NoResultFound



class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    status = Column(String, default="open", nullable=False)
    subject = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)

    operator = relationship("Operator", back_populates="tickets")
    messages = relationship("Message", back_populates="ticket", cascade="all, delete")

    @classmethod
    async def get(cls, session: AsyncSession, ticket_id: int):
        """
        Получает тикет по ID.
        """
        query = select(cls).where(cls.id == ticket_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_or_create(cls, session: AsyncSession, from_email: str, subject: str):
        """
        Возвращает существующий тикет или создаёт новый.
        """
        query = select(cls).filter(
            cls.email == from_email,
            cls.status != "closed",
        )
        result = await session.execute(query)
        ticket = result.scalars().first()

        if ticket:
            return ticket

        ticket = cls(
            email=from_email,
            status="open",
            subject=subject
        )

        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)
        return ticket

    @classmethod
    async def get_tickets(
            cls,
            session: AsyncSession,
            status: Optional[str] = None,
            sort: str = "asc"
    ):
        """
        Получает список обращений с фильтрацией по статусу и сортировкой.
        """
        query = select(cls).options(joinedload(cls.operator))

        if status:
            query = query.where(cls.status == status)

        if sort == "desc":
            query = query.order_by(cls.created_at.desc())
        else:
            query = query.order_by(cls.created_at.asc())

        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def assign_to_operator(cls, session: AsyncSession, ticket_id: int, operator_id: int):
        """
        Назначает тикет оператору.
        """
        query = select(cls).where(cls.id == ticket_id)
        result = await session.execute(query)
        ticket = result.scalar_one_or_none()

        if not ticket:
            raise NoResultFound(f"Ticket with id {ticket_id} not found")

        ticket.operator_id = operator_id
        await session.commit()
        return ticket

    @classmethod
    async def close_ticket(cls, session: AsyncSession, ticket_id: int):
        """
        Закрывает обращение.
        """
        query = select(cls).where(cls.id == ticket_id)
        result = await session.execute(query)
        ticket = result.scalar_one_or_none()

        if not ticket:
            raise NoResultFound(f"Ticket with id {ticket_id} not found")

        ticket.status = "closed"
        await session.commit()
        return ticket
