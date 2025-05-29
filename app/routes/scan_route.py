from flask import Blueprint, render_template, jsonify, redirect, url_for
from app.mqtt_listener import ultimo_uid
from app.models.animal import Animal

scan_bp = Blueprint('scan', __name__)


@scan_bp.route('/scan')
def scan():
    return render_template('scan.html')

@scan_bp.route('/check_tag')
def check_tag():
    if not ultimo_uid:
        return jsonify({"status": "esperando"})

    vaca = Animal.query.filter_by(rfid_uid=ultimo_uid).first()
    if vaca:
        return jsonify({"status": "registrada", "id": vaca.IDAnimal})
    else:
        return jsonify({"status": "nueva", "uid": ultimo_uid})