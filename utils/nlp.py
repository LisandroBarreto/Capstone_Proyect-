import json
import unicodedata
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util
from config.config import DATASET_PATH

# modelo_embeddings = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
modelo_embeddings = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


# Carga el dataset JSON.
def cargar_dataset():
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar el dataset: {e}")
        return None
    
# convierte el texto a minuscula, elimina espacios iniciales, finales y elimina
# signos de interrogacion, exclamacion, y puntuacion.
def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    texto = texto.replace("¿", "").replace("?", "").replace("!", "").replace("¡", "").replace(",", "").replace(".", "").strip()
    return texto

# Similitud basada en coincidencia de caracteres.
def similitud_textual(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Similitud semántica usando SentenceTransformer
cache_embeddings = {}

# Modificación de la función de similitud semántica para usar caché
def similitud_semantica(a, b):
    try:
        if a not in cache_embeddings:
            emb_a = modelo_embeddings.encode(a, convert_to_tensor=True)
            cache_embeddings[a] = emb_a
        else:
            emb_a = cache_embeddings[a]
        
        if b not in cache_embeddings:
            emb_b = modelo_embeddings.encode(b, convert_to_tensor=True)
            cache_embeddings[b] = emb_b
        else:
            emb_b = cache_embeddings[b]

        return float(util.cos_sim(emb_a, emb_b))
    except Exception as e:
        print(f"Error en similitud semántica: {e}")
        return 0

# Combina similitud semántica y textual.
def calcular_similitud(mensaje_usuario, pattern):
    mensaje_usuario = normalizar_texto(mensaje_usuario)
    pattern = normalizar_texto(pattern)
    semantica = similitud_semantica(mensaje_usuario, pattern)
    textual = similitud_textual(mensaje_usuario, pattern)
    return (0.7 * semantica) + (0.3 * textual)

# Busca la mejor coincidencia en el dataset.
def buscar_mejor_respuesta(pregunta, dataset):
    mejor_respuesta = None
    mayor_similitud = 0.0

    for item in dataset:
        posibles_preguntas = item["prompt"]
        if isinstance(posibles_preguntas, str):
            posibles_preguntas = [posibles_preguntas]

        for p in posibles_preguntas:
            similitud = calcular_similitud(pregunta, p) 
            if similitud > mayor_similitud:
                mayor_similitud = similitud
                mejor_respuesta = item["respuesta"]

    if mayor_similitud > 0.65:
        return mejor_respuesta
    return None


company_data = cargar_dataset()
if company_data:
    print(f"👍 Dataset cargado correctamente. Total de registros: {len(company_data)}")
else:
    print("No se pudo cargar el dataset correctamente.")