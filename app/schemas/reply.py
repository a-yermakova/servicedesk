from pydantic import BaseModel


class ReplyRequest(BaseModel):
    ticket_id: int
    response_text: str