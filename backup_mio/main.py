from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from config.config import BOT_TOKEN 
from services.lista import (
    # Funciones
    empezar_lista, definir_nombre, definir_presupuesto, agregar_producto,
    ver_lista, mostrar_lista, 
    finalizar_lista, ajustar_presupuesto,
    eliminar_lista, confirmar_eliminacion, ejecutar_eliminacion,
    cancelar,

    # Constantes de Estado
    ESPERANDO_NOMBRE, ESPERANDO_PRESUPUESTO, AGREGANDO_PRODUCTO, AJUSTAR_PRESUPUESTO,
    ESPERANDO_NOMBRE_LISTA, ESPERANDO_NOMBRE_ELIMINAR, CONFIRMAR_BORRADO
)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("empezar_lista", empezar_lista),
            CommandHandler("ver_lista", ver_lista),
            CommandHandler("eliminar_lista", eliminar_lista)
        ],
        states={
            # Flujo de /empezar_lista
            ESPERANDO_NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, definir_nombre)],
            ESPERANDO_PRESUPUESTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, definir_presupuesto)],
            AGREGANDO_PRODUCTO: [
                CommandHandler("finalizar_lista", finalizar_lista),
                MessageHandler(filters.TEXT & ~filters.COMMAND, agregar_producto)
            ],
            AJUSTAR_PRESUPUESTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, ajustar_presupuesto)],
            
            # Flujo de /ver_lista
            ESPERANDO_NOMBRE_LISTA: [MessageHandler(filters.TEXT & ~filters.COMMAND, mostrar_lista)],
            
            # Flujo de /eliminar_lista
            ESPERANDO_NOMBRE_ELIMINAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmar_eliminacion)],
            CONFIRMAR_BORRADO: [MessageHandler(filters.TEXT & ~filters.COMMAND, ejecutar_eliminacion)],
        },
        fallbacks=[
            CommandHandler("finalizar_lista", finalizar_lista),
            CommandHandler("cancelar", cancelar)
        ]
    )

    app.add_handler(conv_handler)

    print("AhorraBot está en línea.")
    print("Comandos disponibles: /empezar_lista, /ver_lista, /eliminar_lista")
    app.run_polling()

if __name__ == "__main__":
    main()