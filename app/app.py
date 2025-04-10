from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from datetime import datetime

from config import Config
from database import db
from models.user import User
from models.modelUser import ModelUser
from models.animal import Animal
from models.weightHistory import WeightHistory


app = Flask(__name__)
app.config.from_object(Config)

# Inicializaciones
csrf = CSRFProtect(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas principales
@app.route("/")
def home():
    return redirect(url_for("register"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = ModelUser.login(username, password)
        if user:
            login_user(user)
            return redirect(url_for('registrar_vaca'))
        else:
            flash('Usuario o contraseña incorrectos.')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if not username or not password:
            flash("Usuario y contraseña son obligatorios.")
            return redirect(url_for('register'))
        try:
            user = ModelUser.register(username, password)
            flash("Registro exitoso. Iniciá sesión.")
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.')
    return redirect(url_for('login'))

@app.route('/registrar_vaca', methods=['GET', 'POST'])
@login_required
def registrar_vaca():
    
    if request.method == 'POST':
        breed = request.form['breed']
        gender = request.form['gender']
        father = request.form['father']
        birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
        fertile = 'fertile' in request.form

        # Crea el animal
        new_animal = Animal(
            IDUser=current_user.id,
            breed=breed,
            gender=gender,
            father=father,
            birth=birth_date,
            fertile=fertile
        )

        db.session.add(new_animal)
        db.session.commit()

        flash('¡Vaca registrada con éxito!')
        return redirect(url_for('registrar_peso', id_animal= new_animal.IDAnimal))
    return render_template('registrar_vaca.html')


@app.route('/registrar_peso/<int:id_animal>', methods=['GET', 'POST'])
@login_required
def registrar_peso(id_animal):
    if request.method == 'POST':
        peso = float(request.form['peso'])
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()

        # Por ahora, ponemos 0 como IDRegistration (si no usás tabla Registration aún)
        registro = WeightHistory(
            IDAnimal=id_animal,
            IDRegistration=0,
            value=peso,
            date=fecha
        )

        db.session.add(registro)
        db.session.commit()
        flash('Peso registrado correctamente.')
        return redirect(url_for('gestion_vacas'))

    return render_template('registrar_peso.html', id_animal=id_animal)


@app.route('/gestion_vacas')
@login_required
def gestion_vacas():
    males = Male.query.all()
    females = Female.query.all()
    return render_template('gestion_vacas.html', males=males, females=females)

if __name__ == "__main__":
    app.run(debug=True)