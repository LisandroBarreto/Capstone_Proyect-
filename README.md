# AhorraBot, bot Financiero con NLP + Groq

Funcionalidades:
- Entender intención del usuario y analizar su estado de ánimo(Groq NLP y transformers) — añadir/eliminar/mostrar lista de compras.
- Procesar imágenes (tickets/facturas) con OCR vía Groq y extraer items, fecha, total.
- Guardar lista y gastos por usuario (JSON).
- Responder preguntas financieras (Groq).

Instalación y ejecución:
1. Actualizar el pip si no está actualizado:
   python.exe -m pip install --upgrade pip 

2. Instalar dependencias:
   pip install -r requirements.txt

3. Crear `.env` basado en `.env.example` y agregar sus claves.

4. Ejecutar:
   python main.py