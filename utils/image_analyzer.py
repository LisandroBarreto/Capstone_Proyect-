import base64
from PIL import Image
import io
import requests
from config.config import groq_client
from utils.logger import logger

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
        logger.info("🧾 Analizando imagen recibida con Groq")
        completado_chat = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Por favor, describe esta imagen de manera detallada y clara en español. Incluye todos los elementos importantes que veas en la imagen, facturas de pagos o deudas, recibos de pagos o deudas, tickets de pagos o deudas, con énfacis en los datos del lugar de origen y el destinatario del recibo juntos con su monto de dinero a pagar o ya pagado de la factura, ticket y cualquier detalle relevante que puedas observar. No utilices signos de puntuacion extraños y la estructura debe ser simple y legible"
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