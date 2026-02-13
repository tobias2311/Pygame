import pygame
import os

# Módulo para la carga y gestión de activos multimedia (imágenes, fuentes y música).

RUTA_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUTA_ASSETS = os.path.join(RUTA_BASE, "assets")
RUTA_SOUNDS = os.path.join(RUTA_BASE, "assets")

def cargar_imagen(nombre_archivo, size=(100, 100)):
    """Carga una imagen desde el disco y la escala a las dimensiones proporcionadas."""
    ruta = os.path.join(RUTA_ASSETS, nombre_archivo)
    
    if os.path.exists(ruta) == True:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, size)
    else:
        print(f"Advertencia: No se encontró {nombre_archivo}. Utilizando superficie vacía.")
        imagen = pygame.Surface(size)
        imagen.fill((50, 50, 50))
    
    return imagen

def cargar_recursos_graficos(config_ventana):
    """Carga todos los fondos y elementos gráficos necesarios para el juego."""
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
    """Inicializa los objetos de fuente de Pygame con los tamaños configurados."""
    fuentes = {
        "titulo": pygame.font.Font(None, config_fuentes["titulo"]),
        "subtitulo": pygame.font.Font(None, config_fuentes["subtitulo"]),
        "cuerpo": pygame.font.Font(None, config_fuentes["cuerpo"]),
        "info": pygame.font.Font(None, config_fuentes["info"])
    }
    return fuentes

def gestionar_musica(nombre_archivo, volumen=0.5):
    """Carga y reproduce música de fondo en bucle."""
    ruta = os.path.join(RUTA_SOUNDS, nombre_archivo)
    if os.path.exists(ruta) == True:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)
