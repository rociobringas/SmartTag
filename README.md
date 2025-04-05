PLS NO BORREN LOS COMENTARIOS DE LOS FILES, SI CAMBIAN ALGO LOS COMENTARIOS QUEDAN!!!!!
📌 Flujo Resumido

1⃣ C++ (RFID + MQTT) → Lee el ID del animal y lo envía por MQTT (rfid/lectura).
2⃣ Flask (Python + BD) → Recibe el ID, busca al animal en la base de datos.
3⃣ Flask (MQTT) → Si el animal está registrado, publica "abrir" en tranqueras/control.
4⃣ ESP32 (MQTT + GPIO) → Recibe "abrir", activa el motor y abre la tranquera.
5⃣ Flask (BD) → Guarda en la base de datos que el animal entró.
6⃣ ESP32 (MQTT) → Detecta la salida y publica en rfid/salida.
7⃣ Flask (BD) → Registra la salida del animal.

💡 Básicamente:
📤 C++ lee → 📡 MQTT envía → 🖥 Flask consulta → 🚪 ESP32 abre/cierra

🧠 Resumen del flujo completo
1.	La app envía un ángulo deseado (por MQTT o similar).
2.	El ESP32 activa el motor NEMA 17 y empieza a abrir la tranquera.
3.	Un sensor inductivo detecta que la tranquera llegó al ángulo deseado (tope físico).
4.	Se espera a que el animal pase, detectado por una barrera fotoeléctrica.
5.	El ESP32 cierra la tranquera con el motor NEMA 17 en sentido contrario

rfid 
    modelo = MFRC522
    como se comunica con el esp32 = Serial Peripheral Interface 


3 de abril 21hs ROCHI
- hice la carptea esp32, ahi es para hacer la config de mosquito, el codigo en c++ 
para abrir y cerrar las tranqueras y para el sensor rfid
- hay que probar si funciona el rfid code
- el gate code no esta terminado, le falta conectar la parte del sensor que detecta que 
el animal ya paso y que se cierre la tranquera pero necesitamos perobarlo en directo con 
los sensores 

4 de abril 20hs FACU
- Agrego archivo requirements.txt que tiene todas las librerias necesarias peara correr 
la aplicacion. 
- Para instalar las librerias solo hay que correr un comando desde el directorio SmartTag
    **pip install -r requirements.txt**
- Si se agrega o se elimina alguna libreria hay que actualizar el archivo requirements.txt, 
con una linea de codigo. **pip freeze > requirements.txt** 
- Se hace commit y push del archivo y despues los otros tienen que hacer git pull y correr 
el codigo para descargar las nuevas librerias. **pip install -r requirements.txt**
- Cree el archivo .gitignore que es para que git cuando hacemos commit y push los ignore y 
nunca pushee esas cosas. Ahi esta la carpeta .idea que es una carpeta del idea de cada uno 
y tambien esta la carpeta del entorno virtual que eso cada uno se lo crea en su computadora.
Y despues los otros me dijo chat que los agregue, son una compilaciones de python ni idea.

5 de abril 10hs
- Modifique los archivos de login para que quede mas prolijo, con alertas y todo.
- Cree los archivos user.py y modelUser.py para el modelado de los usuarios.
- Agregue librerias al requirements
 