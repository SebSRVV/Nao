import socket
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("[ - ] Falta la API KEY de Gemini. Configura GEMINI_API_KEY en el entorno.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 6000))
server.listen(5)

print("[ + ] Servidor Gemini activo. Esperando texto...")

try:
    while True:
        conn, addr = server.accept()
        print(f"[ + ] Conexion desde {addr}")

        try:
            text = conn.recv(1024).decode("utf-8")
            print("[ / ] Texto recibido:", text)

            if not text.strip():
                response_text = "No recibi nada para responder."
            else:
                response = model.generate_content(text)
                response_text = response.text.strip() if response.text else "No tengo una respuesta clara."

            print("[ + ] Gemini responde:", response_text)
            conn.send(response_text.encode("utf-8"))

        except Exception as e:
            print("[ - ] Error durante la generacion:", e)
            conn.send("Ocurrio un error al generar la respuesta.".encode("utf-8"))

        finally:
            conn.close()
            print("[ / ] Esperando siguiente conexion...\n")

except KeyboardInterrupt:
    print("\n[ - ] Servidor detenido manualmente.")
finally:
    server.close()
