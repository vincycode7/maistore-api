from requests import Response, post, request
from mailer import Mailer, Message
from libs.strings import gettext
import os


class MailerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Sender:
    MAILER_USR = os.environ.get("MAILER_USR", None)
    MAILER_PWD = os.environ.get("MAILER_PWD", None)

    @classmethod
    def send_email(cls, to, subject, html, text=None, from_=None) -> Response:
        sender = cls.acquire_sender()
        from_ = from_ if from_ else cls.MAILER_USR
        msg = Message(
            From=from_,
            To=to,
            charset="utf-8",
        )

        msg.Subject = subject
        msg.Html = html
        msg.Body = text
        try:
            sender.send(msg)
        except Exception as e:
            raise MailerException(gettext("mailer_failed_to_send").format(e))
        return gettext("mailer_sent_mail_success"), 200

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
            raise MailerException(gettext("mailer_failed_to_load_username"))
        if cls.MAILER_PWD is None:
            raise MailerException(gettext("mailer_failed_to_load_password"))

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
        except:
            raise MailerException(gettext("mailer_failed_to_logging"))
