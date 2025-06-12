import google.generativeai as genai

genai.configure(api_key="AIzaSyBmf_0dxaf-Y3w-UK6vcZ55L_G1fKZwjFU")
models = genai.list_models()

for m in models:
    print(m.name)
