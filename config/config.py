import os
import telebot
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATASET_PATH = os.path.join(os.path.dirname(__file__), "c:/Proyecto_final/Capstone_Proyect/data/data.json")
PRODUCTOS = "productos.json"


if not TELEGRAM_TOKEN:
    raise ValueError("No se encuentra el TOKEN de Telegram en el archivo .env")
if not GROQ_API_KEY:
    raise ValueError("No se encuentra el API_KEY de Groq en el archivo .env")


bot = telebot.TeleBot(TELEGRAM_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)