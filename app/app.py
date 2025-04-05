from flask import Flask, render_template, request, jsonify, redirect, url_for, flash 
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_mysqldb import MySQL
#import paho.mqtt.client as mqtt

# Models:
from models.modelUser import ModelUser
from models.user import User

app = Flask(__name__)
csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

# Configurar MQTT
#MQTT_BROKER = "tu-servidor-mqtt"
#MQTT_TOPIC_TRANQUERA = "campo/tranquera"

#client = mqtt.Client()
#client.connect(MQTT_BROKER, 1883, 60)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route("/gestion_vacas")
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

if __name__ == "__main__":
    app.run(debug=True)
