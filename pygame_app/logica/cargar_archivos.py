import csv
import json
import os

# Módulo de funciones de utilidad para la lectura y escritura de archivos CSV y JSON.

def cargar_preguntas(ruta_archivo: str) -> list:
    """Lee el archivo CSV de preguntas y las convierte en una lista de diccionarios."""
    preguntas = []
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
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
    """Carga y decodifica un archivo JSON de configuración."""
    config = {}
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            config = json.load(archivo)
    else:
        print(f"Error: No se encontró el archivo de configuración en {ruta_archivo}")
    
    return config

def guardar_datos_json(ruta_archivo: str, datos: dict) -> bool:
    """Serializa y guarda un diccionario en un archivo formato JSON."""
    try:
        with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar JSON: {e}")
        return False
