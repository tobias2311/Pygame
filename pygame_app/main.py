import pygame
import sys
import os

"""Archivo principal que orquestra el juego y gestiona el cambio de pantallas."""

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logica.cargar_archivos import cargar_configuracion, cargar_preguntas
from grafica.carga_recursos import cargar_recursos_graficos, cargar_fuentes, gestionar_musica
from grafica.menu import generar_botones_menu, mostrar_menu
from grafica.seleccion import generar_botones_seleccion, mostrar_seleccion
from logica.sonido import actualizar_volumen_global, procesar_eventos_volumen
from logica.juego_logica import inicializar_estado_juego
from grafica.juego import mostrar_pantalla_juego, generar_botones_vol_juego
from grafica.usuarios_ui import inicializar_ui_usuarios, mostrar_pantalla_login, mostrar_pantalla_registro
from logica.usuarios import actualizar_puntaje_maximo
from grafica.ranking import generar_botones_ranking, mostrar_ranking
from grafica.configuracion import generar_botones_config, mostrar_configuracion

def inicializar_ventana(config_ventana):
    ancho = config_ventana["ancho"]
    alto = config_ventana["alto"]
    titulo = config_ventana["titulo"]
    
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(titulo)
    return pantalla

def main():
    pygame.init()
    pygame.mixer.init()

    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    config = cargar_configuracion(os.path.join(ruta_base, "data", "config.json"))
    estilo = cargar_configuracion(os.path.join(ruta_base, "data", "estilo.json"))
    layout = cargar_configuracion(os.path.join(ruta_base, "data", "layout.json"))
    sonidos_cfg = cargar_configuracion(os.path.join(ruta_base, "data", "sonidos.json"))

    conf_ventana = config["ventana"]
    conf_juego = config["juego"]
    colores = estilo["colores"]
    conf_fuentes = estilo["fuentes"]
    conf_menu = layout["menu_principal"]
    conf_ui_config = layout["configuracion"]
    conf_ui_juego = layout["juego_ui"]
    conf_ui_seleccion = layout["seleccion"]
    conf_ui_ranking = layout["ranking"]
    
    ruta_preguntas = os.path.join(ruta_base, "preguntas_juego.csv")
    preguntas_base = cargar_preguntas(ruta_preguntas)
    
    pantalla = inicializar_ventana(conf_ventana)
    ancho_p = pantalla.get_width()
    alto_p = pantalla.get_height()

    recursos = cargar_recursos_graficos(conf_ventana)
    fuentes = cargar_fuentes(conf_fuentes)
    fuente_botones = fuentes["subtitulo"]

    botones_menu = generar_botones_menu(ancho_p, alto_p, conf_menu, colores, fuente_botones)
    botones_seleccion = generar_botones_seleccion(ancho_p, alto_p, conf_ui_seleccion, fuentes, colores)
    ui_usuarios = inicializar_ui_usuarios(ancho_p, alto_p, fuentes, colores)
    botones_config = generar_botones_config(ancho_p, alto_p, conf_ui_config, colores, fuente_botones, config["juego"])
    botones_ranking = generar_botones_ranking(ancho_p, alto_p, conf_ui_ranking, colores, fuente_botones)
    botones_vol_juego = generar_botones_vol_juego(ancho_p, alto_p, conf_ui_juego["controles_volumen"], colores, fuentes["info"])
    
    pantalla_actual = "login"
    usuario_logueado = None
    estado_juego = None
    
    control_volumen = {
        "nivel": 0.5,
        "mute": False
    }
    musica_actual = ""
    
    seleccion_partida = {
        "tematica": "",
        "dificultad": ""
    }
    
    corriendo = True
    
    while corriendo == True:
        pos_mouse = pygame.mouse.get_pos()
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False

        configuracion_musica = sonidos_cfg["musica"]
        if pantalla_actual == "menu" or pantalla_actual == "seleccion" or pantalla_actual == "configuracion" or pantalla_actual == "ranking" or pantalla_actual == "login" or pantalla_actual == "registro":
            if musica_actual != "menu":
                actualizar_volumen_global(control_volumen)
                gestionar_musica(configuracion_musica["archivo_menu"], volumen=pygame.mixer.music.get_volume())
                musica_actual = "menu"
        elif pantalla_actual == "juego":
            if musica_actual != "juego":
                actualizar_volumen_global(control_volumen)
                gestionar_musica(configuracion_musica["archivo_juego"], volumen=pygame.mixer.music.get_volume())
                musica_actual = "juego"

        if pantalla_actual == "login":
            prox, datos_u = mostrar_pantalla_login(pantalla, recursos, fuentes, colores, ui_usuarios["login"], pos_mouse, eventos)
            if prox == "menu":
                usuario_logueado = datos_u
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
                seleccion_partida["tematica"] = ""
                seleccion_partida["dificultad"] = ""
                pantalla_actual = "seleccion"
            elif prox_pantalla == "configuracion":
                pantalla_actual = "configuracion"
            elif prox_pantalla == "ranking":
                pantalla_actual = "ranking"
            elif prox_pantalla == "salir":
                corriendo = False

        elif pantalla_actual == "seleccion":
            resultado = mostrar_seleccion(pantalla, recursos, fuentes, colores, botones_seleccion, pos_mouse, eventos, seleccion_partida)
            if resultado == "menu":
                pantalla_actual = "menu"
            elif resultado == "iniciar_juego":
                datos_mensajes = cargar_configuracion(os.path.join(ruta_base, "data", "mensajes.json"))
                lista_motivadores = datos_mensajes["motivadores"]
                
                estado_juego = inicializar_estado_juego(preguntas_base, conf_juego, seleccion_partida["tematica"], seleccion_partida["dificultad"])
                estado_juego["mensajes_motivadores"] = lista_motivadores
                
                pantalla_actual = "juego"

        elif pantalla_actual == "juego":
            resultado = mostrar_pantalla_juego(pantalla, recursos, fuentes, colores, estado_juego, pos_mouse, eventos, botones_vol_juego, control_volumen, conf_ui_juego["layout"])
            if resultado == "menu":
                pantalla_actual = "menu"
            elif resultado == "podio":
                actualizar_puntaje_maximo(usuario_logueado, estado_juego["puntaje"])
                pantalla_actual = "menu"

        elif pantalla_actual == "configuracion":
            prox = mostrar_configuracion(pantalla, recursos, fuentes, colores, botones_config, pos_mouse, eventos, config, conf_ui_config)
            if prox == "menu":
                pantalla_actual = "menu"

        elif pantalla_actual == "ranking":
            prox = mostrar_ranking(pantalla, recursos, fuentes, colores, botones_ranking, pos_mouse, eventos, conf_ui_ranking)
            if prox == "menu":
                pantalla_actual = "menu"

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
