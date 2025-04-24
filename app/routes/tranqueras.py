from flask import Blueprint, render_template, request, jsonify
from app.mqtt_client import publish, MQTT_TOPIC_TRANQUERA

tranqueras_bp = Blueprint('tranqueras', __name__)

@tranqueras_bp.route('/abrir_corral')
def abrir_corral():
    id_animal = request.args.get('id_animal')
    return render_template('abrir_corral.html', id_animal=id_animal)

@tranqueras_bp.route('/abrir_corral', methods=['POST'])
def enviar_mensaje_corral():
    corral = request.json.get('corral')
    if corral in ['1', '2']:
        publish(MQTT_TOPIC_TRANQUERA, f"Abrir corral {corral}")
        return jsonify({"mensaje": f"Corral {corral} abierto correctamente."})
    return jsonify({"mensaje": "Corral inválido"}), 400