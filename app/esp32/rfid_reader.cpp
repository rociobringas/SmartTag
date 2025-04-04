// aca es para leer las caravanas
// Importamos las bibliotecas necesarias
#include <SPI.h>       // Protocolo SPI para comunicación con el MFRC522
#include <MFRC522.h>   // Librería específica para el lector RFID MFRC522

// Definimos los pines de conexión del MFRC522 al ESP32
#define SS_PIN 5   // Necesita avisarle al lector cuándo quiere hablarle → eso se hace con el SS_PIN, es por donde el esp32 le indica a rfid que s eesta comunicando con el
#define RST_PIN 22 // para reinciar la comunicacion cuando queiro leer un nuevo aniaml

// creo un objeto del tipo modelo del rfid
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
    Serial.begin(115200); // Iniciamos la comunicación serie para depuración
    SPI.begin();          // Iniciamos la comunicación SPI
    mfrc522.PCD_Init();   // Inicializamos el lector RFID

    Serial.println("Lector RFID listo. Acerca una tarjeta...");
}

void loop() {
    // Verificamos si hay una tarjeta cerca del lector
    if (!mfrc522.PICC_IsNewCardPresent()) {
        return; // Si no hay tarjeta, salimos del loop y volvemos a verificar
    }

    // Intentamos leer el contenido de la tarjeta
    if (!mfrc522.PICC_ReadCardSerial()) {
        return; // Si no se pudo leer, salimos del loop y volvemos a intentar
    }

    // Si la tarjeta fue detectada y leída, imprimimos su ID
    Serial.print("ID de la tarjeta: ");
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        // Imprimimos cada byte del ID en formato hexadecimal
        Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.println(); // Salto de línea

    // Detenemos la comunicación con la tarjeta para poder leer otra en el futuro
    mfrc522.PICC_HaltA();
}