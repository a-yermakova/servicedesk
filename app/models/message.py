from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from app.db import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)

    ticket = relationship("Ticket", back_populates="messages")

    @classmethod
    async def create(cls, session: AsyncSession, subject: str, content: str, ticket_id: int):
        """
        Создаёт новое сообщение, связанное с тикетом.
        """
        message = cls(ticket_id=ticket_id, subject=subject, content=content)
        session.add(message)
        await session.commit()
        return message
