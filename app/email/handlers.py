import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from app.core.config import settings


def send_email(
        to_email: str,
        message_id: int = None,
        subject: str = None,
        body: str = None,
        email_type: str = None):
    """
    Отправить email пользователю.

    :param to_email: Email получателя
    :param message_id: ID сообщения
    :param subject: Тема сообщения
    :param body: Текст сообщения
    :param email_type: Тип сообщения ('auto_reply', 'operator_message', 'closure_notification')
    """
    if email_type == "auto_reply":
        subject = f"Автоответ: {subject}"
        body = f"Ваше обращение получено и находится в обработке. Мы свяжемся с вами в ближайшее время."
    elif email_type == "closure_notification":
        subject = f"Обращение закрыто: {subject}"
        body = f"Здравствуйте!\n\nВаше обращение закрыто. Спасибо, что обратились к нам.\n\n"
    elif email_type == "operator_message":
        body = f"Сообщение от оператора:\n\n{body}"

    message = MIMEMultipart()
    message["From"] = formataddr(("Служба поддержки", settings.EMAIL_USER))
    message["To"] = to_email
    message["Subject"] = subject

    if message_id:
        # Добавляем заголовки для ответа
        message["In-Reply-To"] = message_id
        message["References"] = message_id

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_USER, [to_email], message.as_string())
