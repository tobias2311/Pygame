import pygame
import sys
import os

# Agregamos el directorio raíz al path para importar correctamente los módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logica.cargar_archivos import cargar_configuracion, cargar_preguntas
from grafica.carga_recursos import cargar_recursos_graficos, cargar_fuentes, gestionar_musica
from grafica.menu import generar_botones_menu, mostrar_menu
from grafica.seleccion import generar_botones_seleccion, mostrar_seleccion
from grafica.juego import inicializar_estado_juego, mostrar_pantalla_juego, generar_botones_vol_juego
from grafica.usuarios_ui import inicializar_ui_usuarios, mostrar_pantalla_login, mostrar_pantalla_registro
from grafica.configuracion import generar_botones_config, mostrar_configuracion

def inicializar_ventana(config_ventana):
    """
    Configura la ventana usando los valores del JSON.
    """
    ancho = config_ventana["ancho"]
    alto = config_ventana["alto"]
    titulo = config_ventana["titulo"]
    
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(titulo)
    return pantalla

def main():
    # 1. Inicialización de Pygame
    pygame.init()
    pygame.mixer.init()

    # 2. Carga de Configuración
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_config = os.path.join(ruta_base, "data", "config.json")
    config = cargar_configuracion(ruta_config)

    conf_ventana = config["ventana"]
    colores = config["colores"]
    conf_menu = config["ui"]["menu_principal"]
    conf_fuentes = config["fuentes"]
    conf_juego = config["juego"]
    conf_ui_config = config["ui"]["configuracion"]
    conf_ui_juego = config["ui"]["juego_ui"]
    
    # 2.1 Carga de Preguntas
    ruta_preguntas = os.path.join(ruta_base, "preguntas_juego.csv")
    preguntas_base = cargar_preguntas(ruta_preguntas)
    
    # 3. Configuración de la Ventana
    pantalla = inicializar_ventana(conf_ventana)
    ancho_p = pantalla.get_width()
    alto_p = pantalla.get_height()

    # 4. Carga de Recursos
    recursos = cargar_recursos_graficos(conf_ventana)
    fuentes = cargar_fuentes(conf_fuentes)
    fuente_botones = fuentes["subtitulo"]

    # 5. Inicialización de Estados
    # Generamos los botones de las pantallas una sola vez
    botones_menu = generar_botones_menu(ancho_p, alto_p, conf_menu, colores, fuente_botones)
    botones_seleccion = generar_botones_seleccion(ancho_p, alto_p, fuentes, colores)
    ui_usuarios = inicializar_ui_usuarios(ancho_p, alto_p, fuentes, colores)
    botones_config = generar_botones_config(ancho_p, alto_p, conf_ui_config, colores, fuente_botones)
    botones_vol_juego = generar_botones_vol_juego(ancho_p, alto_p, conf_ui_juego["controles_volumen"], colores, fuentes["info"])
    
    pantalla_actual = "login"
    usuario_logueado = None
    estado_juego = None
    
    # Estado Global de Sonido
    control_volumen = {
        "nivel": 0.5,
        "mute": False
    }
    
    # Control de música
    musica_actual = ""
    
    # Estado de la selección actual
    seleccion_partida = {
        "tematica": "",
        "dificultad": ""
    }
    
    corriendo = True
    
    # 6. Loop Principal
    while corriendo == True:
        pos_mouse = pygame.mouse.get_pos()
        eventos = pygame.event.get()

        #--- Gestión de Eventos Globales ---
        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False

        #--- Gestión de Música ---
        if pantalla_actual in ["login", "registro", "menu", "seleccion", "configuracion"]:
            if musica_actual != "menu":
                gestionar_musica("musica_menu.mp3", volumen=control_volumen["nivel"] if not control_volumen["mute"] else 0.0)
                musica_actual = "menu"
        elif pantalla_actual == "juego":
            if musica_actual != "juego":
                gestionar_musica("musica_juego.mp3", volumen=control_volumen["nivel"] if not control_volumen["mute"] else 0.0)
                musica_actual = "juego"

        # --- GESTOR DE PANTALLAS (Screen Manager) ---
        if pantalla_actual == "login":
            prox, datos_u = mostrar_pantalla_login(pantalla, recursos, fuentes, colores, ui_usuarios["login"], pos_mouse, eventos)
            if prox == "menu":
                usuario_logueado = datos_u
                print(f"Bienvenido {usuario_logueado['nombre']}!")
                pantalla_actual = "menu"
            elif prox == "registro":
                pantalla_actual = "registro"

        elif pantalla_actual == "registro":
            prox = mostrar_pantalla_registro(pantalla, recursos, fuentes, colores, ui_usuarios["registro"], pos_mouse, eventos)
            if prox == "login":
                pantalla_actual = "login"

        elif pantalla_actual == "menu":
            prox_pantalla = mostrar_menu(pantalla, recursos, fuentes, colores, botones_menu, pos_mouse, eventos, control_volumen)
            if prox_pantalla == "juego":
                # Al dar "Comenzar" ahora vamos a la selección
                pantalla_actual = "seleccion"
            elif prox_pantalla == "configuracion":
                pantalla_actual = "configuracion"
            elif prox_pantalla == "salir":
                corriendo = False

        elif pantalla_actual == "seleccion":
            resultado = mostrar_seleccion(pantalla, recursos, fuentes, colores, botones_seleccion, pos_mouse, eventos, seleccion_partida)
            if resultado == "menu":
                pantalla_actual = "menu"
            elif resultado == "iniciar_juego":
                print(f"Iniciando: {seleccion_partida['tematica']} - {seleccion_partida['dificultad']}")
                estado_juego = inicializar_estado_juego(
                    preguntas_base, 
                    conf_juego, 
                    seleccion_partida["tematica"], 
                    seleccion_partida["dificultad"]
                )
                pantalla_actual = "juego"

        elif pantalla_actual == "juego":
            # Pasamos el estado_juego para que la función lo modifique internamente
            resultado = mostrar_pantalla_juego(pantalla, recursos, fuentes, colores, estado_juego, pos_mouse, eventos, botones_vol_juego, control_volumen)
            
            if resultado == "menu":
                pantalla_actual = "menu"
            elif resultado == "podio":
                print("¡Juego terminado! Puntuación final:", estado_juego["puntaje"])
                pantalla_actual = "menu" # placeholder hasta tener podio

        elif pantalla_actual == "configuracion":
            prox = mostrar_configuracion(pantalla, recursos, fuentes, colores, botones_config, pos_mouse, eventos)
            if prox == "menu":
                pantalla_actual = "menu"

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
