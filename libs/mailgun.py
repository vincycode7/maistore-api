from requests import Response, post, request
from flask import request, url_for, make_response, render_template
from typing import List


class Mailgun:
    MAILGUN_DOMAIN = "sandbox2c9ff2575f0c4dd6970b519cd7c74e67.mailgun.org"
    MAILGUN_API_KEY = "a0297bae74a587331b44484d0b59249b-aff2d1b9-fbf753c5"
    FROM_TITLE = "MAISTORE"
    FROM_EMAIL = "postmaster@sandbox2c9ff2575f0c4dd6970b519cd7c74e67.mailgun.org"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str = None, html: str = None
    ) -> Response:
        return post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <mailgun@{cls.MAILGUN_DOMAIN}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
