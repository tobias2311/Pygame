import pygame
import os

# CONFIGURACIÓN DE RUTAS
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUTA_ASSETS = os.path.join(RUTA_BASE, "assets")
RUTA_SOUNDS = os.path.join(RUTA_BASE, "assets") # Ahora la música también está en assets

def cargar_imagen(nombre_archivo, size=(100, 100)):
    """
    Carga una imagen y la devuelve escalada. Si el archivo no existe, devuelve una superficie sólida.
    """
    ruta = os.path.join(RUTA_ASSETS, nombre_archivo)
    
    if os.path.exists(ruta) == True:
        imagen = pygame.image.load(ruta)
        # Escalamos la imagen al tamaño solicitado
        imagen = pygame.transform.scale(imagen, size)
    else:
        print(f"Advertencia: No se encontró {nombre_archivo}. Usando placeholder.")
        imagen = pygame.Surface(size)
        imagen.fill((50, 50, 50))
    
    return imagen

def cargar_recursos_graficos(config_ventana):
    """
    Centraliza la carga de todas las imágenes del juego usando las dimensiones del JSON.
    """
    ancho = config_ventana["ancho"]
    alto = config_ventana["alto"]
    
    recursos = {
        "fondos": {
            "menu": cargar_imagen("menu_ia.png", size=(ancho, alto)),
            "juego": cargar_imagen("juego_ia.png", size=(ancho, alto))
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
