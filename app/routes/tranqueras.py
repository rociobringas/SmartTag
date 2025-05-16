from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.mqtt_client import publish, MQTT_TOPIC_TRANQUERA

tranqueras_bp = Blueprint('tranqueras', __name__)

# Página para elegir a qué corral abrir
@tranqueras_bp.route('/abrir_corral')
@login_required
def abrir_corral():
    id_animal = request.args.get('id_animal')
    return render_template('abrir_corral.html', id_animal=id_animal)

# Publicar mensaje MQTT para abrir un corral
@tranqueras_bp.route('/abrir_corral', methods=['POST'])
@login_required
def enviar_mensaje_corral():
    data = request.get_json()
    corral = data.get('corral')
    id_animal = data.get('id_animal')

    if not corral or corral not in ['1', '2']:
        return jsonify({"mensaje": "Corral inválido"}), 400

    if not id_animal:
        return jsonify({"mensaje": "ID de animal faltante"}), 400

    mensaje = {
        "accion": "abrir",
        "corral": corral,
        "id_animal": id_animal
    }

    publish(MQTT_TOPIC_TRANQUERA, mensaje)
    return jsonify({"mensaje": f"Corral {corral} abierto correctamente."})

# Página para cerrar corral (simple)
@tranqueras_bp.route('/cerrar_corral')
@login_required
def cerrar_corral():
    return render_template('cerrar_corral.html')

# Publicar mensaje MQTT para cerrar corral
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
