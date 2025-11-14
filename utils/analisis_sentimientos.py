from transformers import pipeline
from utils.logger import logger

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
def analizar_sentimiento(text):
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
