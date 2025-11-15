#utils/logger.py

import logging
import os
import sys


if not os.path.exists("logs"):
    os.makedirs("logs")


LOG_FILE = os.path.join("logs", "bot.log")


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)


logger = logging.getLogger("BotLogger")


def log_startup_message():
    """
    Muestra un mensaje al iniciar el bot.
    """
    logger.info("🚀 BOT INICIADO CORRECTAMENTE")
    logger.info("📂 Sistema de logging activo en logs/bot.log")
