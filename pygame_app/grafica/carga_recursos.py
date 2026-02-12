import pygame
import os

# CONFIGURACIÓN DE RUTAS
# Obtenemos la ruta base del proyecto (un nivel arriba de pygame_app)
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUTA_ASSETS = os.path.join(RUTA_BASE, "assets")
RUTA_SOUNDS = os.path.join(RUTA_BASE, "sounds") # Reutilizamos la carpeta sounds de la raíz

def cargar_imagen(nombre_archivo):
    """
    Carga una imagen y la devuelve.
    """
    ruta = os.path.join(RUTA_ASSETS, nombre_archivo)
    return pygame.image.load(ruta)

def cargar_recursos_graficos():
    """
    Centraliza la carga de todas las imágenes del juego.
    """
    recursos = {
        "fondos": {
            "menu": cargar_imagen("menu_ia.png"),
            "juego": cargar_imagen("juego_ia.png")
        },
        "iconos": {
            # Aquí se pueden agregar logos, vidas, etc.
        }
    }
    return recursos

def cargar_fuentes(config_fuentes):
    """
    Carga las fuentes tipográficas usando los tamaños definidos en el JSON.
    """
    return {
        "titulo": pygame.font.Font(None, config_fuentes["titulo"]),
        "subtitulo": pygame.font.Font(None, config_fuentes["subtitulo"]),
        "cuerpo": pygame.font.Font(None, config_fuentes["cuerpo"]),
        "info": pygame.font.Font(None, config_fuentes["info"])
    }

def gestionar_musica(nombre_archivo, volumen=0.5):
    """
    Maneja el streaming de música de fondo directamente.
    Asume que el archivo existe.
    """
    ruta = os.path.join(RUTA_SOUNDS, nombre_archivo)
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1) # -1 para que sea un bucle infinito
