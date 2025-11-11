import os
import json
import random
from transformers import pipeline
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

#  CONFIGURACIÓN DE CREDENCIALES 
TELEGRAM_TOKEN = "TELEGRAM_TOKEN" 

#  FUNCIÓN DE CARGA DE RESPUESTAS JSON 
def cargar_respuestas(ruta_archivo="respuestas.json"):
    """Carga el diccionario de respuestas desde un archivo JSON."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no se encontró.")
        return {"ERROR_CARGA": "Hubo un error interno al cargar las respuestas. Disculpa la molestia."}
    except json.JSONDecodeError:
        print(f"Error: El archivo '{ruta_archivo}' no tiene un formato JSON válido.")
        return {"ERROR_CARGA": "Hubo un error interno al cargar las respuestas. Disculpa la molestia."}

# Carga las respuestas automáticas al inicio
RESPUESTAS_AUTOMATICAS = cargar_respuestas()

MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment" # Nombre del modelo centralizado

# Carga el modelo pre-entrenado de análisis de sentimiento optimizado para español.
try:
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=MODEL_NAME, 
        tokenizer=MODEL_NAME 
    )
except Exception as e:
    print(f"Error al cargar el modelo BERT: {e}")
    sentiment_pipeline = None

#  FUNCIÓN DE CLASIFICACIÓN DE INTENCIÓN  
def clasificar_intencion_simulada(text):
    """Clasifica la intención del usuario en categorías específicas: Saludo, Despedida, Inversión, Ahorro o Deuda."""
    text_lower = text.lower()
    
    # Intención SALUDO
    saludo_keywords = ["hola", "buenos días", "buenas tardes", "que tal", "q tal"]
    if any(keyword in text_lower for keyword in saludo_keywords):
        return "SALUDO"
    
    # Intención DESPEDIDA
    despedida_keywords = ["adios", "chao", "hasta luego", "bye", "nos vemos"]
    if any(keyword in text_lower for keyword in despedida_keywords):
        return "DESPEDIDA"

    #  INTENCIONES FINANCIERAS SEGMENTADAS 
    
    # Intención INVERSION_BOLSA
    inversion_keywords = [
        "inversión", "inversion", "acciones", "bono", "mercado", "capital", 
        "invertir", "portafolio", "rentabilidad", "bolsa", "cripto", "bitcoin",
        "fondos"
    ]
    if any(keyword in text_lower for keyword in inversion_keywords):
        return "INVERSION_BOLSA"

    # Intención AHORRO_PRESUPUESTO
    ahorro_keywords = [
        "ahorrar", "ahorro", "presupuesto", "gastos", "ingreso", "egreso", 
        "cuenta", "finanzas", "financiero", "patrimonio", "dinero"
    ]
    if any(keyword in text_lower for keyword in ahorro_keywords):
        return "AHORRO_PRESUPUESTO"
        
    # Intención DEUDA_CREDITO
    deuda_keywords = [
        "crédito", "credito", "deuda", "préstamo", "prestamo", "hipoteca", 
        "tarjeta", "interés", "interes", "saldo", "cuota", "tasa", "pagar"
    ]
    if any(keyword in text_lower for keyword in deuda_keywords):
        return "DEUDA_CREDITO"
    

    # Intención PREDETERMINADA
    return "FALLBACK" 


# FUNCIÓN DE ANÁLISIS DE SENTIMIENTO
def analyze_sentiment_bert(text):
    """Analiza el sentimiento de un texto, usa el score para diferenciar intensidades y devuelve la clave de ánimo."""
    if sentiment_pipeline is None:
        return "**Error:** Modelo de Sentimiento no cargado. Revisa tu conexión o el nombre del modelo.", "ANIMO_NEUTRAL"
    
    result = sentiment_pipeline(text)[0]
    
    # Mapeo de la etiqueta a minúsculas para un manejo consistente
    raw_label = result['label'].lower() 
    score = result['score']
    
    CONFIDENCE_THRESHOLD = 0.85
    
    # Lógica de Mapeo
    if raw_label == 'positive': 
        if score > CONFIDENCE_THRESHOLD: # Muy Positivo (p. ej. score > 97%)
            classification = "Muy Positivo 🎉"
            animo_key = "ANIMO_MUY_POSITIVO"
        else: # Positivo Normal
            classification = "Positivo 😊"
            animo_key = "ANIMO_POSITIVO"
    
    elif raw_label == 'negative':
        if score > CONFIDENCE_THRESHOLD: # Muy Negativo (p. ej. score > 97%)
            classification = "Muy Negativo 😠"
            animo_key = "ANIMO_MUY_NEGATIVO"
        else: # Negativo Normal
            classification = "Negativo 😟"
            animo_key = "ANIMO_NEGATIVO"
            
    else: # 'neutral'
        classification = "Neutral 😐"
        animo_key = "ANIMO_NEUTRAL"

    # Formatea el resultado con Markdown
    sentiment_info = (
        f"**Clasificación :** {classification}\n"
        f"**Etiqueta del Modelo:** {raw_label.upper()} ({raw_label})\n"
        f"**Nivel de Confianza:** {score:.4f}"
    )
    
    return sentiment_info, animo_key


# MANEJADOR DE TEXTO DE TELEGRAM 
async def text_sentiment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja los mensajes, clasifica la intención (simulada), analiza el sentimiento y da ánimo."""
    
    user_text = update.message.text
    
    if not user_text:
        await update.message.reply_text(RESPUESTAS_AUTOMATICAS.get("FALLBACK", "Error de respuesta."))
        return
    
    await update.message.reply_text("⏳ Procesando intención y sentimiento...")

    # 1. Clasificación de Intención 
    intencion_detectada = clasificar_intencion_simulada(user_text)

    # 2. Generación de Respuesta Automática
    respuesta_data = RESPUESTAS_AUTOMATICAS.get(intencion_detectada)
    
    if isinstance(respuesta_data, list):
        respuesta_automatica = random.choice(respuesta_data)
    elif isinstance(respuesta_data, str):
        respuesta_automatica = respuesta_data
    else: 
        respuesta_automatica = RESPUESTAS_AUTOMATICAS.get("FALLBACK", "Error interno de respuesta.")
        
    # LÓGICA DE TIP FINANCIERO 
    tip_financiero = "" 
    if intencion_detectada in ["INVERSION_BOLSA", "AHORRO_PRESUPUESTO", "DEUDA_CREDITO"]:
        tips_list = RESPUESTAS_AUTOMATICAS.get("TIPS_FINANCIEROS", [])
        if tips_list and isinstance(tips_list, list):
            # Aseguramos un separador para el tip financiero
            tip_financiero = f"\n\n---\n{random.choice(tips_list)}"
        

    # 3. Análisis de Sentimiento 
    analysis_result, animo_key = analyze_sentiment_bert(user_text) 

    # 4. Generación del Mensaje de Ánimo
    animo_list = RESPUESTAS_AUTOMATICAS.get(animo_key, [])
    
    mensaje_animo = ""
    if animo_list and isinstance(animo_list, list):
        # Aseguramos un separador para el mensaje de ánimo y seleccionamos uno al azar
        mensaje_animo = f"\n\n---\n{random.choice(animo_list)}"
    

    # Primer mensaje: La respuesta automática + Tip Financiero.
    mensaje_intencion = (
        f"{respuesta_automatica}"
        f"{tip_financiero}" 
    )

    await update.message.reply_text(
        mensaje_intencion,
        parse_mode='Markdown'
    )
    
    # Segundo mensaje: El análisis de sentimiento + Mensaje de Ánimo.
    mensaje_sentimiento_completo = (
        f"🧠 **Análisis de Sentimiento:**\n"
        f"{analysis_result}"
        f"{mensaje_animo}" 
    )

    await update.message.reply_text(
        mensaje_sentimiento_completo,
        parse_mode='Markdown'
    )


#  INICIO DEL BOT 
def main():
    """Configura y ejecuta el bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Manejador principal para todos los mensajes de texto (excepto comandos).
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_sentiment_handler))

    print("🤖 Bot iniciado. Presiona Ctrl+C para detener.")
    # Ejecuta el bot. Bloquea hasta que se presione Ctrl+C.
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
