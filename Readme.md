 # NAO Virtual Assistant with Gemini API

Este proyecto conecta un robot NAO (real en este caso ya que es de prueba) con la API de Gemini (Google AI) para crear un asistente conversacional. El robot escucha una entrada (simulada), la envía a Gemini para generar una respuesta inteligente y la dice mientras realiza un gesto de saludo.

📁 Estructura del proyecto

.

├── nao_listen.py         # Script principal en Python 2.7 para NAO

├── gemini_respond.py     # Servidor Gemini en Python 3 que responde al texto

├── .env                  # Archivo de configuración con IP, puerto y API key

└── README.md             # Esta documentación

🔧 Requisitos

Python 2.7 : https://www.python.org/downloads/release/python-2718/

Naoqi: https://drive.google.com/drive/folders/1qV5SQoCFunSMaVyAQVcsozLhM4F6K4zx

py -2.7 nao_listen.py

Python 3+ (para gemini_respond.py)

pip install google-generativeai python-dotenv

🔐 .env

NAO_IP

NAO_PORT

GEMINI_API_KEY

# Desarrollado por SebRVV
