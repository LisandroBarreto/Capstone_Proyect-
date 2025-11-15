from config.config import groq_client
from utils.logger import logger

def generar_resumen_con_groq(texto: str) -> str:
    """
    Envía el documento completo a Groq y pide un resumen con títulos y subtítulos.
    """

    prompt = f"""
Eres un asistente que resume documentos de economía y finanzas.

A continuación tienes un documento completo:

======================
{texto}
======================

Quiero que generes un RESUMEN SUPER CLARO del contenido.

El resumen debe incluir:

- Un TÍTULO general
- Secciones claras con SUBTÍTULOS
- Lista de los temas principales
- Nada de texto innecesario
- NO agregues ejemplos, solo estructura

Formato solicitado:

# TÍTULO PRINCIPAL
## Tema 1
## Tema 2
## Tema 3
...

Devuélvelo EXACTAMENTE así.
"""

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            messages=[
                {"role": "system", "content": prompt}
            ]
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"Error generando resumen con Groq: {e}")
        return "No se pudo generar el resumen con Groq."