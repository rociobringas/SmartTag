from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Configurar MQTT
MQTT_BROKER = "tu-servidor-mqtt"
MQTT_TOPIC_TRANQUERA = "campo/tranquera"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/gestion_vacas")
def gestion_vacas():
    return render_template("gestion_vacas.html")

@app.route("/abrir_tranquera", methods=["GET", "POST"])
def abrir_tranquera():
    if request.method == "POST":
        data = request.json
        tranquera_id = data.get("tranquera")
        client.publish(MQTT_TOPIC_TRANQUERA, tranquera_id)
        return jsonify({"mensaje": f"Tranquera {tranquera_id} abierta correctamente"})
    return render_template("abrir_tranquera.html")

if __name__ == "__main__":
    app.run(debug=True)
