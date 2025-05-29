from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.models.animal import Animal
from app.models.registration import Registration
from app.models.vaccineHistory import VaccineHistory
from app.models.weightHistory import WeightHistory
from app.database import db
from app.mqtt_client import publish, MQTT_TOPIC_TRANQUERA


vacas_bp = Blueprint('vacas', __name__)

@vacas_bp.route('/registrar_vaca', methods=['GET', 'POST'])
@login_required
def registrar_vaca():
    uid = request.form.get("rfid_uid") # UID from the RFID reader
    if request.method == 'POST':
        breed = request.form['breed']
        gender = request.form['gender']
        birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
        fertile = 'fertile' in request.form
        new_animal = Animal(IDUser=current_user.id, breed=breed, gender=gender, birth=birth_date, fertile=fertile, rfid_uid = uid)
        db.session.add(new_animal)
        db.session.commit()
        publish(MQTT_TOPIC_TRANQUERA, f"Vaca registrada: ID={new_animal.IDAnimal}, Raza={new_animal.breed}")

        flash('¡Vaca registrada con éxito!')
        return redirect(url_for('vacas.registrar_evento', id_animal=new_animal.IDAnimal))
    return render_template('registrar_vaca.html', uid=uid)

@vacas_bp.route('/registrar_evento/<int:id_animal>', methods=['GET'])
@login_required
def registrar_evento(id_animal):
    vaca = Animal.query.get_or_404(id_animal)
    return render_template('registrar_evento.html', vaca=vaca)

@vacas_bp.route('/registrar_peso/<int:id_animal>', methods=['GET', 'POST'])
@login_required
def registrar_peso(id_animal):
    if request.method == 'POST':
        if request.form['action'] == 'cancelar':
            return redirect(url_for('vacas.registrar_evento', id_animal=id_animal))
        peso = float(request.form['peso'])
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        nuevo_peso = WeightHistory(IDAnimal=id_animal, value=peso, date=fecha)
        db.session.add(nuevo_peso)
        db.session.commit()
        registro = Registration(IDUser=current_user.id, IDAnimal=id_animal, EventType='weight', reference_id=nuevo_peso.IDWeight, date=fecha)
        db.session.add(registro)
        db.session.commit()
        flash('Peso registrado correctamente!')
        return redirect(url_for('tranqueras.abrir_corral', id_animal=id_animal))
    return render_template('registrar_peso.html', id_animal=id_animal)

@vacas_bp.route('/registrar_vacuna/<int:id_animal>', methods=['GET', 'POST'])
@login_required
def registrar_vacuna(id_animal):
    if request.method == 'POST':
        if request.form['action'] == 'cancelar':
            return redirect(url_for('vacas.registrar_evento', id_animal=id_animal))
        vacuna = request.form['vacuna']
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        nueva_vacuna = VaccineHistory(IDAnimal=id_animal, vaccineType=vacuna, date=fecha)
        db.session.add(nueva_vacuna)
        db.session.commit()
        registro = Registration(IDUser=current_user.id, IDAnimal=id_animal, EventType='vaccine', reference_id=nueva_vacuna.IDVaccine, date=fecha)
        db.session.add(registro)
        db.session.commit()
        flash('Vacuna registrada correctamente!')
        return redirect(url_for('tranqueras.abrir_corral', id_animal=id_animal))
    return render_template('registrar_vacuna.html', id_animal=id_animal)

@vacas_bp.route('/ver_eventos/<int:id_animal>')
@login_required
def ver_eventos(id_animal):
    registros = Registration.query.filter_by(IDAnimal=id_animal).order_by(Registration.date.desc()).all()
    eventos = []
    for reg in registros:
        if reg.EventType == 'weight':
            peso = WeightHistory.query.get(reg.reference_id)
            eventos.append({'tipo': 'Peso', 'fecha': reg.date, 'detalle': f'{peso.value} kg'})
        elif reg.EventType == 'vaccine':
            vacuna = VaccineHistory.query.get(reg.reference_id)
            eventos.append({'tipo': 'Vacuna', 'fecha': reg.date, 'detalle': vacuna.vaccineType})
    return render_template('ver_eventos.html', eventos=eventos)


@vacas_bp.route('/mis_vacas')
@login_required
def mis_vacas():
    vacas = Animal.query.filter_by(IDUser=current_user.id).all()
    return render_template('mis_vacas.html', vacas=vacas)
