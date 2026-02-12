import csv
import json
import os

def cargar_preguntas(ruta_archivo: str) -> list:
    """
    Carga preguntas desde un archivo CSV.
    Retorna una lista de diccionarios con la estructura de la pregunta.
    """
    preguntas = []
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Normalizamos la estructura para que sea fácil de usar en el juego
                pregunta = {
                    "enunciado": fila.get("enunciado", ""),
                    "respuesta_correcta": fila.get("respuesta_correcta", ""),
                    "opciones": [
                        fila.get("opcion1", ""),
                        fila.get("opcion2", ""),
                        fila.get("opcion3", ""),
                        fila.get("opcion4", "")
                    ],
                    "categoria": fila.get("categoria", ""),
                    "dificultad": fila.get("dificultad", ""),
                    "puntos": int(fila.get("puntos", 0))
                }
                preguntas.append(pregunta)
    else:
        print(f"Error: No se encontró el archivo de preguntas en {ruta_archivo}")
    
    return preguntas

def cargar_configuracion(ruta_archivo: str) -> dict:
    """
    Lee la configuración del juego desde un archivo JSON.
    """
    config = {}
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            config = json.load(archivo)
    else:
        print(f"Error: No se encontró el archivo de configuración en {ruta_archivo}")
    
    return config

def guardar_datos_json(ruta_archivo: str, datos: dict) -> bool:
    """
    Guarda un diccionario en un archivo JSON (usado para estadísticas y usuarios).
    """
    try:
        with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar JSON: {e}")
        return False
