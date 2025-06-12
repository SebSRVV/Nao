# -*- coding: utf-8 -*-

from naoqi import ALProxy
import socket
import time

# Conexión con el robot virtual
IP = "127.0.0.1"
PORT = 16127  # Asegúrate de que este puerto es correcto (Choregraphe suele usar 9559)

tts = ALProxy("ALTextToSpeech", IP, PORT)
motion = ALProxy("ALMotion", IP, PORT)

# Solicita entrada de texto (simula escucha)
user_input = raw_input("Escribe lo que NAO 'escucharía': ")

# Enviar a Gemini
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 6000))
client.send(user_input.encode())

# Recibir respuesta
response = client.recv(2048).decode('utf-8')
client.close()

print("Respuesta del modelo:", response)

# --- Animación de saludo mientras habla ---
motion.wakeUp()

# Levanta brazo derecho y abre la mano
motion.setAngles(["RShoulderPitch", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                 [0.5, 1.0, 0.5, 0.0], 0.2)
motion.openHand("RHand")

# Gesto de saludo: mueve la muñeca 3 veces
for i in range(3):
    motion.setAngles("RWristYaw", 0.5, 0.2)
    time.sleep(0.4)
    motion.setAngles("RWristYaw", -0.5, 0.2)
    time.sleep(0.4)

# Cierra la mano
motion.closeHand("RHand")

# Habla la respuesta
tts.say(response.encode('utf-8'))

# Vuelve a la posición de descanso
motion.rest()
