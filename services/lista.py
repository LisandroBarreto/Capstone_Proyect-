import io
import matplotlib.pyplot as plt
import telebot
from telebot.types import Message 
from config.config import bot
# Estados 
(
    ESPERANDO_NOMBRE,
    ESPERANDO_PRESUPUESTO,
    AGREGANDO_PRODUCTO,
    AJUSTAR_PRESUPUESTO
) = range(4)

ESPERANDO_NOMBRE_LISTA = "ESPERANDO_NOMBRE_LISTA"
ESPERANDO_NOMBRE_ELIMINAR = "ESPERANDO_NOMBRE_ELIMINAR"
CONFIRMAR_BORRADO = "CONFIRMAR_BORRADO"
ESPERANDO_NOMBRE_ESTADISTICAS = "ESPERANDO_NOMBRE_ESTADISTICAS"
ESPERANDO_CONFIRMACION_GRAFICO = "ESPERANDO_CONFIRMACION_GRAFICO"

# Lista de productos esenciales
Esenciales = [
    # Alimentos básicos
    "leche", "pan", "huevos", "arroz", "fideos", "pollo", "carne", "cerdo", "pescado",
    "verdura", "fruta", "aceite", "azucar", "sal", "harina", "legumbre", "cereal",
    "yogur", "queso", "queso fresco", "queso rallado", "queso crema",
    "yogur natural", "yogur con frutas", "pan integral", "pan blanco",
    "aceite de oliva", "aceite vegetal", "harina de trigo", "harina integral",
    "papa", "tomate", "zanahoria", "lechuga", "cebolla", "ajo", "espinaca", "brocoli",
    "manzana", "banana", "naranja", "calabaza", "limon", "pera", "uva",
    # Higiene y limpieza esencial
    "toalla higienica", "toalla higienica nocturna", "pañal", "pañales",
    "jabón", "jabon liquido", "jabon en barra", "shampoo", "detergente",
    "papel higienico", "suavizante de ropa", "detergente en polvo", "detergente para ropa liquido",
    "limpiador multiusos", "limpiador de vidrios", "limpiador de baños", "limpiador de pisos",
    "limpiador de cocina", "esponja de cocina", "jabón para platos",
    # Salud
    "paracetamol", "ibuprofeno", "aspirina", "antibiotico", "alcohol en gel",
    "alcohol isopropilico", "curitas", "vendas", "termometro", "mascarilla quirurgica",
    "guantes de latex", "guantes de nitrilo", "desinfectante de superficies",
    "repelente de insectos", "insecticida",
    # Servicios básicos
    "luz", "electricidad", "agua", "gas", "alquiler", "renta", "impuesto", "expensas",
    "internet", "wi-fi", "telefono", "colectivo", "subte", "transporte", "nafta", "gasolina",
    "seguro medico", "prepaga", "obra social", "medicina prepaga"
]

# Lista de productos intermedios
intermedios = [
    # Alimentos y bebidas adicionales

    "cafe", "te", "miel", "mermelada", "mayonesa", "mostaza", "ketchup", "agua mineral", "frutos secos",
    # Productos de cuidado persona,  maquillaje basico  y productos de higiene personal
    "crema hidratante", "crema solar", "protector solar", "protector labial", "labial",
    "delineador", "mascara de pestañas", "base de maquillaje", "polvo compacto",
    "rubor", "sombra de ojos", "perfume", "desodorante corporal", "antitranspirante",
    "crema antiarrugas", "jabón facial", "tonico facial", "exfoliante facial",
    "mascarilla facial", "shampoo", "acondicionador",  "cepillo de dientes", "dentrifico", "hilo dental", "enjuague bucal", "desodorante",
    "shampoo anticaspa", "tratamiento capilar", "serum capilar",
    "protector térmico", "gel fijador", "cera para el cabello",
    # Ropa y accesorios básicos
    "camiseta", "pantalón", "jean", "zapatos", "sandalias", "medias", "ropa interior", "buzo", "camisa",
    "chaqueta", "abrigo", "bufanda", "guantes", "gorro",
    "reloj", "bolso", "mochila", "tetera eléctrica", "cafetera", "licuadora", "batidora",
    "plancha para ropa", "secador de pelo", "rizador de pelo", "aspiradora", "ventilador",
    "calefactor", "plancha para pelo", "tostadora", "microondas", "horno eléctrico",
    "ropa deportiva", "zapatillas deportivas", "sábana", "toalla", "frazada", "almohada", "colchón",
    "agenda", "cuaderno", "lápiz", "bolígrafo", "marcador", "resaltador", "carpeta", "calculadora",
    "libro", "novela", "biografía", "cómic", "revista", "manga", "libro de cocina",
    "ollas", "sartenes", "cubiertos",
    "memoria usb", "disco duro externo", "tarjeta de memoria", "cargador portátil", "audífonos", "bocina bluetooth",
    "pesas", "colchoneta de yoga", "cuerda para saltar", "balón de fútbol", "balón de baloncesto",
    "raqueta de tenis", "pelota de tenis", "gafas de natación", "traje de baño",
    "toalla de playa", "sombrilla de playa", "silla de playa", "nevera portátil", "linterna", "brújula",
    "plan celular", "plan de datos", "servicio de streaming básico"
]

# Lista de productos no esenciales
no_esenciales = [
    #Bedidas azucaradas y dulces/salados
    "gaseosa", "dulce", "golosina", "helado", "galletita", "chocolate", "postre", "papitas", "Mani", "Chizitos", "Pochoclos",
    "cerveza", "vino", "licor", "fernet", "vino caro",
    #Accesorios 
    "collar", "pulsera", "aretes", "anillo", "aritos", "reloj de lujo", "gafas de sol", "decoración", "perfume de lujo",
    # Tecnología y entretenimiento
    "celular", "smartphone", "auriculares", "bocina portátil", "tablet", "laptop", "computadora", "monitor",
    "televisor", "consola de videojuegos", "juego de computadora", "aplicación",
    "videojuego", "consola de videojuegos", "playstation", "smartwatch", "dron",
    "cámara fotográfica", "cámara de video", "notebook gamer", "bocina profesional",  "proyector",
    # juguetes 
    "juego de mesa", "rompecabezas", "muñeca", "auto a control remoto", "pelota", "bicicleta",
    "patineta", "skateboard",
    #  deco hogar 
    "muebles", "cuadro", "alfombra", "lámpara", "cortina",  "adornos", "plantas decorativas",
    "cubiertos", "mantel ", "jarrón decorativo",
    # Entrenamiento y ocio
    "netflix", "spotify", "disney+", "hbo", "amazon prime", "star+", "kick", "twitch", "steam",
    "tatuaje", "piercing", "microblading", "botox", "relleno facial", "tratamiento láser",
    "extensiones de pestañas", "spa",
    "smart TV", "smartwatch premium"
]

# Diccionario de categorías principales y sus productos 
CATEGORIAS_PRINCIPALES = {
    "Alimentos": [
        "leche", "pan", "huevos", "arroz", "fideos", "pollo", "carne", "cerdo", "pescado",
        "verdura", "fruta", "aceite", "azucar", "sal", "harina", "legumbre", "cereal",
        "yogur", "queso", "yogur natural", "pan integral", "pan blanco",
        "aceite de oliva", "aceite vegetal", "harina de trigo", "harina integral",
        "papa", "tomate", "zanahoria", "lechuga", "cebolla", "ajo", "espinaca", "brocoli",
        "manzana", "banana", "naranja", "calabaza", "limon", "pera", "uva",
        "cafe", "te", "miel", "mermelada", "mayonesa", "mostaza", "ketchup", "agua mineral", "frutos secos",
        "gaseosa", "dulce", "golosina", "helado", "galletita", "chocolate", "postre", "papitas", "mani", "chizitos", "pochoclos",
        "cerveza", "vino", "licor", "fernet", "vino caro"
    ],
    "Hogar y Limpieza": [
        "detergente", "papel higienico", "suavizante de ropa", "detergente en polvo", "detergente para ropa liquido",
        "limpiador multiusos", "limpiador de vidrios", "limpiador de baños", "limpiador de pisos",
        "limpiador de cocina", "esponja de cocina", "jabón para platos",
        "ollas", "sartenes", "cubiertos", "tetera eléctrica", "cafetera", "licuadora", "batidora",
        "plancha para ropa", "aspiradora", "ventilador", "calefactor", "tostadora", "microondas", "horno eléctrico",
        "sábana", "toalla", "frazada", "almohada", "colchón",
        "muebles", "cuadro", "alfombra", "lámpara", "cortina", "adornos", "plantas decorativas",
        "jarrón decorativo"
    ],
    "Higiene Personal y Salud": [
        "toalla higienica", "toalla higienica nocturna", "pañal", "pañales",
        "jabón", "jabon liquido", "jabon en barra", "shampoo", "cepillo de dientes", "dentrifico", "hilo dental", "enjuague bucal", "desodorante",
        "shampoo anticaspa", "tratamiento capilar", "serum capilar",
        "protector térmico", "gel fijador", "cera para el cabello",
        "crema hidratante", "crema solar", "protector solar", "protector labial", "labial",
        "delineador", "mascara de pestañas", "base de maquillaje", "polvo compacto",
        "rubor", "sombra de ojos", "perfume", "desodorante corporal", "antitranspirante",
        "crema antiarrugas", "jabón facial", "tonico facial", "exfoliante facial",
        "mascarilla facial", "secador de pelo", "rizador de pelo", "plancha para pelo",
        "paracetamol", "ibuprofeno", "aspirina", "antibiotico", "alcohol en gel",
        "alcohol isopropilico", "curitas", "vendas", "termometro", "mascarilla quirurgica",
        "guantes de latex", "guantes de nitrilo", "desinfectante de superficies",
        "repelente de insectos", "insecticida",
        "tatuaje", "piercing", "microblading", "botox", "relleno facial", "tratamiento láser",
        "extensiones de pestañas", "spa", "perfume de lujo"
    ],
    "Transporte y Servicios": [
        "luz", "electricidad", "agua", "gas", "alquiler", "renta", "impuesto", "expensas",
        "internet", "wi-fi", "telefono", "colectivo", "subte", "transporte", "nafta", "gasolina",
        "seguro medico", "prepaga", "obra social", "medicina prepaga",
        "plan celular", "plan de datos", "servicio de streaming básico"
    ],
    "Ropa y Accesorios": [
        "camiseta", "pantalón", "jean", "zapatos", "sandalias", "medias", "ropa interior", "buzo", "camisa",
        "chaqueta", "abrigo", "bufanda", "guantes", "gorro",
        "ropa deportiva", "zapatillas deportivas",
        "reloj", "bolso", "mochila",
        "collar", "pulsera", "aretes", "anillo", "aritos", "reloj de lujo", "gafas de sol"
    ],
    "Tecnología y Entretenimiento": [
        "memoria usb", "disco duro externo", "tarjeta de memoria", "cargador portátil", "audífonos", "bocina bluetooth",
        "celular", "smartphone", "auriculares", "bocina portátil", "tablet", "laptop", "computadora", "monitor",
        "televisor", "consola de videojuegos", "juego de computadora", "aplicación",
        "videojuego", "consola de videojuegos", "playstation", "smartwatch", "dron",
        "cámara fotográfica", "cámara de video", "notebook gamer", "bocina profesional",  "proyector",
        "netflix", "spotify", "disney+", "hbo", "amazon prime", "star+", "kick", "twitch", "steam",
        "smart TV", "smartwatch premium"
    ],
    "Ocio y Varios": [
        "pesas", "colchoneta de yoga", "cuerda para saltar", "balón de fútbol", "balón de baloncesto",
        "raqueta de tenis", "pelota de tenis", "gafas de natación", "traje de baño",
        "toalla de playa", "sombrilla de playa", "silla de playa", "nevera portátil", "linterna", "brújula",
        "agenda", "cuaderno", "lápiz", "bolígrafo", "marcador", "resaltador", "carpeta", "calculadora",
        "libro", "novela", "biografía", "cómic", "revista", "manga", "libro de cocina",
        "juego de mesa", "rompecabezas", "muñeca", "auto a control remoto", "pelota", "bicicleta",
        "patineta", "skateboard", "decoración"
    ]
}

user_context = {}

def set_user_context(user_id, key, value):
    """funcion que guarda un valor en el contexto del usuario."""
    if user_id not in user_context:
        user_context[user_id] = {}
    user_context[user_id][key] = value

def get_user_context(user_id, key, default=None, pop=False):
    """funcion que obtiene un valor del contexto del usuario."""
    if user_id not in user_context:
        return default
    if pop:
        return user_context[user_id].pop(key, default)
    return user_context[user_id].get(key, default)

def clear_user_context(user_id=None, key=None):
    """funcion que limpia el contexto del usuario."""
    if user_id is None:
        user_context.clear()
    elif key is None:
        user_context.pop(user_id, None)
    else:
        if user_id in user_context:
            user_context[user_id].pop(key, None)

# Listas del usuario
listas_usuarios = {}

def _enviar_grafico_estadisticas(message: Message, nombre_lista):
    """
    Funcion para generar y enviar el gráfico de estadísticas de la lista.
    """
    user_id = message.from_user.id
    if user_id not in listas_usuarios or nombre_lista not in listas_usuarios[user_id]:
        bot.reply_to(message, "No existe una lista con ese nombre para realizar el gráfico.")
        return

    data = listas_usuarios[user_id][nombre_lista]
    if not data["items"]:
        bot.reply_to(message, f"La lista '{nombre_lista}' está vacía. No se puede generar un gráfico.")
        return

    gastos_por_categoria = {}
    for item in data["items"]:
        categoria = item.get("categoria", "Otros")
        if categoria == "Sin Categoría":
            categoria = "Otros"
        gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0) + item["monto"]

    categorias = list(gastos_por_categoria.keys())
    montos = list(gastos_por_categoria.values())

    fig, ax = plt.subplots(figsize=(8, 8))
    colores = plt.cm.Paired(range(len(categorias)))

    ax.pie(
        montos,
        labels=categorias,
        autopct=lambda p: f'${sum(montos) * p / 100.0:,.0f}\n({p:.1f}%)' if p > 3 else '',
        startangle=90,
        colors=colores,
        pctdistance=0.75
    )

    ax.axis('equal')
    ax.set_title(f"Gastos por Categoría en '{nombre_lista}'\nTotal: ${data['total']:,.0f}", fontsize=14, weight='bold')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.5, facecolor='white')
    buf.seek(0)
    plt.close(fig)

    bot.send_photo(message.chat.id, photo=buf, caption=f"Resumen gráfico de tu lista '{nombre_lista}'")

def _clasificar_producto(nombre_producto):
    '''
    funcion para clasificar un producto en esencial, no esencial o intermedio
    '''
    nombre_lower = nombre_producto.lower()
    tipo = "intermedio"
    if any(p in nombre_lower for p in no_esenciales):
        tipo = "no esencial"
    elif any(p in nombre_lower for p in Esenciales):
        tipo = "esencial"
    elif any(p in nombre_lower for p in intermedios):
        tipo = "intermedio"

    categoria = "Otros"
    for cat, items in CATEGORIAS_PRINCIPALES.items():
        if any(prod_item in nombre_lower for prod_item in items):
            categoria = cat
            break
    return {"tipo": tipo, "categoria": categoria}

# --- FLUJO: CREAR LISTA ---

@bot.message_handler(commands=['empezar_lista'])
def empezar_lista(message: Message):
    '''
    Funcion para iniciar la creación de una nueva lista de compras.
    '''
    user_id = message.from_user.id
    listas_usuarios.setdefault(user_id, {})

    if len(listas_usuarios[user_id]) >= 2:
        bot.reply_to(message, "Ya tenés dos listas activas. Usá /eliminar_lista si querés crear una nueva.")
        return

    bot.reply_to(message, "Escribí un nombre para esta lista (por ejemplo 'semana' o 'mes'):")
    bot.register_next_step_handler(message, definir_nombre)


def definir_nombre(message: Message):
    '''
    Funcion que define el nombre de la lista y verifica que no exista ya.
    '''
    user_id = message.from_user.id
    nombre_lista = message.text.strip().lower()

    if nombre_lista in listas_usuarios[user_id]:
        bot.reply_to(message, "Ya existe una lista con ese nombre. Elegí otro.")
        bot.register_next_step_handler(message, definir_nombre) 
        return

    listas_usuarios[user_id][nombre_lista] = {"presupuesto": 0, "total": 0, "items": []}
    set_user_context(user_id, "lista_activa", nombre_lista) 
    
    bot.reply_to(message, f"Perfecto. La lista '{nombre_lista}' fue creada. ¿Cuál es tu presupuesto máximo?")
    bot.register_next_step_handler(message, definir_presupuesto)


def definir_presupuesto(message: Message):
    '''
    funcion que define el presupuesto máximo para la lista.
    '''
    user_id = message.from_user.id
    nombre_lista = get_user_context(user_id, "lista_activa")

    try:
        presupuesto = int(message.text)
        if presupuesto <= 0:
            bot.reply_to(message, "El presupuesto debe ser un número positivo.")
            bot.register_next_step_handler(message, definir_presupuesto) 
            return
        
        listas_usuarios[user_id][nombre_lista]["presupuesto"] = presupuesto
        bot.reply_to(message, f"Presupuesto de ${presupuesto} establecido para '{nombre_lista}'.\n"
                                 "Agregá tus productos (ej: arroz 2500).\n"
                                 "Cuando termines, usá /finalizar_lista.")
        bot.register_next_step_handler(message, agregar_producto)
    except (ValueError, TypeError):
        bot.reply_to(message, "Ingresá un número válido para el presupuesto.")
        bot.register_next_step_handler(message, definir_presupuesto)


def agregar_producto(message: Message):
    '''
    Funcion para agregar productos a la lista.
    '''
    user_id = message.from_user.id
    nombre_lista = get_user_context(user_id, "lista_activa")
    
    if message.text.strip().lower() == '/finalizar_lista':
        return finalizar_lista(message) # Llamamos a la función /finalizar_lista
    if message.text.strip().lower() == '/cancelar':
        return cancelar(message) # Llamamos a la función /cancelar

    if not nombre_lista or nombre_lista not in listas_usuarios.get(user_id, {}):
        bot.reply_to(message, "Hubo un error, no encuentro tu lista activa. Empezá de nuevo con /empezar_lista.")
        return 

    mensaje = message.text.lower().strip()
    partes = mensaje.split()

    if len(partes) < 2:
        bot.reply_to(message, "El formato es incorrecto. Usá: producto precio (ej. harina 1500)")
        bot.register_next_step_handler(message, agregar_producto) 
        return

    try:
        monto = int(partes[-1])
        nombre = " ".join(partes[:-1])
        if monto <= 0:
            bot.reply_to(message, "El monto debe ser un número positivo.")
            bot.register_next_step_handler(message, agregar_producto)
            return
    except ValueError:
        bot.reply_to(message, "El monto debe ser un número válido al final.")
        bot.register_next_step_handler(message, agregar_producto)
        return

    data = listas_usuarios[user_id][nombre_lista]
    
    clasificacion = _clasificar_producto(nombre)
    data["items"].append({
        "nombre": nombre, 
        "monto": monto, 
        "tipo": clasificacion["tipo"], 
        "categoria": clasificacion["categoria"] 
    })
    
    data["total"] += monto

    presupuesto = data["presupuesto"]
    total = data["total"]
    
    mensaje_respuesta = f"Agregado: {nombre} (${monto}) - {clasificacion['tipo']} / Cat: {clasificacion['categoria']}\n"
    mensaje_respuesta += f"Total: ${total} / ${presupuesto}\n"

    tipo_producto = clasificacion["tipo"] 
    if total > presupuesto:
        mensaje_respuesta += "\n ¡Te pasaste del presupuesto!"
        productos_no_esenciales = [item for item in data["items"] if item["tipo"] == "no esencial"]

        if productos_no_esenciales:
            productos_texto = "\n".join(f"• {item['nombre']} (${item['monto']})" for item in productos_no_esenciales)
            mensaje_respuesta += (
                f"\nTenés estos productos no esenciales en tu lista:\n{productos_texto}\n\n"
                "Escribí el nombre exacto del producto que querés eliminar o escribí 'no' para mantenerlo."
            )
            set_user_context(user_id, "productos_no_esenciales", productos_no_esenciales)
            bot.reply_to(message, mensaje_respuesta, parse_mode="Markdown")
            bot.register_next_step_handler(message, ajustar_presupuesto)
            return
        else:
            mensaje_respuesta += "\n No tenés productos no esenciales en tu lista para recortar fácilmente."
            bot.reply_to(message, mensaje_respuesta, parse_mode="Markdown")
            bot.register_next_step_handler(message, agregar_producto) # Sigue agregando
            return

    elif total >= presupuesto * 0.9:
        mensaje_respuesta += "Estás cerca del límite."
    elif tipo_producto == "no esencial":
        mensaje_respuesta += f"(Recordá que '{nombre}' es no esencial)"

    bot.reply_to(message, mensaje_respuesta, parse_mode="Markdown")
    bot.register_next_step_handler(message, agregar_producto) # Sigue agregando


def ajustar_presupuesto(message: Message):
    '''
    Funcion para ajustar la lista si el usuario se excede del presupuesto.
    '''
    user_id = message.from_user.id
    nombre_lista = get_user_context(user_id, "lista_activa")
    respuesta = message.text.lower().strip()
    data = listas_usuarios[user_id][nombre_lista]

    if respuesta == "no":
        bot.reply_to(message, "OK. Mantenemos los productos, but seguís excedido. Podés agregar más o usar /finalizar_lista.")
        bot.register_next_step_handler(message, agregar_producto)
        return

    productos_no_esenciales = get_user_context(user_id, "productos_no_esenciales", [])
    item_a_eliminar = next((item for item in productos_no_esenciales if item["nombre"] == respuesta), None)

    if item_a_eliminar:
        data["items"].remove(item_a_eliminar)
        data["total"] = sum(i["monto"] for i in data["items"])
        
        bot.reply_to(message,
            f"'{respuesta}' fue eliminado. Nuevo total: ${data['total']} / ${data['presupuesto']}"
        )
        # Actualizamos la lista de no esenciales en contexto
        productos_actualizados = [item for item in data["items"] if item["tipo"] == "no esencial"]
        set_user_context(user_id, "productos_no_esenciales", productos_actualizados)

    else:
        bot.reply_to(message, "No encontré ese producto en tu lista de 'no esenciales'. Escribí el nombre exacto o 'no'.")
        bot.register_next_step_handler(message, ajustar_presupuesto) 
        return

    # Verificamos si sigue excediendo el presupuesto
    if data["total"] > data["presupuesto"]:
        productos_no_esenciales_actuales = get_user_context(user_id, "productos_no_esenciales", [])
        if productos_no_esenciales_actuales:
            productos_texto = "\n".join(f"• {item['nombre']} (${item['monto']})" for item in productos_no_esenciales_actuales)
            bot.reply_to(message,
                f"Aún superás el presupuesto. ¿Querés eliminar otro?\n{productos_texto}\n(Escribí el nombre o 'no')"
            )
            bot.register_next_step_handler(message, ajustar_presupuesto)
            return
        else:
            bot.reply_to(message, "Ya no quedan más productos no esenciales. Seguís excedido. Podés /finalizar_lista o agregar otro producto.")
            bot.register_next_step_handler(message, agregar_producto)
            return
    
    bot.reply_to(message,
        "Perfecto. Ya estás dentro del presupuesto.\nSeguí agregando productos o usá /finalizar_lista."
    )
    bot.register_next_step_handler(message, agregar_producto)


# --- FLUJO: VER LISTA ---

@bot.message_handler(commands=['ver_lista'])
def ver_lista(message: Message):
    '''
    Funcion que iniciar el proceso para ver una lista existente.
    '''
    user_id = message.from_user.id

    if user_id not in listas_usuarios or not listas_usuarios[user_id]:
        bot.reply_to(message, "No tenés listas activas. Creá una con /empezar_lista.")
        return

    nombres = list(listas_usuarios[user_id].keys())
    
    if len(nombres) == 1:
        bot.reply_to(message, f"Tenés una lista llamada: '{nombres[0]}'. Escribí su nombre para verla.")
    else:
        texto = "Tus listas activas:\n" + "\n".join(f"• {n}" for n in nombres)
        texto += "\n\nEscribí el nombre de la lista que querés ver."
        bot.reply_to(message, texto)

    bot.register_next_step_handler(message, mostrar_lista)

def mostrar_lista(message: Message):
    """
    Muestra el resumen de la lista Y preguntA por el gráfico.
    """
    user_id = message.from_user.id
    nombre_lista = message.text.strip().lower()

    if user_id not in listas_usuarios or nombre_lista not in listas_usuarios[user_id]:
        bot.reply_to(message, "No existe una lista con ese nombre.")
        return

    data = listas_usuarios[user_id][nombre_lista]
    
    if not data["items"]:
        resumen = "La lista está vacía."
    else:
        resumen = "\n".join([
            f"• {i['nombre']} (${i['monto']}) - {i['tipo']} / Cat: {i.get('categoria', 'Otros')}" 
            for i in data["items"]
        ])

    total = data["total"]
    presupuesto = data["presupuesto"]
    restante = presupuesto - total

    mensaje = (f"{nombre_lista.upper()}:\n\n{resumen}\n\n"
               f"Total gastado: ${total}\n"
               f"Presupuesto: ${presupuesto}\n")
    
    if total > presupuesto:
        mensaje += f"Estás ${total - presupuesto} por encima del presupuesto."
    else:
        mensaje += f"Te sobran: ${restante}"

    bot.reply_to(message, mensaje, parse_mode="Markdown")
    
    if data["items"]:
        set_user_context(user_id, "lista_para_grafico", nombre_lista)
        bot.reply_to(message, " ¿Querés ver un gráfico de gastos por categoría? (sí/no)")
        bot.register_next_step_handler(message, manejar_confirmacion_grafico)
    
# --- FLUJO: FINALIZAR LISTA (COMANDO) ---

@bot.message_handler(commands=['finalizar_lista'])
def finalizar_lista(message: Message):
    """
    Finaliza , muestra resumen Y preguntapor el gráfico.
    (Usado por /finalizar_lista)
    """
    user_id = message.from_user.id
    nombre_lista = get_user_context(user_id, "lista_activa") 

    if not nombre_lista or nombre_lista not in listas_usuarios.get(user_id, {}):
        bot.reply_to(message, "No tenés una lista activa para finalizar.")
        return

    # resumen 
    data = listas_usuarios[user_id][nombre_lista]
    if not data["items"]:
        resumen = "La lista está vacía."
    else:
        resumen = "\n".join([f"• {i['nombre']} (${i['monto']}) - {i['tipo']} / Cat: {i.get('categoria', 'Otros')}" for i in data["items"]])

    total = data["total"]
    presupuesto = data["presupuesto"]
    restante = presupuesto - total
    mensaje = (f"Resumen de {nombre_lista.upper()}:\n\n{resumen}\n\n"
               f"Total gastado: ${total} / ${presupuesto}\n")
    if total > presupuesto:
        mensaje += f"Estás ${total - presupuesto} por encima."
    else:
        mensaje += f"Te sobran: ${restante}"
    
    bot.reply_to(message, mensaje, parse_mode="Markdown")

    if data["items"]:
        # Se guarda la lista que se quiere graficar
        set_user_context(user_id, "lista_para_grafico", nombre_lista)
        clear_user_context(user_id, "lista_activa") 
        
        bot.reply_to(message, f"Lista '{nombre_lista}' guardada. \n📊 ¿Querés ver el gráfico de gastos? (sí/no)")
        bot.register_next_step_handler(message, manejar_confirmacion_grafico)
        return
    
    clear_user_context(user_id, "lista_activa") 
    bot.reply_to(message, f"Lista '{nombre_lista}' guardada (vacía).")

# FLUJO: grafico  /ver_lista y /finalizar_lista

def manejar_confirmacion_grafico(message: Message):
    """
    Funcion que maneja el si o no para realizar el grafico
    """
    respuesta = message.text.strip().lower()
    user_id = message.from_user.id
    
    nombre_lista = get_user_context(user_id, "lista_para_grafico", pop=True) # Obtenemos y limpiamos

    if respuesta == "sí" or respuesta == "si":
        if nombre_lista:
            bot.reply_to(message, "Perfecto, espera un segundo mientras te genero el gráfico...")
            _enviar_grafico_estadisticas(message, nombre_lista)
        else:
            bot.reply_to(message, "Hubo un error, no encontré qué lista graficar.")
    else:
        bot.reply_to(message, "Entiendo. No se generará el gráfico.")
    
    clear_user_context(user_id)

# FLUJO:eliminar lista

@bot.message_handler(commands=['eliminar_lista'])
def eliminar_lista(message: Message):
    '''
    Funcion que inicia el proceso para eliminar una lista.
    '''
    user_id = message.from_user.id
    if user_id not in listas_usuarios or not listas_usuarios[user_id]:
        bot.reply_to(message, "No tenés listas activas para eliminar.")
        return

    nombres = list(listas_usuarios[user_id].keys())
    texto = "Tus listas activas:\n" + "\n".join(f"• {n}" for n in nombres)
    texto += "\n\nEscribí el nombre de la lista que querés eliminar."
    bot.reply_to(message, texto, parse_mode="Markdown")
    bot.register_next_step_handler(message, confirmar_eliminacion)


def confirmar_eliminacion(message: Message):
    """
    Fucnion que pide confirmar antes de borrar.
    """
    user_id = message.from_user.id
    nombre_lista = message.text.strip().lower()

    if nombre_lista not in listas_usuarios.get(user_id, {}):
        bot.reply_to(message, "No existe esa lista. Volvé a empezar con /eliminar_lista si querés.")
        return

    set_user_context(user_id, "lista_a_borrar", nombre_lista)
    bot.reply_to(message,
        f"¿Seguro que querés eliminar la lista '{nombre_lista}' para siempre? (sí/no)"
    )
    bot.register_next_step_handler(message, ejecutar_eliminacion)


def ejecutar_eliminacion(message: Message):
    """
    Funcion que elimina la lista si el usuario dice 'sí'.
    """
    user_id = message.from_user.id
    respuesta = message.text.strip().lower()
    nombre_lista = get_user_context(user_id, "lista_a_borrar", pop=True) # Obtenemos y limpiamos

    if respuesta == "sí": # con tilde
        if nombre_lista and nombre_lista in listas_usuarios.get(user_id, {}):
            listas_usuarios[user_id].pop(nombre_lista)
            bot.reply_to(message, f"Listo. La lista '{nombre_lista}' fue eliminada.")
        else:
            bot.reply_to(message, "Error, no encontré la lista para borrar.")
    else:
        bot.reply_to(message, "Cancelado. Tu lista está a salvo.")

    clear_user_context(user_id)


# FLUJO: esatdisticas 

@bot.message_handler(commands=['estadisticas'])
def estadisticas_lista(message: Message):
    """
    Fucion que iicia el proceso para mostrar estadísticas de una lista.
    """
    user_id = message.from_user.id
    if user_id not in listas_usuarios or not listas_usuarios[user_id]:
        bot.reply_to(message, "No tenés listas activas para ver estadísticas.")
        return

    nombres = list(listas_usuarios[user_id].keys())
    texto = "Tus listas activas:\n" + "\n".join(f"• {n}" for n in nombres)
    texto += "\n\nEscribí el nombre de la lista para la que querés ver las estadísticas."
    bot.reply_to(message, texto, parse_mode="Markdown")
    bot.register_next_step_handler(message, generar_estadisticas)


def generar_estadisticas(message: Message):
    """
    funcion qeu maneja el comando /estadisticas y genera el grafico.
    """
    nombre_lista = message.text.strip().lower()
    _enviar_grafico_estadisticas(message, nombre_lista)

# FLUJO: cancelar

@bot.message_handler(commands=['cancelar'])
def cancelar(message: Message):
    user_id = message.from_user.id
    clear_user_context(user_id) 
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    
    bot.reply_to(message, "Operación cancelada.")
