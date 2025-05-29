import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "52.3.134.187"
MQTT_PORT = 1883
TOPICS = [
    ("tranquera/estado", 0),
    ("rfid/lectura", 0),
]

ultimo_uid = None  # Variable global para almacenar el último UID leído

def on_connect(client, userdata, flags, rc):
    print("✅ Conectado al broker MQTT con código:", rc)
    for topic, qos in TOPICS:
        client.subscribe(topic)
        print(f"🔔 Suscripto a: {topic}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    global ultimo_uid
    print(f"[📥 MQTT] Mensaje recibido en {topic}: {payload}")  

    if topic == "tranquera/estado":
        try:
            data = json.loads(payload)  # <-- ✅ Parsear JSON
            estado = data.get("estado")
            corral = data.get("corral")
            if estado == "abierta":
                print(f"🔓 La tranquera del corral {corral} fue abierta")
            elif estado == "cerrada":
                print(f"🔒 La tranquera del corral {corral} fue cerrada")
            else:
                print(f"⚠️ Estado desconocido: {estado}")
        except Exception as e:
            print(f"❌ Error al interpretar JSON del mensaje: {e}")
    elif topic == "rfid/lectura":
        ultimo_uid = payload.strip()  # Eliminar espacios en blanco
        print(f"🔖 UID leído: {ultimo_uid}")

def start_mqtt_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()  # Escuchar en segundo plano
    except Exception as e:
        print(f"❌ Error al conectar al broker MQTT: {e}")

    return client
