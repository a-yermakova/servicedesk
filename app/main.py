from fastapi import FastAPI
import asyncio

from app.api import tickets
from app.core.config import settings
from app.db import engine, Base
import threading

from app.email.listener import EmailListener

app = FastAPI()
app.include_router(tickets.router, prefix="/api", tags=["Tickets"])

listener = EmailListener(settings.EMAIL_USER, settings.EMAIL_PASSWORD, settings.EMAIL_HOST)
listener_thread = None


@app.on_event("startup")
async def start_listener():
    """
    Запускаем слушатель при старте приложения.
    """
    global listener_thread
    listener_thread = threading.Thread(target=listener.listen, daemon=True)
    listener_thread.start()
    print("Email Listener started.")


@app.on_event("shutdown")
async def stop_listener():
    """
    Останавливаем слушатель при завершении работы приложения.
    """
    listener.stop()
    listener_thread.join()
    print("Email Listener stopped.")


@app.get("/")
async def read_root():
    return {"message": "Start page"}


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
