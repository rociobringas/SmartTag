import paho.mqtt.client as mqtt

MQTT_BROKER = "172.31.90.218"
MQTT_PORT = 1883
TOPICS = [
    ("tranquera/estado", 0),
    # Podés agregar más topics si querés escuchar otros
]

def on_connect(client, userdata, flags, rc):
    print("✅ Conectado al broker MQTT con código:", rc)
    for topic, qos in TOPICS:
        client.subscribe(topic)
        print(f"🔔 Suscripto a: {topic}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[📥 MQTT] Mensaje recibido en {topic}: {payload}")

    # Solo mostramos el mensaje. No se guarda en la base de datos.
    if topic == "tranquera/estado":
        if payload == "abierta":
            print("🔓 La tranquera fue abierta")
        elif payload == "cerrada":
            print("🔒 La tranquera fue cerrada")

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
