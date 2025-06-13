#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Stepper.h>
#include <ArduinoJson.h>

// ------------------------ CONFIG ------------------------ //
#define RST_PIN  21
#define SS_PIN   5

const char* ssid = "UA-Alumnos";
const char* password = "41umn05WLC";

const char* mqtt_server = "52.3.134.187";
const int mqtt_port = 1883;
const char* mqtt_topic = "rfid/lectura";

WiFiClient espClient;
PubSubClient client(espClient);
MFRC522 mfrc522(SS_PIN, RST_PIN);

// ------------------------ MOTOR 1 + SENSOR 1 ------------------------ //
#define SENSOR_PIN1 3
const int pasosPorRevolucion = 200; 
Stepper motor(pasosPorRevolucion, 32, 33, 25, 4); // ⚠️ No usar pin 5
int enaA = 26;
int enaB = 27;
int movimientos1 = 0;

// ------------------------ MOTOR 2 + SENSOR 2 ------------------------ //
#define SENSOR_PIN2 15
const int dirPin = 12;
const int stepPin = 14;
const int stepsPerRevolution = 200;
const int velocity= 2000; // A menor numero mayor velocidad (750 es lo maximo)
int movimientos2 = 0;

// ------------------------ FLAGS + DATOS ------------------------ //
bool abrir = false;
bool cerrar = false;
String corral_actual = "1";
String id_animal_actual = "";
String lastUID = "";

// ------------------------ FUNCIONES WIFI ------------------------ //
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\n✅ WiFi conectado");
  Serial.print("IP: "); Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando conexión MQTT...");
    if (client.connect("ESP32Reader")) {
      Serial.println("conectado ✅");
      client.subscribe("campo/tranquera");  // ✅ Suscripción correcta
    } else {
      Serial.print("❌ fallo, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

// ------------------------ FUNCIONES AUXILIARES ------------------------ //
void publicarEstado(String estado) {
  StaticJsonDocument<128> doc;
  doc["estado"] = estado;
  doc["corral"] = corral_actual;
  doc["id_animal"] = id_animal_actual;

  char buffer[128];
  serializeJson(doc, buffer);
  client.publish("tranquera/estado", buffer);
}


// -------- MOVER MOTOR 1 -------------- //
void moverMotor1HastaSensor() {
  Serial.println("🚀 Abriendo tranquera 1...");
  digitalWrite(enaA, HIGH);
  digitalWrite(enaB, HIGH);
  while((digitalRead(SENSOR_PIN1) != LOW)){
    motor.step(1);
    movimientos1++;
    delay(5);
  }
  Serial.println("💥 Sensor activado → detener motor");
  digitalWrite(enaA, LOW);
  digitalWrite(enaB, LOW);
  publicarEstado("abierta");
}

void cerrarTranquera1() {
  Serial.println("🔄 Cerrando tranquera 1...");
  digitalWrite(enaA, HIGH);
  digitalWrite(enaB, HIGH);
  motor.step(-movimientos1);
  digitalWrite(enaA, LOW);
  digitalWrite(enaB, LOW);
  publicarEstado("cerrada");
  Serial.println("Corral 1 cerrado.");
}

// -------- MOVER MOTOR 2 ----------- //

void moverMotor2HastaSensor(){
  Serial.println("🚀 Abriendo tranquera 2...");
  digitalWrite(dirPin, LOW);
  while ((digitalRead(SENSOR_PIN2) != LOW)){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(velocity);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(velocity);
    movimientos2++;
  }
  Serial.println("💥 Sensor 2 activado → detener motor 2");
  publicarEstado("abierta");
}

void cerrarTranquera2(){
  Serial.println("🔄 Cerrando tranquera 2...");
  digitalWrite(dirPin, HIGH);  // sentido opuesto al de abrir

  for (int i = 0; i < movimientos2; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(velocity);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(velocity);
  }

  publicarEstado("cerrada");
  Serial.println("Corral 2 cerrado.");
}


// ------------------------ CALLBACK MQTT ------------------------ //
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("📩 Mensaje recibido: ");
  String msg = "";
  for (int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.println(msg);

  StaticJsonDocument<128> doc;
  DeserializationError error = deserializeJson(doc, msg);
  if (error) {
    Serial.println("❌ Error al parsear JSON");
    return;
  }

  String accion = doc["accion"];
  corral_actual = doc["corral"] | "1";
  id_animal_actual = doc["id_animal"] | "";

  if (accion == "abrir") {
    abrir = true;
  } else if (accion == "cerrar") {
    cerrar = true;
  }
}

// ------------------------ RFID ------------------------ //
String getUIDString() {
  String uidStr = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) uidStr += "0";
    uidStr += String(mfrc522.uid.uidByte[i], HEX);
  }
  uidStr.toUpperCase();
  return uidStr;
}

// ------------------------ SETUP ------------------------ //
void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  mfrc522.PCD_SetAntennaGain(mfrc522.RxGain_48dB);

  motor.setSpeed(30);
  pinMode(enaA, OUTPUT);
  pinMode(enaB, OUTPUT);
  pinMode(SENSOR_PIN1, INPUT);

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(SENSOR_PIN2, INPUT);

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

// ------------------------ LOOP ------------------------ //
void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
  String uid = getUIDString();

  if (uid != lastUID) {
    Serial.print("UID detectado: "); 
    Serial.println(uid);
    client.publish(mqtt_topic, uid.c_str());
    lastUID = uid;
  } else {
    Serial.println("UID repetido, ignorado.");
  }

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
  delay(3000); // esperar para evitar múltiples lecturas
}

  // Motor 
  if (abrir) {
    if (corral_actual == "1"){
      moverMotor1HastaSensor();
    } else if (corral_actual == "2"){
      moverMotor2HastaSensor();
    }
    abrir = false;
  }
  if (cerrar) {
    if (corral_actual == "1") {
      cerrarTranquera1();
    } else if (corral_actual == "2") {
      cerrarTranquera2();
    }
  cerrar = false;
}


}
