import telebot
import json
import os
import unicodedata
import time
from difflib import SequenceMatcher
from dotenv import load_dotenv
from groq import Groq
from typing import Optional
from sentence_transformers import SentenceTransformer, util
# ==============================
# CONFIGURACIÓN Y MODELOS
# ==============================

load_dotenv()

# modelo_embeddings = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased-v2")
modelo_embeddings = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATASET_PATH = "data.json"
PRODUCTOS = "productos.json"

if not TELEGRAM_TOKEN:
    raise ValueError("No se encuentra el TOKEN de Telegram en el archivo .env")
if not GROQ_API_KEY:
    raise ValueError("No se encuentra el API_KEY de Groq en el archivo .env")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

# ==============================
# FUNCIONES AUXILIARES
# ==============================

# Carga el dataset JSON.
def cargar_dataset():
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar el dataset: {e}")
        return None
    
# convierte el texto a minuscula, elimina espacios iniciales, finales y elimina
# signos de interrogacion, exclamacion, y puntuacion.
def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    texto = texto.replace("¿", "").replace("?", "").replace("!", "").replace("¡", "").replace(",", "").replace(".", "").strip()
    return texto

# Similitud basada en coincidencia de caracteres.
def similitud_textual(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Similitud semántica usando SentenceTransformer
cache_embeddings = {}

# Modificación de la función de similitud semántica para usar caché
def similitud_semantica(a, b):
    try:
        if a not in cache_embeddings:
            emb_a = modelo_embeddings.encode(a, convert_to_tensor=True)
            cache_embeddings[a] = emb_a
        else:
            emb_a = cache_embeddings[a]
        
        if b not in cache_embeddings:
            emb_b = modelo_embeddings.encode(b, convert_to_tensor=True)
            cache_embeddings[b] = emb_b
        else:
            emb_b = cache_embeddings[b]

        return float(util.cos_sim(emb_a, emb_b))
    except Exception as e:
        print(f"Error en similitud semántica: {e}")
        return 0

# Combina similitud semántica y textual.
def calcular_similitud(mensaje_usuario, pattern):
    mensaje_usuario = normalizar_texto(mensaje_usuario)
    pattern = normalizar_texto(pattern)
    semantica = similitud_semantica(mensaje_usuario, pattern)
    textual = similitud_textual(mensaje_usuario, pattern)
    return (0.7 * semantica) + (0.3 * textual)

# Busca la mejor coincidencia en el dataset.
def buscar_mejor_respuesta(pregunta, dataset):
    mejor_respuesta = None
    mayor_similitud = 0.0

    for item in dataset:
        posibles_preguntas = item["prompt"]
        if isinstance(posibles_preguntas, str):
            posibles_preguntas = [posibles_preguntas]

        for p in posibles_preguntas:
            similitud = calcular_similitud(pregunta, p) 
            if similitud > mayor_similitud:
                mayor_similitud = similitud
                mejor_respuesta = item["respuesta"]

    if mayor_similitud > 0.65:
        return mejor_respuesta
    return None

# ==============================
# FUNCIONES GROQ (TEXTO + AUDIO)
# ==============================

# Genera una respuesta usando Groq (modelo Llama) y system_prompt en caso de que el bot telegram no encuentre alguna respuesta.
def respuesta_groq(mensaje: str, company_data) -> Optional[str]:
    try:
        system_prompt = f"""Eres el ChatBot de AI assistants. Tu tarea es responder preguntas basándote ÚNICAMENTE en la siguiente información de la empresa. 
Si te preguntan algo que no está en estos datos, indica amablemente que no puedes proporcionar esa información y sugiere contactar directamente con la empresa.

Datos de la empresa:
{json.dumps(company_data, ensure_ascii=False, indent=2)}

Reglas importantes:
1. Solo responde con información que esté en el dataset proporcionado.
2. No inventes ni añadas información adicional.
3. Si la información solicitada no está en el dataset, sugiere contactar a info@IA.com.
4. No respondas preguntas no relacionadas con la empresa.
5. No incluyas en tus respuestas nunca un dato sensible como el número de teléfono del staff.
6. Sé amable y profesional en tus respuestas.
7. Solo debes saludar en la primera interacción del usuario, luego en la conversación no.
8. Usa emojis apropiados relacionados con Inteligencia Artificial.
9. No incluyas saludos como "hola" si ya se ha iniciado la conversación.
10. Siempre responde, pero evita redundancia o repetición de información.
11. NUNCA debes enviar links que no estén activos. Si el usuario solicita ejemplos o catálogos, proporciona siempre la lista completa de páginas que figura en el dataset.
"""
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=500
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error Groq: {e}")
        return None

def transcribir_audio_groq(message: telebot.types.Message) -> Optional[str]:
    """Transcribe un mensaje de voz usando Whisper (Groq)."""
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        temp_file = "temp_voice.ogg"

        with open(temp_file, "wb") as f:
            f.write(downloaded_file)

        with open(temp_file, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(temp_file, file.read()),
                model="whisper-large-v3-turbo",
                language="es",
                response_format="json"
            )
        os.remove(temp_file)
        return transcription.text
    except Exception as e:
        print(f"Error al transcribir audio: {e}")
        return None

# ==============================
# MANEJO DE MENSAJES TELEGRAM
# ==============================
company_data = cargar_dataset()
if company_data:
    print(f"Dataset cargado correctamente. Total de registros: {len(company_data)}")
else:
    print("No se pudo cargar el dataset correctamente.")

@bot.message_handler(commands=["start", "help"])
def bienvenida(message):
    """Mensaje de bienvenida inicial."""
    bot.send_chat_action(message.chat.id, "typing")
    prompt = "Genera un mensaje de bienvenida para el bot de AI assistants que incluya una breve descripción de la empresa y mencione que pueden hacer cualquier pregunta sobre tí."
    respuesta = respuesta_groq(prompt, company_data)
    if respuesta:
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, "¡Hola! Soy el ChatBot de AI assistants. Puedo responder tus preguntas sobre mí y mi identidad.")

@bot.message_handler(content_types=["text"])
def manejar_texto(message):
    """Procesa mensajes de texto."""
    bot.send_chat_action(message.chat.id, "typing")
    pregunta = message.text

    respuesta = buscar_mejor_respuesta(pregunta, company_data)
    if not respuesta:
        respuesta = respuesta_groq(pregunta, company_data)

    if respuesta:
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, "Lo siento, no pude procesar tu consulta. Intenta nuevamente.")

@bot.message_handler(content_types=["voice"])
def manejar_audio(message):
    """Procesa mensajes de voz."""
    bot.send_chat_action(message.chat.id, "typing")

    transcripcion = transcribir_audio_groq(message)
    if not transcripcion:
        bot.reply_to(message, "No pude transcribir el audio. Intenta nuevamente.")
        return

    respuesta = buscar_mejor_respuesta(transcripcion, company_data)
    if not respuesta:
        respuesta = respuesta_groq(transcripcion, company_data)

    if respuesta:
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, "No pude generar una respuesta. Por favor, intenta más tarde.")

# ==============================
# EJECUCION DEL PROGRAMA
# ==============================
if __name__ == "__main__":
    print("Bot de Telegram IA")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error en el bot: {e}")
            print("Reiniciando en 5 segundos...")
            time.sleep(5)