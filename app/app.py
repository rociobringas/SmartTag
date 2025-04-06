from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
#import paho.mqtt.client as mqtt
from models.modelUser import ModelUser
from models.user import User
from database import db  # usamos el db de database.py

# Configuración inicial
app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Cambiala por una más segura en producción
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Facu2004@localhost/smarttag'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurar MQTT
#MQTT_BROKER = "tu-servidor-mqtt"
#MQTT_TOPIC_TRANQUERA = "campo/tranquera"

# Inicializaciones
csrf = CSRFProtect(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

#client = mqtt.Client()
#client.connect(MQTT_BROKER, 1883, 60)

# Cargar usuario en sesión
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas
@app.route("/")
def home():
    return redirect(url_for("register"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('gestion_vacas'))
        else:
            flash('Usuario o contraseña incorrectos.')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form.get('fullname', '')

        try:
            user = ModelUser.register(username, password, fullname)
            flash("Registro exitoso. Iniciá sesión.")
            return redirect(url_for('gestion_vacas'))
        except Exception as e:
            flash(str(e))
            return render_template('register.html')

    return render_template('register.html')

@app.route("/gestion_vacas")
@login_required
def gestion_vacas():
    return render_template("gestion_vacas.html")


#@app.route("/abrir_tranquera", methods=["GET", "POST"])
#def abrir_tranquera():
    #if request.method == "POST":
        #data = request.json
        #tranquera_id = data.get("tranquera")
        #client.publish(MQTT_TOPIC_TRANQUERA, tranquera_id)
        #return jsonify({"mensaje": f"Tranquera {tranquera_id} abierta correctamente"})
    #return render_template("abrir_tranquera.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
