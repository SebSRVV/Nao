 # NAO Virtual Assistant with Gemini API

Este proyecto conecta un robot NAO con la API de Gemini (Google AI). El robot escucha una entrada , la envía a Gemini para generar una respuesta inteligente y la dice mientras realiza un gesto de saludo.

📁 Estructura del proyecto

.

├── nao_virtual.py         # Script principal para entorno Virtual en Python 2.7 para NAO

├── nao_real.py         # Script principal para entorno Real en Python 2.7 para NAO

├── nao_egg.py         # Script Easter Egg en Python 2.7 para NAO

├── nao_saludo.py         # Un Peculiar saludo en Python 2.7 para NAO

├── gemini.py     # Servidor Gemini en Python 3 que responde al texto

├── models.py     # Script para saber que modelos tiene acceso tu API KEY

├── .env                  # Archivo de configuración con IP, puerto y API key

└── README.md             # Esta documentación

🔧 Requisitos

Python 2.7 : https://www.python.org/downloads/release/python-2718/

Naoqi: https://drive.google.com/drive/folders/1qV5SQoCFunSMaVyAQVcsozLhM4F6K4zx

Para correr el script, usa el siguiente comando:

`py -2.7 nao_listen.py`


Python 3+ (para gemini.py)

`pip install google-generativeai python-dotenv`

🔐 .env

NAO_IP

NAO_PORT

GEMINI_API_KEY

# Desarrollado por SebRVV
