from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.routes.auth import auth_bp
from app.routes.vacas import vacas_bp
from app.routes.tranqueras import tranqueras_bp
from app.routes.sensores import sensores_bp

from app.config import Config
from app.database import db
from app.models.user import User
from app.mqtt_listener import start_mqtt_listener


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializaciones
    csrf = CSRFProtect()
    csrf.init_app(app)
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
    app.register_blueprint(tranqueras_bp, url_prefix="/tranqueras")
    app.register_blueprint(sensores_bp)

    # Iniciar el listener MQTT
    start_mqtt_listener()

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)

