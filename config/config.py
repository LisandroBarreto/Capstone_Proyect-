# config/config

import json
import os
import telebot
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# Tokens
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DATOS_RESPUESTAS= os.path.join(os.path.dirname(__file__), "c:/Proyecto_final/Capstone_Proyect/data/data.json")
DATOS_ECONOMIA = os.path.join(os.path.dirname(__file__), "c:/Proyecto_final/Capstone_Proyect/data/tips_financieros.txt")



if not TELEGRAM_TOKEN:
    raise ValueError("❌No se encuentra TELEGRAM_TOKEN en el archivo .env")
if not GROQ_API_KEY:
    raise ValueError("❌ No se encuentra GROQ_API_KEY en el archivo .env")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

def cargar_datos_economia():
    try:
        with open(DATOS_ECONOMIA, "r", encoding="utf-8-sig") as f:
            return f.read()
        
    except Exception as e:
        print(f"Error al cargar DATOS_ECONOMIA: {e}")
        return None



def cargar_dataset():
    try:
        with open(DATOS_RESPUESTAS, "r", encoding="utf-8") as f:
            return json.load(f)
        
    except Exception as e:
        print(f"Error al cargar DATASET_PATH: {e}")
        return None