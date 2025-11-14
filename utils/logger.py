import logging
import os
import sys

# ==========================================================
# 🔧 CONFIGURACIÓN GLOBAL DE LOGGING
# ==========================================================

# Crear carpeta logs si no existe
if not os.path.exists("logs"):
    os.makedirs("logs")

# Archivo donde se guardarán los logs
LOG_FILE = os.path.join("logs", "bot.log")

# Formato de los mensajes de log
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configurar logging global
logging.basicConfig(
    level=logging.INFO,               # Nivel mínimo de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  # Guarda logs en archivo
        logging.StreamHandler(sys.stdout)                 # Muestra logs en consola
    ]
)

# Instancia global del logger
logger = logging.getLogger("BotLogger")

# ==========================================================
# ✅ FUNCIÓN AUXILIAR (opcional)
# ==========================================================

def log_startup_message():
    """
    Muestra un mensaje al iniciar el bot.
    """
    logger.info("🚀 BOT INICIADO CORRECTAMENTE")
    logger.info("📂 Sistema de logging activo en logs/bot.log")
