// aca se controlan las tranqueras
#include <Arduino.h>

#define DIR_PIN 26    // Dirección del motor
#define STEP_PIN 25   // Paso del motor
#define SENSOR_PIN 33 // Sensor inductivo

void setup() {
    pinMode(DIR_PIN, OUTPUT);
    pinMode(STEP_PIN, OUTPUT);
    pinMode(SENSOR_PIN, INPUT);

    digitalWrite(DIR_PIN, HIGH); // Sentido de apertura
}

void loop() {
    if (digitalRead(SENSOR_PIN) == LOW) { // Si el sensor NO detecta el tope, seguimos
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(500);
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(500);
    } else {
        Serial.println("Tranquera abierta, tope detectado");
        while (true); // Se detiene aquí hasta el siguiente paso
    }
}
// falta ponerle que se cierre cuando detecta que el animal paso, pero estaria bueno hacerlo con los sensores