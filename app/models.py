from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
