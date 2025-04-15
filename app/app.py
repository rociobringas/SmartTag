from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from datetime import datetime

from config import Config
from database import db
from models.animal import Animal
from models.user import User
from models.modelUser import ModelUser
from models.registration import Registration
from models.vaccineHistory import VaccineHistory
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
        birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
        fertile = 'fertile' in request.form

        # Crea el animal
        new_animal = Animal(
            IDUser=current_user.id,
            breed=breed,
            gender=gender,
            birth=birth_date,
            fertile=fertile
        )

        db.session.add(new_animal)
        db.session.commit()

        flash('¡Vaca registrada con éxito!')
        return redirect(url_for('registrar_evento', id_animal= new_animal.IDAnimal))
    return render_template('registrar_vaca.html')


@app.route('/registrar_evento/<int:id_animal>', methods=['GET'])
@login_required
def registrar_evento(id_animal):
    vaca = Animal.query.get_or_404(id_animal)
    return render_template('registrar_evento.html', vaca=vaca)


@app.route('/registrar_peso/<int:id_animal>', methods=['GET', 'POST'])
@login_required
def registrar_peso(id_animal):
    if request.method == 'POST':
        #Si aprieto cancelar
        if request.form['action'] == 'cancelar':
            return redirect(url_for('registrar_evento', id_animal = id_animal))
        
        #Si aprieto guardar
        peso = float(request.form['peso'])
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        
        # Crear el registro de peso
        nuevo_peso = WeightHistory(IDAnimal=id_animal, value=peso, date=fecha)
        db.session.add(nuevo_peso)
        db.session.commit()

        # Registrar el evento en la tabla Registration
        registro = Registration(
            IDUser=current_user.id,
            IDAnimal=id_animal,
            EventType='weight',
            reference_id=nuevo_peso.IDWeight,
            date=fecha
        )
        db.session.add(registro)
        db.session.commit()

        flash('Peso registrado correctamente!')
        return redirect(url_for('ver_eventos', id_animal=id_animal))
    
    return render_template('registrar_peso.html', id_animal=id_animal)

@app.route('/registrar_vacuna/<int:id_animal>', methods=['GET', 'POST'])
@login_required
def registrar_vacuna(id_animal):
    if request.method == 'POST':
        #Si aprieto cancelar
        if request.form['action'] == 'cancelar':
            return redirect(url_for('registrar_evento', id_animal = id_animal))

        #Si aprieto guardar
        vacuna = request.form['vacuna']
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()

        # Crear el registro de vacuna
        nueva_vacuna = VaccineHistory(IDAnimal=id_animal, vaccineType=vacuna, date=fecha)
        db.session.add(nueva_vacuna)
        db.session.commit()

        # Registrar el evento en la tabla Registration
        registro = Registration(
            IDUser=current_user.id,
            IDAnimal=id_animal,
            EventType='vaccine',
            reference_id=nueva_vacuna.IDVaccine,
            date=fecha
        )
        db.session.add(registro)
        db.session.commit()

        flash('Vacuna registrada correctamente!')
        return redirect(url_for('ver_eventos', id_animal=id_animal))
    
    return render_template('registrar_vacuna.html', id_animal=id_animal)

@app.route('/ver_eventos/<int:id_animal>')
@login_required
def ver_eventos(id_animal):
    # Obtener todos los registros de eventos para el animal
    registros = Registration.query.filter_by(IDAnimal=id_animal).order_by(Registration.date.desc()).all()

    # Construir la lista de eventos para la vista
    eventos = []
    for reg in registros:
        if reg.EventType == 'weight':
            peso = WeightHistory.query.get(reg.reference_id)
            eventos.append({'tipo': 'Peso', 'fecha': reg.date, 'detalle': f'{peso.value} kg'})
        elif reg.EventType == 'vaccine':
            vacuna = VaccineHistory.query.get(reg.reference_id)
            eventos.append({'tipo': 'Vacuna', 'fecha': reg.date, 'detalle': vacuna.vaccineType})
    
    return render_template('ver_eventos.html', eventos=eventos)




if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)

@app.route('/check-db')
def check_db():
    try:
        db.session.execute("SELECT 1")
        return "Conexión a base de datos exitosa ✅"
    except Exception as e:
        return f"Error de conexión ❌: {e}"
