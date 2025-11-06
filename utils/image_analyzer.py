import os
import base64
import telebot
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import io
import requests
from config.config import TELEGRAM_TOKEN, GROQ_API_KEY

load_dotenv()


TOKEN_BOT_TELEGRAM = os.getenv('TELEGRAM_TOKEN')
CLAVE_API_GROQ = os.getenv('GROQ_API_KEY')


if not TOKEN_BOT_TELEGRAM:
    raise ValueError("TELEGRAM_BOT_TOKEN no está configurado en las variables de entorno")


if not CLAVE_API_GROQ:
    raise ValueError("GROQ_API_KEY no está configurado en las variables de entorno")


bot = telebot.TeleBot(TOKEN_BOT_TELEGRAM)
cliente_groq = Groq(api_key=CLAVE_API_GROQ)


def imagen_a_base64(ruta_o_bytes_imagen):
    try:
        if isinstance(ruta_o_bytes_imagen, bytes):
            return base64.b64encode(ruta_o_bytes_imagen).decode('utf-8')
        else:
            with open(ruta_o_bytes_imagen, "rb") as archivo_imagen:
                return base64.b64encode(archivo_imagen.read()).decode('utf-8')
            
    except Exception as e:
        print(f"Error al convertir imagen a base64: {e}")
        return None


def describir_imagen_con_groq(imagen_base64):
    try:
        completado_chat = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Por favor, describe esta imagen de manera detallada y clara en español. Incluye todos los elementos importantes que veas en la imagen, facturas de pagos o deudas, recibos de pagos o deudas, tickets de pagos o deudas, con énfacis en los datos del lugar de origen y el destinatario del recibo juntos con su monto de dinero a pagar o ya pagado de la factura, ticket y cualquier detalle relevante que puedas observar."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{imagen_base64}"
                            }
                        }
                    ]
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=1000
        )
        return completado_chat.choices[0].message.content
    
    except Exception as e:
        print(f"Error al describir imagen con Groq: {e}")
        return None