from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.models.animal import Animal
from app.mqtt_listener import obtener_uid, limpiar_uid

scan_bp = Blueprint('scan', __name__)


@scan_bp.route('/scan')
@login_required
def scan():
    return render_template('scan.html')

@scan_bp.route('/check_tag')
@login_required
def check_tag():
    uid = obtener_uid()
    if not uid:
        return jsonify({"status": "esperando"})

    vaca = Animal.query.filter_by(rfid_uid=uid).first()

    # 🔴 Limpiamos el UID para que no se use más
    limpiar_uid()

    if vaca:
        return jsonify({"status": "registrada", "id": vaca.IDAnimal})
    else:
        return jsonify({"status": "nueva", "uid": uid})