from requests import Response, post, request
from mailer import Mailer, Message
import os

FAILED_LOAD_USR = "username not found"
FAILED_LOAD_PWD = "password not found"
ERR_SENDING_EMAIL = "Error in sending confirmation email. (check mailer credentials or network connection)"

class MailerException(Exception):
    def __init__(self, message:str):
        super().__init__(message)

class Sender:
    MAILER_USR = os.environ.get("MAILER_USR")
    MAILER_PWD = os.environ.get("MAILER_PWD")

    @classmethod
    def send_email(cls, to, subject, html, text=None) -> Response:
        sender = cls.acquire_sender()
        msg = Message(
            From=cls.MAILER_USR,
            To=to,
            charset="utf-8",
        )

        msg.Subject = subject
        msg.Html = html
        msg.Body = text
        try:
            sender.send(msg)
        except:
            raise MailerException(ERR_SENDING_EMAIL)
        return

    @classmethod
    def acquire_sender(
        cls,
        host="smtp.zoho.com",
        port=587,
        use_tls=True,
        use_ssl=False,
        use_plain_auth=False,
    ):
        if cls.MAILER_USR is None:
            raise MailerException(FAILED_LOAD_USR)
        if cls.MAILER_PWD is None:
            raise MailerException(FAILED_LOAD_PWD)
        
        try:
            sender = Mailer(
                host=host,
                port=port,
                use_tls=use_tls,
                use_ssl=use_ssl,
                use_plain_auth=use_plain_auth,
            )
            sender.login(usr=cls.MAILER_USR, pwd=cls.MAILER_PWD)
            return sender
        except Exception as e:
            raise e
