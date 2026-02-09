"""
Módulo para cargar y gestionar recursos del juego (fondos, fuentes, imágenes)
"""
import pygame
import os
from constantes import ANCHO_VENTANA, ALTO_VENTANA, PROJ_ROOT, FONDO_MENU, FONDO_JUEGO


def cargar_fondo(nombre_archivo):
    
    ruta = os.path.join("Archivos", "Bocetos", nombre_archivo)
    imagen = pygame.image.load(ruta) 
    return escalar_imagen(imagen)


def escalar_imagen(imagen):
   return pygame.transform.scale(imagen, (ANCHO_VENTANA, ALTO_VENTANA))


def cargar_fondos():
    fondo_menu = escalar_imagen(pygame.image.load(os.path.join(PROJ_ROOT, "Bocetos", FONDO_MENU)))
    fondo_juego = escalar_imagen(pygame.image.load(os.path.join(PROJ_ROOT, "Bocetos", FONDO_JUEGO)))
    return {
        'menu': fondo_menu,
        'juego': fondo_juego
    }


def cargar_fuentes():
   
    return {
        'titulo': pygame.font.Font(None, 48),
        'ajustes': pygame.font.Font(None, 36),
        'info': pygame.font.Font(None, 28)
    }
