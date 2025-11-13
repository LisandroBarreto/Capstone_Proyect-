import os
import telebot
from dotenv import load_dotenv
load_dotenv()

# Tokens
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DATASET_PATH = os.path.join(os.path.dirname(__file__), "../data/data.json")
PRODUCTOS = "productos.json"

if not TELEGRAM_TOKEN:
    raise ValueError("No se encuentra TELEGRAM_TOKEN en el archivo .env")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

try:
    from groq import Groq
    if GROQ_API_KEY:
        groq_client = Groq(api_key=GROQ_API_KEY)
    else:
        groq_client = None
except ImportError:
    groq_client = None
