import time
from config.config import bot
from handlers import commands  

if __name__ == "__main__":
    print("🤖 Bot de Telegram IA")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error en el bot: {e}")
            print("Reiniciando en 5 segundos...")
            time.sleep(5)