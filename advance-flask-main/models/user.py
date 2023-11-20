from flask import request, url_for
from requests import Response

from libs.mailgun import Mailgun
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, username: str):
        """Method to find a record from users database based on username"""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_userid(cls, userid: int):
        """Method to find a record from users database based on userid"""
        return cls.query.filter_by(userid=userid).first()

    @classmethod
    def find_by_email(cls, email: str):
        """Method to find a record from users database based on email id"""
        return cls.query.filter_by(email=email).first()

    def send_confirmation_email(self) -> Response:
        subject = "Registration Confirmation"
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        return Mailgun.send_email([self.email], subject, html)

    def save_to_db(self) -> None:
        """Save the data to users table"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete the data from users table"""
        db.session.delete(self)
        db.session.commit()
