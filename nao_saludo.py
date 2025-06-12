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
IP = env.get("NAO_IP")
PORT = int(env.get("NAO_PORT"))

try:
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    motion = ALProxy("ALMotion", IP, PORT)
except Exception as e:
    print("❌ Error al conectar con el robot:", e)
    exit(1)

motion.wakeUp()
motion.setStiffnesses("RArm", 1.0)

texto = "Hi Hitler"

tts.post.say(texto)

motion.setAngles(
    ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"],
    [0.0, -0.3, 1.5, 0.0, -1.5],
    0.2
)
motion.openHand("RHand")

duracion = len(texto) * 0.06
time.sleep(duracion + 1.0) 

motion.closeHand("RHand")
motion.setAngles(
    ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"],
    [1.5, 0.0, 1.2, 0.0, 0.0],
    0.2
)
