import pygame
import sys
import os

"""
Archivo principal del juego.

"""

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logica.juego_logica import inicializar_contexto_juego, gestionar_musica_segun_estado, procesar_logica_por_estado

def main():
    pygame.init()
    pygame.mixer.init()

    # CONFIGURACIÓN (RECURSOS ESTÁTICOS)
    recursos = inicializar_contexto_juego()
    
    # ESTADO GLOBAL 
    estado_global = {
        "pantalla": "login",
        "usuario": None,
        "estado_juego_datos": None,
        "musica_actual": None,
        "volumen": {"nivel": 0.5, "mute": False},
        "seleccion": {"tematica": "", "dificultad": ""},
        "flag_run": True
    }
    
    # BUCLE PRINCIPAL
    while estado_global["flag_run"] == True:
        # 1. Gestión de música según estado
        gestionar_musica_segun_estado(estado_global, recursos["sonidos_cfg"])

        # 2. Captura de inputs
        pos_mouse = pygame.mouse.get_pos()
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                estado_global["flag_run"] = False

        # 3. Lógica según el estado actual (DELEGADO)
        procesar_logica_por_estado(recursos, estado_global, pos_mouse, eventos)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
