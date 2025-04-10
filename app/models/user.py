from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import db  # Asegurate que este archivo tenga SQLAlchemy() definido

class User(db.Model, UserMixin):
    __tablename__ = 'User'  # Nombre exacto de la tabla en MySQL

    IDUser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)  # Hashea al guardar

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def id(self):
        return self.IDUser
        
    def get_id(self):
        return str(self.IDUser)  # Flask-Login necesita esto si el ID no se llama literalmente "id"

