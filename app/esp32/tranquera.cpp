#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "Stepper.h"

// Motor de barrera (usa Step/Dir como antes)
const int dirPinBarrera = 5;
const int stepPinBarrera = 19;
const int stepsPerRevolution = 200; // # de pasos q necesita el motor para dar vuelta completa
const int velocity = 750;

// Motor de cuchilla eliminado — no lo usamos
// Pines para sensores
const int sensorInductivoPin = 16;    // Detecta barrera completamente abierta
const int sensorFotoelectricoPin = 3; // Detecta si pasó el animal

// Variables de control
volatile bool sensorInductivoActivado = false;
volatile bool sensorFotoelectricoActivado = false;

bool abriendo = false;
bool esperandoAnimal = false;
bool cerrando = false;

void IRAM_ATTR sensorInductivoInterrupt() {
  sensorInductivoActivado = true;
}

void IRAM_ATTR sensorFotoelectricoInterrupt() {
  sensorFotoelectricoActivado = true;
}

void setup() {
  Serial.begin(115200);

  pinMode(dirPinBarrera, OUTPUT);
  pinMode(stepPinBarrera, OUTPUT);
  pinMode(sensorInductivoPin, INPUT_PULLUP);
  pinMode(sensorFotoelectricoPin, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(sensorInductivoPin), sensorInductivoInterrupt, FALLING);
  attachInterrupt(digitalPinToInterrupt(sensorFotoelectricoPin), sensorFotoelectricoInterrupt, FALLING);
}

void loop() {
  // Si se recibe una señal para abrir (por ahora lo activamos automáticamente para demo)
  if (!abriendo && !esperandoAnimal && !cerrando) {
    abrirBarrera();
  }

  // Esperar que se active el sensor inductivo (barrera abierta)
  if (abriendo && sensorInductivoActivado) {
    detenerMotor();
    sensorInductivoActivado = false;
    esperandoAnimal = true;
    abriendo = false;
  }

  // Cuando se detecta que el animal pasó, cerrar la barrera
  if (esperandoAnimal && sensorFotoelectricoActivado) {
    sensorFotoelectricoActivado = false;
    esperandoAnimal = false;
    cerrarBarrera();
  }

  // Barrera se cerró (por pasos), volver al estado inicial
  if (cerrando) {
    detenerMotor();
    cerrando = false;
    delay(1000);
  }
}

void abrirBarrera() {
  Serial.println("Abriendo barrera...");
  digitalWrite(dirPinBarrera, LOW); // Dirección apertura

  abriendo = true;
  while (!sensorInductivoActivado) {
  // while (digitalRead(sensorInductivoPin) == HIGH) {
    digitalWrite(stepPinBarrera, HIGH);
    delayMicroseconds(velocity);
    digitalWrite(stepPinBarrera, LOW);
    delayMicroseconds(velocity);
  }

  // Una vez activado el sensor, parar motor
  detenerMotor();
  abriendo = false;
  sensorInductivoActivado = false;

  esperandoAnimal = true;
}

void cerrarBarrera() {
  Serial.println("Cerrando barrera...");
  digitalWrite(dirPinBarrera, HIGH); // Dirección cierre
  for (int x = 0; x < pasosBarrera; x++) {
    digitalWrite(stepPinBarrera, HIGH);
    delayMicroseconds(velocity);
    digitalWrite(stepPinBarrera, LOW);
    delayMicroseconds(velocity);
  }
  cerrando = true;
}

void detenerMotor() {
  digitalWrite(stepPinBarrera, LOW);
}