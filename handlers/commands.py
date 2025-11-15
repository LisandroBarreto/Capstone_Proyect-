# handlers/commands.py

from utils.image_analyzer import imagen_a_base64, describir_imagen_con_groq
from utils.analisis_sentimientos import analizar_sentimiento
from config.config import bot,cargar_dataset, cargar_datos_economia
from services.groq_service import respuesta_groq, transcribir_audio_groq
from utils.nlp import buscar_mejor_respuesta, cargar_dataset
from utils.logger import logger
import os


cargar_info = cargar_datos_economia()
company_data = cargar_dataset()
learning_mode = {}

@bot.message_handler(commands=["start", "help"])
def enviar_bienvenida(message):
    texto = """
👋 ¡Hola! Soy AhorraBot 🤖, un asistente inteligente.

✅ Puedo:
• Responder mensajes de texto con información específica
• Escuchar y transcribir audios con información específica
• Leer imágenes (tickets, facturas, comprobantes)
• Realizar listas de gastos para ayudarle a administrar su dinero
• Enseñarle sobre economía y finanzas basicas para que pueda tomar las mejores decisiones posibles

📸 Solo enviame una imagen 🧾
🎤 O un audio 🎙️

Si nececita ayuda para recordar los lo que puedo hacer solo ejecute /help

Si quiere entrar en modo aprendizaje para que le enseñe algunas cosas de economía basica ejecute el siguiente comando:

/aprender: Inicia el modo aprendizaje

/salir: Sale del modo aprendizaje

Si quiere que le ayude a crear una lista con sus gastos solo ejecute los siguientes comandos:

/empezar_lista : Inicia el proceso para crear una nueva lista de compras con un presupuesto definido. 

/ver_lista: Muestra un resumen de los productos y el estado del presupuesto para una lista existente

/eliminar_lista: Inicia el proceso de borrar una lista de compras.

/estadísticas: Genera un gráfico de torta con el gastos por categoría para la lista seleccionada

/finalizar_lista: Finaliza la agregación de productos a la lista activa y muestra el resumen final

/cancelar: Cancela cualquier proceso o conversación activa (ej. creación de lista, eliminación) 

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

    respuesta = respuesta_groq(transcripcion, company_data)

    if respuesta:
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, "No pude generar una respuesta. Por favor, intenta más tarde.")


@bot.message_handler(content_types=["text"])

def manejar_texto(message):
    bot.send_chat_action(message.chat.id, "typing")
    user_text = message.text
    user_name = message.from_user.username or "Usuario"
    pregunta = message.text

    respuesta = buscar_mejor_respuesta(pregunta, company_data)
    if not respuesta:
        respuesta = respuesta_groq(pregunta, company_data)

    if respuesta:
        bot.reply_to(message, respuesta)
    else:
        bot.reply_to(message, "Lo siento, no pude procesar tu consulta. Intenta nuevamente.")

    sentimiento = analizar_sentimiento(user_text)
    logger.info(f"🧠 Análisis de sentimiento - Usuario: {user_name} | Sentimiento: {sentimiento}")

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


