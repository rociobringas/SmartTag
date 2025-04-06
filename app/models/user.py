from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import db  # Asegurate de tener SQLAlchemy() en database.py

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    fullname = db.Column(db.String(200), nullable=True)

    def __init__(self, username, password, fullname=""):
        self.username = username
        self.password = generate_password_hash(password)  # Hash automático
        self.fullname = fullname

    def check_password(self, password):
        return check_password_hash(self.password, password)
