"""
Constantes globales del juego
"""
import os

# Dimensiones de ventana
ANCHO_VENTANA = 1400
ALTO_VENTANA = 800

# Rutas del proyecto
PROJ_ROOT = os.path.dirname(os.path.dirname(__file__))

# Colores predefinidos
COLORES = {
    # Colores para botones
    "VERDE": (0, 150, 0),
    "VERDE_OSCURO": (0, 100, 0),
    "VERDE_CLARO": (0, 200, 0),
    "ROJO": (150, 0, 0),
    "ROJO_OSCURO": (100, 0, 0),
    "ROJO_CLARO": (200, 0, 0),
    "AZUL": (0, 0, 255),
    "AZUL_OSCURO": (0, 0, 139),
    "AZUL_CLARO": (0, 0, 200),
    "AMARILLO": (150, 150, 0),
    "AMARILLO_OSCURO": (100, 100, 0),
    "AMARILLO_CLARO": (200, 200, 0),
    "MAGENTA": (255, 0, 255),
    "MAGENTA_OSCURO": (150, 0, 150),
    "MAGENTA_CLARO": (255, 100, 255),
    "GRIS": (100, 100, 100),
    "GRIS_OSCURO": (50, 50, 50),
    "GRIS_CLARO": (150, 150, 150),
    "NARANJA": (255, 150, 0),
    "NARANJA_OSCURO": (200, 80, 0),
    "NARANJA_CLARO": (255, 200, 0),
    
    # Colores de texto
    "BLANCO": (255, 255, 255),
    "NEGRO": (0, 0, 0),
    "AMARILLO_TEXTO": (255, 255, 0),
    "CYAN": (0, 255, 255),
    "NARANJA_TEXTO": (255, 165, 0),
    
    # Colores de feedback
    "VERDE_FEEDBACK": (0, 255, 0),
    "ROJO_FEEDBACK": (255, 0, 0),
    
    # Colores de fondo
    "FONDO_OSCURO": (30, 30, 30),
    "FONDO_MEDIO": (50, 50, 50),
}

# Configuración del juego
NUM_PREGUNTAS = 12
TEMATICAS = ["Cultura General", "Frases Deportivas", "Frases Populares"]
DIFICULTADES = ["Fácil", "Pro", "Experto"]

# Puntos por dificultad
PUNTOS_POR_DIFICULTAD = {
    "Fácil": 1,
    "Pro": 2,
    "Experto": 5
}

# Nombres de archivos de recursos
FONDO_MENU = "menu_ia.png"
FONDO_JUEGO = "juego_ia.png"
MUSICA_MENU = "musica_menu.mp3"
MUSICA_PARTIDA = "musica_partida.mp3"
