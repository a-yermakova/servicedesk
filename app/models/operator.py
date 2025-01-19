from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    tickets = relationship("Ticket", back_populates="operator", cascade="all, delete-orphan")