import json
import paho.mqtt.client as mqtt

MQTT_BROKER = "172.31.90.218"
MQTT_PORT = 1883
MQTT_TOPIC_TRANQUERA = "campo/tranquera"

def create_mqtt_client():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

def publish(topic, message):
    try:
        client = create_mqtt_client()

        # Si el mensaje es un diccionario, lo convertimos a JSON string
        if isinstance(message, dict):
            message = json.dumps(message)

        # Publicamos el mensaje
        result = client.publish(topic, message)

        # Esperar hasta que se publique realmente
        result.wait_for_publish()

        client.disconnect()

    except Exception as e:
        print(f"Error al publicar MQTT: {e}")

