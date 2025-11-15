# AhorraBot, bot Financiero con NLP + Groq
# Usar python 

1. Clonar el repositorio:
   git clone https://github.com/LisandroBarreto/Capstone_Proyect-.git

2. Crear `.env` basado en `.env.example` y agregar sus claves.

3. crear entorno virtual:
   python -m venv "nombre de su entrono virtual"

4. Activa el entorno virtual:
   source "nombre de su entorno virtual"/Scripts/activate

5. Actualizar el pip si no está actualizado:
   python.exe -m pip install --upgrade pip

6. Instalar dependencias:
   pip install -r requirements.txt

7. Ejecutar en la consola:
   python main.py

FUNCIONES Y MODO DE USO:

- Entender intención del usuario y analizar su estado de ánimo(Groq NLP y transformers) 
- Procesar imágenes (tickets/facturas) con OCR vía Groq y extraer items, fecha, total.
- Guardar/añadir/eliminar/mostrar lista de y gastos por usuario mediante gráficos.
- Responder preguntas financieras (Groq).

-Para inicializar el bot ejecute:

/start

-Siquiere recordar los comandos del bot solo ejecute:

/help

-Si quiere entrar en modo aprendizaje para que le enseñe algunas cosas de economía basica ejecute el siguiente comando:

/aprender: Inicia el modo aprendizaje

/salir: Sale del modo aprendizaje

-Si quiere que le ayude a crear una lista con sus gastos solo ejecute los siguientes comandos:

/empezar_lista : Inicia el proceso para crear una nueva lista de compras con un presupuesto definido. 

/ver_lista: Muestra un resumen de los productos y el estado del presupuesto para una lista existente

/eliminar_lista: Inicia el proceso de borrar una lista de compras.

/estadísticas: Genera un gráfico de torta con el gastos por categoría para la lista seleccionada

/finalizar_lista: Finaliza la agregación de productos a la lista activa y muestra el resumen final

/cancelar: Cancela cualquier proceso o conversación activa (ej. creación de lista, eliminación) 


--PRUEBA DEL BOT:

Principal

1. Salude al bot

2. Digale que esta endeudado o que tiene problemas economicos 

3. Preguntale que puede hacer

4. Enviale una imagen de una factura, recibo o ticket.


Uso de la Función Lista
La gestión de listas se realiza a través de un flujo de conversación guiado.

1. Crear y Establecer Presupuesto
Usa el comando /empezar_lista.

El bot te pedirá el nombre de la lista (ej: "semana", "vacaciones", etc).

Luego, te pedirá el presupuesto máximo (solo números, ej: 15000).

2. Agregar Productos
Una vez que el presupuesto esté definido, el bot entrará en modo de agragar productos.

Formato de entrada: Escribe el nombre del producto seguido de su precio (sin el símbolo $).

Ejemplo: arroz 2500

El bot clasificará automáticamente el producto por Tipo (Esencial, No Esencial, Intermedio) y Categoría para el análisis.

3. Ajuste por Exceso de Presupuesto
Si el total de tus gastos supera el presupuesto establecido, el bot te notificará y te ofrecerá eliminar productos clasificados como 'No Esenciales' para ayudarte a ajustar el gasto.

Para eliminar un producto sugerido, escribe su nombre exacto.

Para continuar sin eliminar, escribe no.

4. Finalizar
Cuando termines de agregar productos, usa /finalizar_lista para cerrar la lista y ver un resumen final. El bot te preguntará si deseas generar el gráfico de estadísticas.


Uso del modo aprendizaje:

1. Activar el modo aprendizaje
Usa el comando /aprender. Le va a dar algunas opciones de temas económicos. 

2. Debe escribir el tema que le interesaria aprender. Puede elegir otro cuando termine de explicar el primero.

3. Finalizar el modo aprendizaje.
Use el comando /salir para terminar el modo aprendizaje y repetir otras funciones. 

