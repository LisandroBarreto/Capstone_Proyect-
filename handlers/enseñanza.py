#handlers/enseñanza.py

from config.config import bot
from services.profe_groq import responder_con_groq
from services.resumen_groq import generar_resumen_con_groq
from utils.logger import logger

en_modo_aprender = {}

RUTA_INFO = "data/tips_financieros.txt"


def cargar_contenido():
    try:
        with open(RUTA_INFO, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error al cargar archivo de economía: {e}")
        return None


@bot.message_handler(commands=["aprender"])
def activar_modo_aprender(message):
    user_id = message.from_user.id
    en_modo_aprender[user_id] = True

    contenido = cargar_contenido()

    if not contenido:
        bot.send_message(user_id, "No se pudo cargar el contenido de aprendizaje.")
        return

    resumen = generar_resumen_con_groq(contenido)

    bot.send_message(
        user_id,
        "📘 *Modo aprendizaje activado*\n\n"
        "¡Muy bien! Siempre es bueno aprender cosas nuevas.\n\n"
        "Esta es la información que puedo enseñarte:\n\n"
        f"{resumen}",
        parse_mode="Markdown"
    )


@bot.message_handler(commands=["salir"])
def salir_modo_aprender(message):
    user_id = message.from_user.id

    if user_id in en_modo_aprender:
        del en_modo_aprender[user_id]

    bot.send_message(user_id, "Has salido del modo aprendizaje. 👍")


@bot.message_handler(func=lambda m: m.from_user.id in en_modo_aprender)
def manejar_modo_aprender(message):
    user_id = message.from_user.id

    if user_id not in en_modo_aprender:
        return

    pregunta = message.text
    respuesta = responder_con_groq(pregunta)

    bot.send_message(user_id, respuesta)
