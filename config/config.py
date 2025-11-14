# config.config

import json
import os
import telebot
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATASET_PATH = os.path.join(os.path.dirname(__file__), "c:/Proyecto_final/Capstone_Proyect/data/data.json")
RESPUESTAS = os.path.join(os.path.dirname(__file__), "c:/Proyecto_final/Capstone_Proyect/data/respuestas.json")


if not TELEGRAM_TOKEN:
    raise ValueError("No se encuentra el TOKEN de Telegram en el archivo .env")
if not GROQ_API_KEY:
    raise ValueError("No se encuentra el API_KEY de Groq en el archivo .env")


bot = telebot.TeleBot(TELEGRAM_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)


def cargar_dataset():
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    
        respuestas = {}
        for item in data:
            for p in item["prompt"]:
                respuestas[p.lower()] = item["respuesta"]
                return respuestas

    except Exception as e:
        print(f"Error al cargar el dataset: {e}")
        return None