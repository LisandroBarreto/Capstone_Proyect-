import time
from config.config import bot  
import services.lista  # lista
if __name__ == "__main__":
    print("🤖 AhorraBot esta en linea...")
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(f" Error en el bot: {e}")
            print("Reiniciando en 5 segundos...")
            time.sleep(5)
