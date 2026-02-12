import pygame
import os

# CONFIGURACIÓN DE RUTAS
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUTA_ASSETS = os.path.join(RUTA_BASE, "assets")
RUTA_SOUNDS = os.path.join(RUTA_BASE, "sounds")

def cargar_imagen(nombre_archivo, size=(100, 100)):
    """
    Carga una imagen y la devuelve. Si el archivo no existe, devuelve una superficie sólida.
    Se usa os.path.exists en lugar de try/except por restricciones del proyecto.
    """
    ruta = os.path.join(RUTA_ASSETS, nombre_archivo)
    
    # Verificamos existencia con flujo lógico (sin try-except)
    if os.path.exists(ruta) == True:
        imagen = pygame.image.load(ruta)
    else:
        print(f"Advertencia: No se encontró {nombre_archivo}. Usando placeholder.")
        imagen = pygame.Surface(size)
        imagen.fill((50, 50, 50))
    
    return imagen

def cargar_recursos_graficos():
    """
    Centraliza la carga de todas las imágenes del juego.
    """
    recursos = {
        "fondos": {
            "menu": cargar_imagen("menu_ia.png", size=(1400, 800)),
            "juego": cargar_imagen("juego_ia.png", size=(1400, 800))
        },
        "iconos": {}
    }
    return recursos

def cargar_fuentes(config_fuentes):
    """
    Carga las fuentes tipográficas usando los tamaños definidos en el JSON.
    """
    fuentes = {
        "titulo": pygame.font.Font(None, config_fuentes["titulo"]),
        "subtitulo": pygame.font.Font(None, config_fuentes["subtitulo"]),
        "cuerpo": pygame.font.Font(None, config_fuentes["cuerpo"]),
        "info": pygame.font.Font(None, config_fuentes["info"])
    }
    return fuentes

def gestionar_musica(nombre_archivo, volumen=0.5):
    """
    Maneja el streaming de música de fondo.
    """
    ruta = os.path.join(RUTA_SOUNDS, nombre_archivo)
    if os.path.exists(ruta) == True:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)
