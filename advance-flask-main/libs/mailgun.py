from requests import Response, post
from os import getenv


class Mailgun:
    FROM_USER = getenv("FROM_USER")
    FROM_EMAIL = f'o-not-reply@{getenv("FROM_EMAIL")}'
    YOUR_DOMAIN_NAME = getenv("YOUR_DOMAIN_NAME")
    YOUR_API_KEY = getenv("YOUR_API_KEY")

    @classmethod
    def send_email(cls, email, subject, html) -> Response:
        return post(
                f"https://api.mailgun.net/v3/{cls.YOUR_DOMAIN_NAME}/messages",
                auth=("api", cls.YOUR_API_KEY),
                data={"from": f"{cls.FROM_USER} {cls.FROM_EMAIL}",
                      "to": email,
                      "subject": subject,
                      "html": html,
                      }
        )
