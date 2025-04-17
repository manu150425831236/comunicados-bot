from flask import Flask, Response
from threading import Thread
import requests
from bs4 import BeautifulSoup
import time

app = Flask('')

@app.route('/')
def home():
    return Response("<h1>Bot activo ✅</h1>", mimetype="text/html")

def run():
    app.run(host='0.0.0.0', port=8080)

def mantener_vivo():
    t = Thread(target=run)
    t.start()

# CONFIGURACIÓN
URL = "https://secretariadeasuntosdocentes2laplata.blogspot.com/"
TOKEN = "7851025025:AAHOtTlJ5I4HBIeJh8t7-G5N-p8KZvpCbKw"
CHAT_ID = "1834269373"
TIEMPO_ESPERA = 300  # 5 minutos

def obtener_ultimo_comunicado():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        comunicados = soup.find_all('h3', class_='post-title entry-title')
        if comunicados:
            entrada = comunicados[0]
            titulo = entrada.get_text(strip=True)
            enlace = entrada.find('a')['href'] if entrada.find('a') else URL
            return titulo, enlace
    except Exception as e:
        print(f"Error al acceder a la página: {e}")
    return None, None

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=payload)
        print("✅ Alerta enviada por Telegram.")
    except Exception as e:
        print(f"Error al enviar mensaje por Telegram: {e}")

# INICIO DEL BOT
mantener_vivo()
titulo_anterior, _ = obtener_ultimo_comunicado()
print(f"📌 Último comunicado detectado: {titulo_anterior}")
print("🔎 Iniciando monitoreo...")

while True:
    time.sleep(TIEMPO_ESPERA)
    titulo_actual, link_actual = obtener_ultimo_comunicado()
    if titulo_actual and titulo_actual != titulo_anterior:
        mensaje = f"🔔 Nuevo comunicado:\n\n📝 {titulo_actual}\n🔗 {link_actual}"
        enviar_telegram(mensaje)
        titulo_anterior = titulo_actual
    else:
        print("⏳ Sin nuevos comunicados.")
