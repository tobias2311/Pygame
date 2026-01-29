import csv
import os

def cargar_preguntas_desde_csv():
    """Carga las preguntas desde el archivo CSV"""
    ruta_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), "preguntas_juego.csv")
    
    preguntas = []
    try:
        with open(ruta_csv, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                preguntas.append({
                    "enunciado": fila.get("enunciado", ""),
                    "respuesta_correcta": fila.get("respuesta_correcta", ""),
                    "opciones": [
                        fila.get("opcion1", ""),
                        fila.get("opcion2", ""),
                        fila.get("opcion3", ""),
                        fila.get("opcion4", "")
                    ],
                    "categoria": fila.get("categoria", ""),
                    "puntos": int(fila.get("puntos", "1"))
                })
    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_csv}")
    
    return preguntas
