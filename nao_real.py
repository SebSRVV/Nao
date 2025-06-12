# -*- coding: utf-8 -*-
from naoqi import ALProxy
import socket
import time
import os

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
        print("[- ] No se pudo cargar el archivo .env")
    return env

env = load_env()
IP = env.get("NAO_IP", "127.0.0.1")
PORT = int(env.get("NAO_PORT", "9559"))
GEMINI_PORT = int(env.get("GEMINI_PORT", "6000"))

# Conectar a proxys
tts = ALProxy("ALTextToSpeech", IP, PORT)
motion = ALProxy("ALMotion", IP, PORT)
speech_recog = ALProxy("ALSpeechRecognition", IP, PORT)
memory = ALProxy("ALMemory", IP, PORT)
posture = ALProxy("ALRobotPosture", IP, PORT)

motion.wakeUp()
posture.goToPosture("StandInit", 0.5)

idioma = "Spanish"  # Cambiar a "English" si corresponde
speech_recog.setLanguage(idioma)

# Lista de palabras
vocabulario = ["hola", "como estas", "quien eres", "adios", "ayuda"]
speech_recog.setVocabulary(vocabulario, False)

speech_recog.subscribe("nao_app")
print("[ + ] NAO esta escuchando...")

palabra_escuchada = None
timeout = time.time() + 10

while palabra_escuchada is None and time.time() < timeout:
    data = memory.getData("WordRecognized")
    if isinstance(data, list) and len(data) > 1 and data[1] > 0.4:
        palabra_escuchada = data[0]
    time.sleep(0.1)

speech_recog.unsubscribe("nao_app")

if palabra_escuchada is None:
    print("[- ] No se escucho nada.")
    tts.say("No escuche nada.")
    motion.rest()
    exit(0)

print("[ / ] Palabra escuchada:", palabra_escuchada)

# Enviar al servidor Gemini
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", GEMINI_PORT))
    client.send(palabra_escuchada.encode("utf-8"))

    response = client.recv(2048).decode("utf-8")
    client.close()
except Exception as e:
    print("[- ] Error al conectar con el servidor Gemini:", e)
    tts.say("No pude conectar con el servidor.")
    motion.rest()
    exit(1)

print("[ + ] Respuesta de Gemini:", response)

# Gesto mientras habla
motion.setStiffnesses("RArm", 1.0)
motion.setAngles(["RShoulderPitch", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                 [0.5, 1.0, 0.5, 0.0], 0.2)
motion.openHand("RHand")

for i in range(2):
    motion.setAngles("RWristYaw", 0.5, 0.2)
    time.sleep(0.3)
    motion.setAngles("RWristYaw", -0.5, 0.2)
    time.sleep(0.3)

motion.closeHand("RHand")

# Decir respuesta
tts.say(response.encode("utf-8"))

motion.rest()
