# -*- coding: utf-8 -*-

from naoqi import ALProxy
import socket
import time

# Mi .env
def load_env(filename=".env"):
    env = {}
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    except IOError:
        print("No se pudo cargar el archivo .env")
    return env

env = load_env()
IP = env.get("NAO_IP", "127.0.0.1")
PORT = int(env.get("NAO_PORT", "9559"))
GEMINI_PORT = int(env.get("GEMINI_PORT", "6000"))

# Proxys
tts = ALProxy("ALTextToSpeech", IP, PORT)
motion = ALProxy("ALMotion", IP, PORT)

motion.wakeUp()

user_input = raw_input("Escribe lo que NAO 'escucharia': ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", GEMINI_PORT))
client.send(user_input.encode())

response = client.recv(2048).decode('utf-8')
client.close()

print("Respuesta del modelo:", response)

motion.setAngles(["RShoulderPitch", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                 [0.5, 1.0, 0.5, 0.0], 0.2)
motion.openHand("RHand")

for i in range(3):
    motion.setAngles("RWristYaw", 0.5, 0.2)
    time.sleep(0.3)
    motion.setAngles("RWristYaw", -0.5, 0.2)
    time.sleep(0.3)

motion.closeHand("RHand")

tts.say(response.encode('utf-8'))

