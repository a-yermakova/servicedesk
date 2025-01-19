import imaplib
import email as email_lib
import time
from email.utils import parseaddr
import threading
from email.header import decode_header

from app.email.tasks import process_new_email_task


class EmailListener:
    """
    Класс для прослушивания новых писем с электронной почты.
    """
    def __init__(self, username, password, imap_server):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.stop_event = threading.Event()

    def listen(self):
        """
        Прослушивание новых писем.
        """
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.username, self.password)

        print(">>> Waiting for new emails...")

        try:
            while not self.stop_event.is_set():
                mail.select("INBOX")
                _, email_ids = mail.search(None, "UNSEEN")
                email_ids = email_ids[0].split()

                for email_id in email_ids:
                    _, email_data = mail.fetch(email_id, "(RFC822)")
                    raw_email = email_data[0][1]
                    msg = email_lib.message_from_bytes(raw_email)

                    message_id = msg.get("Message-ID")
                    from_email = parseaddr(msg.get("From"))[1]
                    coded_subject = msg.get("Subject")
                    subject = self.decode_subject(coded_subject)
                    content = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                content = part.get_payload(decode=True).decode("utf-8")
                    else:
                        content = msg.get_payload(decode=True).decode("utf-8")

                    process_new_email_task.delay(message_id, from_email, subject, content)

                time.sleep(30)
        except Exception as e:
            raise e
        finally:
            mail.logout()

    def stop(self):
        """
        Остановка прослушивания.
        """
        self.stop_event.set()

    @staticmethod
    def decode_subject(subject):
        decoded_parts = decode_header(subject)
        decoded_subject = ""
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                # Если часть закодирована, декодируем её
                decoded_subject += part.decode(encoding or "utf-8")
            else:
                # Если часть уже строка, добавляем её
                decoded_subject += part
        return decoded_subject
