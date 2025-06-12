import socket
import google.generativeai as genai
import os

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 6000))
server.listen(1)
print("Esperando texto...")

conn, addr = server.accept()
text = conn.recv(1024).decode()
print("Texto recibido:", text)


response = model.generate_content(text)
print("Gemini responde:", response.text)


conn.send(response.text.encode())
conn.close()
