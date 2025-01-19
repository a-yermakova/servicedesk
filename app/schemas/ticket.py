from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TicketResponse(BaseModel):
    id: int
    email: str
    status: str
    subject: str
    created_at: datetime
    operator_id: Optional[int]

    class Config:
        orm_mode = True
