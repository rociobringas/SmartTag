from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from routes.auth import auth_bp
from routes.vacas import vacas_bp
from routes.tranqueras import tranqueras_bp
from routes.sensores import sensores_bp

from config import Config
from database import db
from models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializaciones
    csrf = CSRFProtect(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(vacas_bp)
    app.register_blueprint(tranqueras_bp)
    app.register_blueprint(sensores_bp)



if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)

