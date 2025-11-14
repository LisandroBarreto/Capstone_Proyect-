#services/groq_service.py

from typing import Optional
import json
import os 
import telebot
from config.config import bot, groq_client
from utils.logger import logger


# Genera una respuesta usando Groq (modelo Llama) y system_prompt en caso de que el bot telegram no encuentre alguna respuesta.
def respuesta_groq(mensaje: str, company_data) -> Optional[str]:
    try:
        logger.info(f"Analizando pregunta con Groq: {mensaje}")
        system_prompt = f"""Eres el ChatBot que tiene conocimienteo sobre economia y finanzas. Tu tarea es responder preguntas basándote ÚNICAMENTE en la siguiente información de la empresa. 
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