# handlers.commands.py

from utils.image_analyzer import imagen_a_base64, describir_imagen_con_groq
from utils.analisis_sentimientos import analizar_sentimiento
from config.config import bot,cargar_dataset
from services.groq_service import respuesta_groq, transcribir_audio_groq
from utils.logger import logger
import os



company_data = cargar_dataset()


@bot.message_handler(commands=["start", "help"])
def enviar_bienvenida(message):
    texto = """
👋 ¡Hola! Soy un asistente inteligente.

✅ Puedo:
• Responder mensajes de texto
• Escuchar y transcribir audios
• Leer imágenes (tickets, facturas, comprobantes)

📸 Solo enviame una imagen 🧾
🎤 O un audio 🎙️
📝 O escribime lo que necesites ✍️
"""
    bot.reply_to(message, texto)


@bot.message_handler(content_types=['photo'])

def manejar_foto(mensaje):
    try:
        bot.reply_to(mensaje, "📸 He recibido tu imagen. Analizándola... ⏳")
        foto = mensaje.photo[-1]
        info_archivo = bot.get_file(foto.file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)

        imagen_base64 = imagen_a_base64(archivo_descargado)
        if not imagen_base64:    
            bot.reply_to(mensaje, "❌ Error al procesar la imagen. Intenta de nuevo.")
            return
        
        descripcion = describir_imagen_con_groq(imagen_base64)
        if descripcion:
            respuesta = f"🤖 **Descripción de la imagen:**\n\n{descripcion}"
            bot.reply_to(mensaje, respuesta, parse_mode=None)
        else:
            bot.reply_to(mensaje, "❌ No pude analizar la imagen. Por favor, intenta con otra imagen.")

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        bot.reply_to(mensaje, "❌ Ocurrió un error al procesar tu imagen. Intenta de nuevo.")


@bot.message_handler(content_types=["voice"])

def manejar_audio(message):
    bot.send_chat_action(message.chat.id, "typing")

    transcripcion = transcribir_audio_groq(message)
    if not transcripcion:
        bot.reply_to(message, "No pude transcribir el audio. Intenta nuevamente.")
        return

    # respuesta = buscar_mejor_respuesta(transcripcion, company_data)
    # if not respuesta:
    respuesta = respuesta_groq(transcripcion, company_data)

    if respuesta:
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, "No pude generar una respuesta. Por favor, intenta más tarde.")


# @bot.message_handler(content_types=["text"])

# def manejar_texto(message):
#     bot.send_chat_action(message.chat.id, "typing")
#     pregunta = message.text

#     # respuesta = buscar_mejor_respuesta(pregunta, company_data)
#     # if not respuesta:
#     respuesta = respuesta_groq(pregunta, company_data)

#     if respuesta:
#         bot.reply_to(message, respuesta)
#     else:
#         bot.reply_to(message, "Lo siento, no pude procesar tu consulta. Intenta nuevamente.")


@bot.message_handler(content_types=["text"])
def manejar_texto(message):
    bot.send_chat_action(message.chat.id, "typing")
    user_text = message.text
    user_name = message.from_user.username or "Usuario"

    respuesta = respuesta_groq(user_text, company_data)
    if respuesta:
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, "Lo siento, no pude procesar tu consulta. Intenta nuevamente.")

    # --- 1️⃣ Analizar y registrar sentimiento ---
    sentimiento = analizar_sentimiento(user_text)
    logger.info(f"🧠 Análisis de sentimiento - Usuario: {user_name} | Sentimiento: {sentimiento}")

    # --- 2️⃣ Enviar al admin (opcional) ---
    ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
    if ADMIN_CHAT_ID:
        try:
            bot.send_message(
                ADMIN_CHAT_ID,
                f"🔍 *ANÁLISIS DE MENSAJE*\n👤 @{user_name}\n💬 {user_text}\n🧠 {sentimiento}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.warning(f"No se pudo enviar el análisis al admin: {e}")

    # --- 3️⃣ Generar respuesta normalmente ---
    respuesta = respuesta_groq(user_text, company_data)
    if respuesta:
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, "Lo siento, no pude procesar tu consulta. Intenta nuevamente.")

@bot.message_handler(func=lambda msg: True)

def manejar_otros(message):
    bot.reply_to(message, "No entiendo ese tipo de mensaje. Envíame texto, audio o una imagen. 👀")