from models.user import User
from database import db

class ModelUser:

    @classmethod
    def login(cls, username, password):
        try:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                return user
            return None
        except Exception as ex:
            raise Exception(f"Error en login: {str(ex)}")

    @classmethod
    def get_by_id(cls, user_id):
        try:
            return User.query.get(user_id)
        except Exception as ex:
            raise Exception(f"Error al obtener usuario por ID: {str(ex)}")

    @classmethod
    def register(cls, username, password):
        try:
            if User.query.filter_by(username=username).first():
                raise Exception("El usuario ya existe")
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as ex:
            raise Exception(f"Error al registrar usuario: {str(ex)}")
