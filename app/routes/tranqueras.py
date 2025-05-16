from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.mqtt_client import publish, MQTT_TOPIC_TRANQUERA

tranqueras_bp = Blueprint('tranqueras', __name__)

@tranqueras_bp.route('/abrir_corral')
@login_required
def abrir_corral():
    id_animal = request.args.get('id_animal')
    return render_template('abrir_corral.html', id_animal=id_animal)

@tranqueras_bp.route('/cerrar_corral', methods=['POST'])
@login_required
def enviar_mensaje_cerrar_corral():
    data = request.get_json()
    corral = data.get('corral')

    if corral not in ['1', '2']:
        return jsonify({"mensaje": "Corral inválido"}), 400

    mensaje = {
        "accion": "cerrar",
        "corral": corral
    }

    publish(MQTT_TOPIC_TRANQUERA, mensaje)
    return jsonify({"mensaje": f"Corral {corral} cerrado correctamente."})


@tranqueras_bp.route('/abrir_corral', methods=['POST'])
@login_required
def enviar_mensaje_corral():
    data = request.get_json()
    corral = data.get('corral')
    id_animal = data.get('id_animal')

    if corral not in ['1', '2']:
        return jsonify({"mensaje": "Corral inválido"}), 400

    mensaje = {
        "accion": "abrir",
        "corral": corral,
        "id_animal": id_animal
    }

    publish(MQTT_TOPIC_TRANQUERA, mensaje)
    return jsonify({"mensaje": f"Corral {corral} abierto correctamente."})
