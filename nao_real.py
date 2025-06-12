# -*- coding: utf-8 -*-
from naoqi import ALProxy
import socket
import time

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

# Proxys necesarios
tts = ALProxy("ALTextToSpeech", IP, PORT)
motion = ALProxy("ALMotion", IP, PORT)
speech_recog = ALProxy("ALSpeechRecognition", IP, PORT)
memory = ALProxy("ALMemory", IP, PORT)

motion.wakeUp()

language = "Spanish"  # Cambiar a "English"
speech_recog.setLanguage(language)

# Palabras que puede reconocer
vocabulario = ["hola", "cómo estás", "quién eres", "adiós", "ayuda"]
speech_recog.setVocabulary(vocabulario, False)

# Suscribirse al reconocimiento
speech_recog.subscribe("mi_app")
print("🎤 NAO está escuchando... di algo del vocabulario.")

# Esperar a que escuche algo
palabra_escuchada = None
timeout = time.time() + 10  # Espera 10 segundos máx

while palabra_escuchada is None and time.time() < timeout:
    data = memory.getData("WordRecognized")
    if data and isinstance(data, list) and len(data) > 1 and data[1] > 0.4:
        palabra_escuchada = data[0]
    time.sleep(0.1)

speech_recog.unsubscribe("mi_app")

if palabra_escuchada is None:
    print("⏱️ No se escuchó nada.")
    tts.say("No escuché nada.")
    exit(0)

print("🗣️ NAO escuchó:", palabra_escuchada)

# Enviar lo escuchado al modelo
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", GEMINI_PORT))
client.send(palabra_escuchada.encode())
response = client.recv(2048).decode('utf-8')
client.close()

print("💬 Respuesta del modelo:", response)

# Gesto mientras habla
motion.setAngles(["RShoulderPitch", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                 [0.5, 1.0, 0.5, 0.0], 0.2)
motion.openHand("RHand")

for i in range(3):
    motion.setAngles("RWristYaw", 0.5, 0.2)
    time.sleep(0.3)
    motion.setAngles("RWristYaw", -0.5, 0.2)
    time.sleep(0.3)

motion.closeHand("RHand")

# Decir respuesta
tts.say(response.encode('utf-8'))
