import pygame
import os
from logica.cargar_archivos import cargar_configuracion, cargar_preguntas
from grafica.carga_recursos import cargar_recursos_graficos, cargar_fuentes, gestionar_musica
from grafica.menu import generar_botones_menu, mostrar_menu
from grafica.seleccion import generar_botones_seleccion, mostrar_seleccion
from logica.sonido import actualizar_volumen_global
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

def inicializar_contexto_juego():
    """Carga recursos estáticos y genera botones iniciales."""
    ruta_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config = cargar_configuracion(os.path.join(ruta_base, "data", "config.json"))
    estilo = cargar_configuracion(os.path.join(ruta_base, "data", "estilo.json"))
    layout = cargar_configuracion(os.path.join(ruta_base, "data", "layout.json"))
    sonidos_cfg = cargar_configuracion(os.path.join(ruta_base, "data", "sonidos.json"))

    pantalla = inicializar_ventana(config["ventana"])
    ancho_p = pantalla.get_width()
    alto_p = pantalla.get_height()

    recursos_graficos = cargar_recursos_graficos(config["ventana"])
    fuentes = cargar_fuentes(estilo["fuentes"])
    fuente_botones = fuentes["subtitulo"]

    recursos = {
        "pantalla": pantalla,
        "config": config,
        "estilo": estilo,
        "layout": layout,
        "sonidos_cfg": sonidos_cfg,
        "recursos_graficos": recursos_graficos,
        "fuentes": fuentes,
        "botones_menu": generar_botones_menu(ancho_p, alto_p, layout["menu_principal"], estilo["colores"], fuente_botones),
        "botones_seleccion": generar_botones_seleccion(ancho_p, alto_p, layout["seleccion"], fuentes, estilo["colores"]),
        "ui_usuarios": inicializar_ui_usuarios(ancho_p, alto_p, fuentes, estilo["colores"]),
        "botones_config": generar_botones_config(ancho_p, alto_p, layout["configuracion"], estilo["colores"], fuente_botones, config["juego"]),
        "botones_ranking": generar_botones_ranking(ancho_p, alto_p, layout["ranking"], estilo["colores"], fuente_botones),
        "botones_vol_juego": generar_botones_vol_juego(ancho_p, alto_p, layout["juego_ui"]["controles_volumen"], estilo["colores"], fuentes["info"]),
        "preguntas_base": cargar_preguntas(os.path.join(ruta_base, "preguntas_juego.csv")),
        "ruta_base": ruta_base
    }
    return recursos

def gestionar_musica_segun_estado(estado_global, sonidos_cfg):
    """Lógica de música basada en el estado."""
    configuracion_musica = sonidos_cfg["musica"]
    pantalla_actual = estado_global["pantalla"]
    musica_actual = estado_global["musica_actual"]
    control_volumen = estado_global["volumen"]

    es_menu = (pantalla_actual == "login" or pantalla_actual == "registro" or 
               pantalla_actual == "menu" or pantalla_actual == "seleccion" or 
               pantalla_actual == "configuracion" or pantalla_actual == "ranking")

    if es_menu == True:
        if musica_actual != "menu":
            actualizar_volumen_global(control_volumen)
            gestionar_musica(configuracion_musica["archivo_menu"], volumen=pygame.mixer.music.get_volume())
            estado_global["musica_actual"] = "menu"
    elif pantalla_actual == "juego":
        if musica_actual != "juego":
            actualizar_volumen_global(control_volumen)
            gestionar_musica(configuracion_musica["archivo_juego"], volumen=pygame.mixer.music.get_volume())
            estado_global["musica_actual"] = "juego"

def procesar_logica_por_estado(recursos, estado_global, pos_mouse, eventos):
    """Maneja la transición de pantallas."""
    pantalla_actual = estado_global["pantalla"]
    
    if pantalla_actual == "login":
        prox, datos_u = mostrar_pantalla_login(recursos["pantalla"], recursos["recursos_graficos"], recursos["fuentes"], recursos["estilo"]["colores"], recursos["ui_usuarios"]["login"], pos_mouse, eventos)
        if prox == "menu":
            estado_global["usuario"] = datos_u
            estado_global["pantalla"] = "menu"
        elif prox == "registro":
            estado_global["pantalla"] = "registro"

    elif pantalla_actual == "registro":
        prox = mostrar_pantalla_registro(recursos["pantalla"], recursos["recursos_graficos"], recursos["fuentes"], recursos["estilo"]["colores"], recursos["ui_usuarios"]["registro"], pos_mouse, eventos)
        if prox == "login":
            estado_global["pantalla"] = "login"

    elif pantalla_actual == "menu":
        prox_pantalla = mostrar_menu(recursos["pantalla"], recursos["recursos_graficos"], recursos["fuentes"], recursos["estilo"]["colores"], recursos["botones_menu"], pos_mouse, eventos, estado_global["volumen"])
        if prox_pantalla == "juego":
            estado_global["seleccion"]["tematica"] = ""
            estado_global["seleccion"]["dificultad"] = ""
            estado_global["pantalla"] = "seleccion"
        elif prox_pantalla == "configuracion":
            estado_global["pantalla"] = "configuracion"
        elif prox_pantalla == "ranking":
            estado_global["pantalla"] = "ranking"
        elif prox_pantalla == "salir":
            estado_global["flag_run"] = False

    elif pantalla_actual == "seleccion":
        resultado = mostrar_seleccion(recursos["pantalla"], recursos["recursos_graficos"], recursos["fuentes"], recursos["estilo"]["colores"], recursos["botones_seleccion"], pos_mouse, eventos, estado_global["seleccion"])
        if resultado == "menu":
            estado_global["pantalla"] = "menu"
        elif resultado == "iniciar_juego":
            datos_mensajes = cargar_configuracion(os.path.join(recursos["ruta_base"], "data", "mensajes.json"))
            nuevo_estado_juego = inicializar_estado_juego(recursos["preguntas_base"], recursos["config"]["juego"], estado_global["seleccion"]["tematica"], estado_global["seleccion"]["dificultad"])
            nuevo_estado_juego["mensajes_motivadores"] = datos_mensajes["motivadores"]
            estado_global["estado_juego_datos"] = nuevo_estado_juego
            estado_global["pantalla"] = "juego"

    elif pantalla_actual == "juego":
        resultado = mostrar_pantalla_juego(recursos["pantalla"], recursos["recursos_graficos"], recursos["fuentes"], recursos["estilo"]["colores"], estado_global["estado_juego_datos"], pos_mouse, eventos, recursos["botones_vol_juego"], estado_global["volumen"], recursos["layout"]["juego_ui"]["layout"])
        if resultado == "menu":
            estado_global["pantalla"] = "menu"
        elif resultado == "podio":
            actualizar_puntaje_maximo(estado_global["usuario"], estado_global["estado_juego_datos"]["puntaje"])
            estado_global["pantalla"] = "menu"

    elif pantalla_actual == "configuracion":
        prox = mostrar_configuracion(recursos["pantalla"], recursos["recursos_graficos"], recursos["fuentes"], recursos["estilo"]["colores"], recursos["botones_config"], pos_mouse, eventos, recursos["config"], recursos["layout"]["configuracion"])
        if prox == "menu":
            estado_global["pantalla"] = "menu"

    elif pantalla_actual == "ranking":
        prox = mostrar_ranking(recursos["pantalla"], recursos["recursos_graficos"], recursos["fuentes"], recursos["estilo"]["colores"], recursos["botones_ranking"], pos_mouse, eventos, recursos["layout"]["ranking"])
        if prox == "menu":
            estado_global["pantalla"] = "menu"
