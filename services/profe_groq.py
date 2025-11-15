#services/profe_groq.py

from config.config import groq_client, cargar_datos_economia
from utils.logger import logger


DATOS_ECONOMIA = cargar_datos_economia()


def responder_con_groq(mensaje: str) -> str:
    try:
        logger.info(f"Consultando Groq con mensaje: {mensaje}")


        system_prompt = f"""
Eres un asistente experto en economía y finanzas básicas.
Responde ÚNICAMENTE usando la información del siguiente documento:


{DATOS_ECONOMIA}

REGLAS OBLIGATORIAS:
- Responde únicamente el fragmento relevante, NO todo el documento completo.
- Máximo 60 líneas.
- Si la respuesta supera 4000 caracteres, córtala y continúa con: "[texto reducido]" 
- No inventes información.
- Si no encuentras una sección que responda a la pregunta, responde:
  "Lo siento, esa información no está disponible en mi base de conocimientos."
- Usa emojis adecuados a la hora de responder
"""


        completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": mensaje}
        ]
    )


        return completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error Groq: {e}")
    return "Ocurrió un error procesando tu consulta."