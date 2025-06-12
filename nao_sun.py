# -*- coding: utf-8 -*-

from naoqi import ALProxy
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

# Crear proxys para texto y movimiento
tts = ALProxy("ALTextToSpeech", IP, PORT)
motion = ALProxy("ALMotion", IP, PORT)

motion.wakeUp()

motion.setAngles(["RShoulderPitch", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                 [0.5, 1.0, 0.5, 0.0], 0.2)
motion.openHand("RHand")

# Saludo
for i in range(3):
    motion.setAngles("RWristYaw", 0.5, 0.2)
    time.sleep(0.3)
    motion.setAngles("RWristYaw", -0.5, 0.2)
    time.sleep(0.3)

motion.closeHand("RHand")

# Frase
tts.say("¡Hola! Soy S.U.N. A.I un asistente tributario inteligente.")
