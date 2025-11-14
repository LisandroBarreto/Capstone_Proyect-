# import os
# import time
# import random
# from transformers import pipeline
# from config.config import bot, cargar_dataset
# from utils.logger import logger
# from utils.logger import log_startup_message


# MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
# RESPUESTAS = cargar_dataset()

# try:
#     sentiment_pipeline = pipeline(
#         "sentiment-analysis",
#         model=MODEL_NAME,
#         tokenizer=MODEL_NAME
#     )
#     logger.info("✅ Modelo BERT de sentimiento cargado correctamente.")
# except Exception as e:
#     logger.error(f"Error al cargar modelo de sentimiento: {e}")
#     sentiment_pipeline = None


# def analyze_sentiment_bert(text):

#     if sentiment_pipeline is None:
#         return "Error: modelo no cargado", "ANIMO_NEUTRAL"

#     result = sentiment_pipeline(text)[0]
#     raw_label = result["label"].lower()
#     score = result["score"]

#     # Clasificación general
#     if raw_label == "positive":
#         return f"Sentimiento positivo 😊 ({score:.2f})", "ANIMO_POSITIVO"
#     elif raw_label == "negative":
#         return f"Sentimiento negativo 😟 ({score:.2f})", "ANIMO_NEGATIVO"
#     else:
#         return f"Sentimiento neutral 😐 ({score:.2f})", "ANIMO_NEUTRAL"


# @bot.message_handler(content_types=["text"])
# def manejar_mensaje_texto(message):
#     user_text = message.text
#     user_id = message.from_user.id
#     user_name = message.from_user.username

#     logger.info(f"📩 Mensaje recibido de @{user_name}: {user_text}")

#     sentimiento, animo_key = analyze_sentiment_bert(user_text)

#     # 4️⃣ Mensaje de ánimo adicional
#     animo_extra = RESPUESTAS.get(animo_key, [])
#     mensaje_animo = random.choice(animo_extra) if isinstance(animo_extra, list) and animo_extra else ""

#     # 5️⃣ Enviar respuesta al usuario
#     final_message = f"🧠 {sentimiento}\n{mensaje_animo}"
#     bot.reply_to(message, final_message)

#     # 6️⃣ Notificar análisis al admin (opcional)
#     ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
#     if ADMIN_CHAT_ID:
#         try:
#             bot.send_message(
#                 ADMIN_CHAT_ID,
#                 f"🔍 *ANÁLISIS DE MENSAJE*\n👤 @{user_name} (ID: {user_id})\n💬 {user_text}\n🧠 {sentimiento}",
#                 parse_mode="Markdown"
#             )
#         except Exception as e:
#             logger.warning(f"No se pudo enviar el análisis al admin: {e}")


# if __name__ == "__main__":
#     log_startup_message()
#     print("🤖 Bot de Telegram IA con análisis de sentimiento")
#     while True:
#         try:
#             bot.polling(none_stop=True, interval=0, timeout=20)
#         except Exception as e:
#             print(f"Error en el bot: {e}")
#             time.sleep(5)


import os
import time
import random
from transformers import pipeline
from config.config import bot
from utils.logger import logger
from utils.logger import log_startup_message


# ==========================================
# 🔹 CONFIGURACIÓN DEL MODELO DE SENTIMIENTO
# ==========================================
MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

try:
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME
    )
    logger.info("✅ Modelo BERT de sentimiento cargado correctamente.")
except Exception as e:
    logger.error(f"Error al cargar modelo de sentimiento: {e}")
    sentiment_pipeline = None


# ==========================================
# 🧠 FUNCIÓN DE ANÁLISIS DE SENTIMIENTO
# ==========================================
def analyze_sentiment_bert(text):
    """Analiza el sentimiento del texto y devuelve el resultado."""
    if sentiment_pipeline is None:
        return "Error: modelo no cargado", "ANIMO_NEUTRAL"

    result = sentiment_pipeline(text)[0]
    raw_label = result["label"].lower()
    score = result["score"]

    if raw_label == "positive":
        return f"Sentimiento positivo 😊 ({score:.2f})"
    elif raw_label == "negative":
        return f"Sentimiento negativo 😟 ({score:.2f})"
    else:
        return f"Sentimiento neutral 😐 ({score:.2f})"


# ==========================================
# 💬 MANEJADOR DE MENSAJES
# ==========================================
@bot.message_handler(content_types=["text"])
def manejar_mensaje_texto(message):
    user_text = message.text
    user_name = message.from_user.username or "Usuario"

    sentimiento = analyze_sentiment_bert(user_text)

    # Notificar análisis al admin (opcional)
    ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
    logger.info(f"{sentimiento}")
    if ADMIN_CHAT_ID:
        try:
            bot.send_message(
                ADMIN_CHAT_ID,
                f"🔍 *ANÁLISIS DE MENSAJE*\n👤 @{user_name}\n💬 {user_text}\n🧠 {sentimiento}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.warning(f"No se pudo enviar el análisis al admin: {e}")


# ==========================================
# 🚀 INICIO DEL BOT
# ==========================================

log_startup_message()

if __name__ == "__main__":
    log_startup_message()
    print("🤖 Bot de Telegram IA con análisis de sentimiento")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error en el bot: {e}")
            time.sleep(5)