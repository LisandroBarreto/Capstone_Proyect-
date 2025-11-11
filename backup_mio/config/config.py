from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables del .env

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Validación 
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN' no encontrado en .env")