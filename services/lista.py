from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# Constantes
(
    ESPERANDO_NOMBRE,
    ESPERANDO_PRESUPUESTO,
    AGREGANDO_PRODUCTO,
    AJUSTAR_PRESUPUESTO
) = range(4)

# Estados para ver list y eliminar lista
ESPERANDO_NOMBRE_LISTA = "ESPERANDO_NOMBRE_LISTA"
ESPERANDO_NOMBRE_ELIMINAR = "ESPERANDO_NOMBRE_ELIMINAR"
CONFIRMAR_BORRADO = "CONFIRMAR_BORRADO"

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


# Listas del usuario
listas_usuarios = {}

#
def _clasificar_producto(nombre_producto):
    """Clasifica un producto basado en las listas  que determina si es esencial, intermedio o no esencial."""
    nombre_lower = nombre_producto.lower()
    # Chequea que no sea no esencial primero
    if any(p in nombre_lower for p in no_esenciales):
        return "no esencial"
    if any(p in nombre_lower for p in intermedios):
        return "intermedio"
    if any(p in nombre_lower for p in Esenciales):
        return "esencial"
    # Si no está en ninguna lista, lo marcamos como intermedio por defecto
    return "intermedio" 


# Flujo: crear lista con /empezar_lista
async def empezar_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Funcion para iniciar la creación de una nueva lista de compras. Limita a 2 listas por usuario.
    1. Pide el nombre de la lista.
    2. Pide el presupuesto máximo.
    3. Permite agregar productos hasta que el usuario finalice.
    4. Maneja el presupuesto y sugiere ajustes si se excede.    
    '''
    user_id = update.message.from_user.id
    listas_usuarios.setdefault(user_id, {})

    if len(listas_usuarios[user_id]) >= 2:
        await update.message.reply_text("Ya tenés dos listas activas. Usá /eliminar_lista si querés crear una nueva.")
        return ConversationHandler.END

    await update.message.reply_text("Escribí un nombre para esta lista (por ejemplo 'semana' o 'mes'):")
    return ESPERANDO_NOMBRE


async def definir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Funcion que define el nombre de la lista y verifica que no exista ya.   
    '''
    user_id = update.message.from_user.id
    nombre_lista = update.message.text.strip().lower()

    if nombre_lista in listas_usuarios[user_id]:
        await update.message.reply_text("Ya existe una lista con ese nombre. Elegí otro.")
        return ESPERANDO_NOMBRE

    listas_usuarios[user_id][nombre_lista] = {"presupuesto": 0, "total": 0, "items": []}
    context.user_data["lista_activa"] = nombre_lista
    await update.message.reply_text(f"Perfecto. La lista '{nombre_lista}' fue creada. ¿Cuál es tu presupuesto máximo?")
    return ESPERANDO_PRESUPUESTO 


async def definir_presupuesto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    funcion que define el presupuesto máximo para la lista.Asegura queel numero del presupuesto sea positivo.
    '''
    user_id = update.message.from_user.id
    nombre_lista = context.user_data.get("lista_activa")

    try:
        presupuesto = int(update.message.text)
        if presupuesto <= 0:
             await update.message.reply_text("El presupuesto debe ser un número positivo.")
             return ESPERANDO_PRESUPUESTO
        
        listas_usuarios[user_id][nombre_lista]["presupuesto"] = presupuesto
        await update.message.reply_text(f"Presupuesto de ${presupuesto} establecido para '{nombre_lista}'.\n"
                                        "Agregá tus productos (ej: arroz 2500).\n"
                                        "Cuando termines, usá /finalizar_lista.")
        return AGREGANDO_PRODUCTO
    except (ValueError, TypeError):
        await update.message.reply_text("Ingresá un número válido para el presupuesto.")
        return ESPERANDO_PRESUPUESTO 


async def agregar_producto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Funcion para agregar productos a la lista.Actualiza el total y maneja el presupuesto.
    1. Verifica el formato del mensaje.
    2. Clasifica el producto como esencial, intermedio o no esencial.
    3. Actualiza el total gastado.
    4. Si se excede el presupuesto, sugiere eliminar productos no esenciales.
    '''
    user_id = update.message.from_user.id
    nombre_lista = context.user_data.get("lista_activa")
    
    if not nombre_lista or nombre_lista not in listas_usuarios.get(user_id, {}):
        await update.message.reply_text("Hubo un error, no encuentro tu lista activa. Empezá de nuevo con /empezar_lista.")
        return ConversationHandler.END

    mensaje = update.message.text.lower().strip()
    partes = mensaje.split()

    if len(partes) < 2:
        await update.message.reply_text("El formato es incorrecto. Usá: producto precio (ej. harina 1500)")
        return AGREGANDO_PRODUCTO

    try:
        monto = int(partes[-1])
        nombre = " ".join(partes[:-1])
        if monto <= 0:
            await update.message.reply_text("El monto debe ser un número positivo.")
            return AGREGANDO_PRODUCTO
    except ValueError:
        await update.message.reply_text("El monto debe ser un número válido al final.")
        return AGREGANDO_PRODUCTO

    data = listas_usuarios[user_id][nombre_lista]
    
    # Clasifica y guarda el tipo
    tipo_producto = _clasificar_producto(nombre)
    data["items"].append({"nombre": nombre, "monto": monto, "tipo": tipo_producto})
    data["total"] += monto

    presupuesto = data["presupuesto"]
    total = data["total"]
    
    mensaje_respuesta = f"Agregado: {nombre} (${monto}) - *{tipo_producto}*\n"
    mensaje_respuesta += f"Total: ${total} / ${presupuesto}\n"

    if total > presupuesto:
        mensaje_respuesta += "\n *¡Te pasaste del presupuesto!*"

        # Buscamos productos no esenciales en su lista
        productos_no_esenciales = [item for item in data["items"] if item["tipo"] == "no esencial"]

        if productos_no_esenciales:
            productos_texto = "\n".join(f"• {item['nombre']} (${item['monto']})" for item in productos_no_esenciales)
            mensaje_respuesta += (
                f"\nTenés estos productos no esenciales en tu lista:\n{productos_texto}\n\n"
                "Escribí el nombre exacto del producto que querés **eliminar** o escribí **'no'** para mantenerlo."
            )
            context.user_data["productos_no_esenciales"] = productos_no_esenciales
            await update.message.reply_text(mensaje_respuesta, parse_mode="Markdown")
            return AJUSTAR_PRESUPUESTO
        else:
            mensaje_respuesta += "\n No tenés productos no esenciales en tu lista para recortar fácilmente."
            await update.message.reply_text(mensaje_respuesta, parse_mode="Markdown")
            return AGREGANDO_PRODUCTO

    elif total >= presupuesto * 0.9:
        mensaje_respuesta += "Estás cerca del límite."
    elif tipo_producto == "no esencial":
        mensaje_respuesta += f"(Recordá que '{nombre}' es no esencial)"

    await update.message.reply_text(mensaje_respuesta, parse_mode="Markdown")
    return AGREGANDO_PRODUCTO


async def ajustar_presupuesto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Funcion para ajustar la lista si el usuario se excede del presupuesto.
    1. Si el usuario dice 'no', mantiene los productos pero informa que sigue excedido.
    2. Si el usuario nombra un producto, lo elimina de la lista y actualiza el total.
    3. Verifica si aún se excede y sugiere más eliminaciones 
    '''
    user_id = update.message.from_user.id
    nombre_lista = context.user_data.get("lista_activa")
    respuesta = update.message.text.lower().strip()
    data = listas_usuarios[user_id][nombre_lista]

    if respuesta == "no":
        await update.message.reply_text("OK. Mantenemos los productos, pero seguís excedido. Podés agregar más o usar /finalizar_lista.")
        return AGREGANDO_PRODUCTO

    productos_no_esenciales = context.user_data.get("productos_no_esenciales", [])
    item_a_eliminar = next((item for item in productos_no_esenciales if item["nombre"] == respuesta), None)

    if item_a_eliminar:
        data["items"].remove(item_a_eliminar)
        data["total"] = sum(i["monto"] for i in data["items"])
        
        await update.message.reply_text(
            f"'{respuesta}' fue eliminado. Nuevo total: ${data['total']} / ${data['presupuesto']}"
        )
        # Actualizamos la lista de no esenciales en contexto
        context.user_data["productos_no_esenciales"] = [item for item in data["items"] if item["tipo"] == "no esencial"]

    else:
        await update.message.reply_text("No encontré ese producto en tu lista de 'no esenciales'. Escribí el nombre exacto o 'no'.")
        return AJUSTAR_PRESUPUESTO # Mantenemos el estado

    # Verificamos si sigue excediendo el presupuesto
    if data["total"] > data["presupuesto"]:
        if context.user_data["productos_no_esenciales"]:
            productos_texto = "\n".join(f"• {item['nombre']} (${item['monto']})" for item in context.user_data["productos_no_esenciales"])
            await update.message.reply_text(
                f"Aún superás el presupuesto. ¿Querés eliminar otro?\n{productos_texto}\n(Escribí el nombre o 'no')"
            )
            return AJUSTAR_PRESUPUESTO
        else:
             await update.message.reply_text("Ya no quedan más productos no esenciales. Seguís excedido. Podés /finalizar_lista o agregar otro producto.")
             return AGREGANDO_PRODUCTO
    
    await update.message.reply_text(
        "¡Perfecto! Ya estás dentro del presupuesto.\nSeguí agregando productos o usá /finalizar_lista."
    )
    return AGREGANDO_PRODUCTO



async def ver_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Funcion que iniciar el proceso para ver una lista existente.
    1. Muestra las listas activas del usuario.  
    2. Pide el nombre de la lista a ver.
    3. Muestra el resumen de la lista
    '''
    user_id = update.message.from_user.id

    if user_id not in listas_usuarios or not listas_usuarios[user_id]:
        await update.message.reply_text("No tenés listas activas. Creá una con /empezar_lista.")
        return ConversationHandler.END 

    nombres = list(listas_usuarios[user_id].keys())
    
    if len(nombres) == 1:
        # Si solo tiene una lista, le pedimos que confirme el nombre
        await update.message.reply_text(f"Tenés una lista: '{nombres[0]}'. Escribí su nombre para verla.")
    else:
        texto = "📋 Tus listas activas:\n" + "\n".join(f"• {n}" for n in nombres)
        texto += "\n\nEscribí el nombre de la lista que querés ver."
        await update.message.reply_text(texto)

    return ESPERANDO_NOMBRE_LISTA


async def mostrar_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    nombre_lista = update.message.text.strip().lower()

    if user_id not in listas_usuarios or nombre_lista not in listas_usuarios[user_id]:
        await update.message.reply_text("No existe una lista con ese nombre.")
        return ConversationHandler.END

    data = listas_usuarios[user_id][nombre_lista]
    
    if not data["items"]:
        resumen = "La lista está vacía."
    else:
        # Mostramos los ítems con su tipo
        resumen = "\n".join([f"• {i['nombre']} (${i['monto']}) - *{i['tipo']}*" for i in data["items"]])

    total = data["total"]
    presupuesto = data["presupuesto"]
    restante = presupuesto - total

    mensaje = (f"*{nombre_lista.upper()}*:\n\n{resumen}\n\n"
               f"Total gastado: ${total}\n"
               f"Presupuesto: ${presupuesto}\n")
    
    if total > presupuesto:
        mensaje += f" *Estás ${total - presupuesto} por encima del presupuesto.*"
    else:
         mensaje += f"Te sobran: ${restante}"

    await update.message.reply_text(mensaje, parse_mode="Markdown")
    return ConversationHandler.END


#   Flujo: Para eliminar lista con  /eliminar_lista

async def eliminar_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Inicia el proceso para eliminar una lista.
    """
    user_id = update.message.from_user.id
    if user_id not in listas_usuarios or not listas_usuarios[user_id]:
        await update.message.reply_text("No tenés listas activas para eliminar.")
        return ConversationHandler.END

    nombres = list(listas_usuarios[user_id].keys())
    texto = " Tus listas activas:\n" + "\n".join(f"• {n}" for n in nombres)
    texto += "\n\nEscribí el nombre exacto de la lista que querés **eliminar**."
    await update.message.reply_text(texto, parse_mode="Markdown")
    return ESPERANDO_NOMBRE_ELIMINAR


async def confirmar_eliminacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Pide confirmar antes de borrar.
    """
    user_id = update.message.from_user.id
    nombre_lista = update.message.text.strip().lower()

    if nombre_lista not in listas_usuarios.get(user_id, {}):
        await update.message.reply_text("No existe esa lista. Volvé a empezar con /eliminar_lista si querés.")
        return ConversationHandler.END

    context.user_data["lista_a_borrar"] = nombre_lista
    await update.message.reply_text(
        f"¿Seguro de que querés eliminar la lista '{nombre_lista}' para siempre? (sí/no)"
    )
    return CONFIRMAR_BORRADO


async def ejecutar_eliminacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Elimina la lista si el usuario dice 'sí'.
    """
    user_id = update.message.from_user.id
    respuesta = update.message.text.strip().lower()
    nombre_lista = context.user_data.get("lista_a_borrar")

    if respuesta == "sí": # con tilde 
        if nombre_lista and nombre_lista in listas_usuarios.get(user_id, {}):
            listas_usuarios[user_id].pop(nombre_lista)
            await update.message.reply_text(f"Listo. La lista '{nombre_lista}' fue eliminada.")
        else:
            await update.message.reply_text("Error, no encontré la lista para borrar.")
    else:
        await update.message.reply_text("Cancelado. Tu lista está a salvo.")

    context.user_data.pop("lista_a_borrar", None)
    return ConversationHandler.END


async def finalizar_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Funcion para finalizar la lista activa del usuario.
    1. Muestra un resumen de la lista
    3. Indica que la lista fue guardada y que ya no se pueden agregar mas productos.
    '''

    user_id = update.message.from_user.id
    nombre_lista = context.user_data.get("lista_activa")

    if not nombre_lista or nombre_lista not in listas_usuarios.get(user_id, {}):
        await update.message.reply_text("No tenés una lista activa para finalizar.")
        return ConversationHandler.END

    await update.message.reply_text(f"Resumen de la lista '{nombre_lista}':")

    data = listas_usuarios[user_id][nombre_lista]
    if not data["items"]:
        resumen = "La lista está vacía."
    else:
        resumen = "\n".join([f"• {i['nombre']} (${i['monto']}) - *{i['tipo']}*" for i in data["items"]])

    total = data["total"]
    presupuesto = data["presupuesto"]
    restante = presupuesto - total

    mensaje = (f"*{nombre_lista.upper()}*:\n\n{resumen}\n\n"
               f"Total gastado: ${total}\n"
               f"Presupuesto: ${presupuesto}\n")
    if total > presupuesto:
        mensaje += f" *Estás ${total - presupuesto} por encima del presupuesto.*"
    else:
         mensaje += f"Te sobran: ${restante}"
    await update.message.reply_text(mensaje, parse_mode="Markdown")
    
    context.user_data.pop("lista_activa", None)
    
    await update.message.reply_text(f"Lista '{nombre_lista}' guardada. Ya no estás agregando productos.")
    return ConversationHandler.END


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Cancela la operación actual y limpia el contexto.
    """
    context.user_data.pop("lista_activa", None)
    context.user_data.pop("lista_a_borrar", None)
    await update.message.reply_text("Operación cancelada.")
    return ConversationHandler.END