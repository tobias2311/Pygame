import pygame
import os

"""Módulo para la carga y gestión de activos multimedia (imágenes, fuentes y música)."""

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

def actualizar_musica_pantalla(pantalla_actual, musica_actual, configuracion_musica):
    """Determina si debe cambiar la música según la pantalla y devuelve el nuevo identificador."""
    nueva_musica = musica_actual
    
    es_menu = (pantalla_actual == "login" or pantalla_actual == "registro" or 
               pantalla_actual == "menu" or pantalla_actual == "seleccion" or 
               pantalla_actual == "configuracion" or pantalla_actual == "ranking")
               
    if es_menu == True:
        if musica_actual != "menu":
            gestionar_musica(configuracion_musica["archivo_menu"], volumen=pygame.mixer.music.get_volume())
            nueva_musica = "menu"
    elif pantalla_actual == "juego":
        if musica_actual != "juego":
            gestionar_musica(configuracion_musica["archivo_juego"], volumen=pygame.mixer.music.get_volume())
            nueva_musica = "juego"
            
    return nueva_musica
