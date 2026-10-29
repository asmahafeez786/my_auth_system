from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    token_version = db.Column(db.Integer, default=0)

    otp = db.Column(db.String(200), nullable=True)

    otp_expiry = db.Column(db.DateTime, nullable=True)