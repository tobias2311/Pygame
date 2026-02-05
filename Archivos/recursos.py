"""
Módulo para cargar y gestionar recursos del juego (fondos, fuentes, imágenes)
"""
import pygame
import os
from constantes import ANCHO_VENTANA, ALTO_VENTANA, PROJ_ROOT, FONDO_MENU, FONDO_JUEGO


def cargar_fondo(nombre_archivo, color_fallback=(50, 50, 50)):
   
    # Intentar desde la carpeta Archivos/Bocetos
    ruta_posible = os.path.join(os.path.dirname(__file__), "Bocetos", nombre_archivo)
    if os.path.exists(ruta_posible):
        return pygame.image.load(ruta_posible)
    
    # Intentar desde PROJ_ROOT/Bocetos
    ruta_alternativa = os.path.join(PROJ_ROOT, "Bocetos", nombre_archivo)
    if os.path.exists(ruta_alternativa):
        return pygame.image.load(ruta_alternativa)
    
    # Fallback: superficie de color
    superficie = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    superficie.fill(color_fallback)
    return superficie


def escalar_imagen(imagen, ancho=None, alto=None):
   
    if ancho is None:
        ancho = ANCHO_VENTANA
    if alto is None:
        alto = ALTO_VENTANA
    
    return pygame.transform.scale(imagen, (ancho, alto))


def cargar_fondos():
  
    fondo_menu = cargar_fondo(FONDO_MENU, (50, 50, 50))
    fondo_juego = cargar_fondo(FONDO_JUEGO, (30, 30, 30))
    
    # Intentar fallback a juego.png si juego_ia.png no existe
    if fondo_juego.get_size() == (ANCHO_VENTANA, ALTO_VENTANA) and \
       not os.path.exists(os.path.join(PROJ_ROOT, "Bocetos", FONDO_JUEGO)):
        ruta_juego_viejo = os.path.join(os.path.dirname(__file__), "Bocetos", "juego.png")
        if os.path.exists(ruta_juego_viejo):
            fondo_juego = pygame.image.load(ruta_juego_viejo)
    
    return {
        'menu': escalar_imagen(fondo_menu),
        'juego': escalar_imagen(fondo_juego)
    }


def cargar_fuentes():
   
    return {
        'titulo': pygame.font.Font(None, 48),
        'titulo_grande': pygame.font.Font(None, 70),
        'ajustes': pygame.font.Font(None, 36),
        'info': pygame.font.Font(None, 28),
        'info_pequeña': pygame.font.Font(None, 24),
        'pregunta': pygame.font.Font(None, 50),
        'opciones': pygame.font.Font(None, 36),
        'feedback': pygame.font.Font(None, 48),
        'puntos': pygame.font.Font(None, 64),
        'boton': pygame.font.Font(None, 32),
        'guia_titulo': pygame.font.Font(None, 45),
        'guia_info': pygame.font.Font(None, 30),
        'estadisticas_info': pygame.font.Font(None, 50),
        'instrucciones': pygame.font.Font(None, 32),
        'escape': pygame.font.Font(None, 28),
    }
