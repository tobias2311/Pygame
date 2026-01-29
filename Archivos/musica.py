import pygame
import os

# Variables de volumen
volumen_actual = 0.5

# Variable para almacenar la música actual
musica_actual = None

def set_volumen(vol):
    """Establece el volumen global"""
    global volumen_actual
    volumen_actual = max(0, min(1, vol))
    # Actualizar volumen de la música si está reproduciendo
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(volumen_actual)

def get_volumen():
    """Obtiene el volumen actual"""
    return volumen_actual

def subir_volumen():
    """Sube el volumen en 0.1"""
    global volumen_actual
    volumen_actual = min(1, volumen_actual + 0.1)
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(volumen_actual)
    return volumen_actual

def bajar_volumen():
    """Baja el volumen en 0.1"""
    global volumen_actual
    volumen_actual = max(0, volumen_actual - 0.1)
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(volumen_actual)
    return volumen_actual

def iniciar_musica():
    """Inicia la música de fondo en loop"""
    try:
        # Obtener la ruta al archivo de música
        ruta_musica = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds", "Música de juegos de retro game (música sin copyright).mp3")
        
        if os.path.exists(ruta_musica):
            # Cargar y reproducir la música
            pygame.mixer.music.load(ruta_musica)
            pygame.mixer.music.set_volume(volumen_actual)
            pygame.mixer.music.play(-1)  # -1 significa reproducir en loop infinito
        else:
            print(f"Archivo de música no encontrado: {ruta_musica}")
    except Exception as e:
        print(f"Error al cargar la música: {e}")

def detener_musica():
    """Detiene la música"""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def pausar_musica():
    """Pausa la música"""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

def reanudar_musica():
    """Reanuda la música pausada"""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
