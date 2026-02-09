import pygame
import sys
import os
import json

# Importar módulos propios
from constantes import ANCHO_VENTANA, ALTO_VENTANA, PROJ_ROOT, COLORES
from recursos import cargar_fondos, cargar_fuentes
from pantallas import (
    mostrar_pantalla_seleccion,
    mostrar_pantalla_ajustes,
    mostrar_pantalla_guia,
    mostrar_pantalla_estadisticas
)
from juego import iniciar_juego
from manejo_usuarios import mostrar_pantalla_registro, mostrar_pantalla_login
from botones import crear_boton_texto, dibujar_boton
from musica import (
    iniciar_musica,
    iniciar_musica_partida,
    detener_musica,
    get_volumen,
    set_volumen,
    subir_volumen,
    bajar_volumen
)

# ---------------- VARIABLES GLOBALES ----------------
usuario_actual = None
ruta_json_usuarios = ""
menu_fondo_escalado = None
ruta_config = ""


def abrir_juego():
    """Función principal que inicia y ejecuta el juego."""
    global usuario_actual, ruta_json_usuarios, menu_fondo_escalado, ruta_config

    pygame.init()
    pygame.mixer.init()

    VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Desafio Mental")

    set_volumen(0.5)
    iniciar_musica()

    ruta_json_usuarios = os.path.join(PROJ_ROOT, "datos_usuario.json")
    # Usar ruta absoluta basada en la ubicación de este archivo
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_config = os.path.join(directorio_actual, "config.json")

    # ---------------- FONDOS Y FUENTES ----------------
    fondos = cargar_fondos()
    menu_fondo_escalado = fondos['menu']
    fondo_juego_escalado = fondos['juego']
    
    fuentes = cargar_fuentes()
    fuente_titulo = fuentes['titulo']
    fuente_ajustes = fuentes['ajustes']
    fuente_info = fuentes['info']

    # ---------------- ESTADOS Y BOTONES ----------------
    estado_actual = "pre_menu"
    nombre_jugador = ""
    dificultad_seleccionada = ""
    tematica_seleccionada = ""

    # Botones (usando constantes de colores)
    boton_comenzar_juego = crear_boton_texto("Comenzar Juego", fuente_ajustes, COLORES["BLANCO"], COLORES["VERDE"], COLORES["VERDE_OSCURO"], COLORES["VERDE_CLARO"], (50, 300), (250, 80))
    boton_guia = crear_boton_texto("Guía", fuente_ajustes, COLORES["BLANCO"], COLORES["AZUL"], COLORES["AZUL_OSCURO"], COLORES["AZUL_CLARO"], (50, 420), (250, 80))
    boton_estadisticas = crear_boton_texto("Estadísticas", fuente_ajustes, COLORES["BLANCO"], COLORES["MAGENTA"], COLORES["MAGENTA_OSCURO"], COLORES["MAGENTA_CLARO"], (50, 540), (250, 80))
    boton_ajustes = crear_boton_texto("Ajustes", fuente_ajustes, COLORES["BLANCO"], COLORES["AMARILLO"], COLORES["AMARILLO_OSCURO"], COLORES["AMARILLO_CLARO"], (1100, 300), (250, 80))
    boton_salir = crear_boton_texto("Salir", fuente_ajustes, COLORES["BLANCO"], COLORES["ROJO"], COLORES["ROJO_OSCURO"], COLORES["ROJO_CLARO"], (1100, 420), (250, 80))
    boton_bajar_volumen = crear_boton_texto("-", fuente_info, COLORES["BLANCO"], COLORES["ROJO_CLARO"], COLORES["ROJO_OSCURO"], (255, 50, 50), (1100, 540), (50, 50))
    boton_subir_volumen = crear_boton_texto("+", fuente_info, COLORES["BLANCO"], COLORES["VERDE_CLARO"], COLORES["VERDE_OSCURO"], (50, 255, 50), (1160, 540), (50, 50))
    boton_login = crear_boton_texto("Iniciar Sesión", fuente_ajustes, COLORES["BLANCO"], COLORES["AZUL"], COLORES["AZUL_OSCURO"], COLORES["AZUL_CLARO"], (450, 400), (250, 80))
    boton_registro = crear_boton_texto("Registrarse", fuente_ajustes, COLORES["BLANCO"], COLORES["VERDE"], COLORES["VERDE_OSCURO"], COLORES["VERDE_CLARO"], (750, 400), (250, 80))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if estado_actual == "pre_menu":
                    if boton_login["Rectangulo"].collidepoint(mouse_pos): estado_actual = "login"
                    if boton_registro["Rectangulo"].collidepoint(mouse_pos): estado_actual = "registro"
                elif estado_actual == "menu":
                    if boton_comenzar_juego["Rectangulo"].collidepoint(mouse_pos): estado_actual = "seleccion_juego"
                    if boton_guia["Rectangulo"].collidepoint(mouse_pos): estado_actual = "guia"
                    if boton_estadisticas["Rectangulo"].collidepoint(mouse_pos): estado_actual = "estadisticas"
                    if boton_ajustes["Rectangulo"].collidepoint(mouse_pos): estado_actual = "ajustes"
                    if boton_salir["Rectangulo"].collidepoint(mouse_pos): pygame.quit(); sys.exit()
                    if boton_bajar_volumen["Rectangulo"].collidepoint(mouse_pos): set_volumen(bajar_volumen())
                    if boton_subir_volumen["Rectangulo"].collidepoint(mouse_pos): set_volumen(subir_volumen())

        # ---------------- DIBUJO DE ESTADOS ----------------
        if estado_actual == "pre_menu":
            VENTANA.blit(menu_fondo_escalado, (0, 0))
            dibujar_boton(VENTANA, boton_login)
            dibujar_boton(VENTANA, boton_registro)

        elif estado_actual == "menu":
            if not pygame.mixer.music.get_busy(): iniciar_musica()
            VENTANA.blit(menu_fondo_escalado, (0, 0))
            
            if nombre_jugador:
                mensaje = fuente_info.render(f"¡Bienvenido, {nombre_jugador}!", True, (255, 255, 0))
                VENTANA.blit(mensaje, (ANCHO_VENTANA // 2 - mensaje.get_width() // 2, 10))

            volumen_porcentaje = int(get_volumen() * 100)
            texto_volumen = fuente_info.render(f"Volumen: {volumen_porcentaje}%", True, (255, 255, 255))
            VENTANA.blit(texto_volumen, (ANCHO_VENTANA - 250, 25))

            dibujar_boton(VENTANA, boton_comenzar_juego)
            dibujar_boton(VENTANA, boton_guia)
            dibujar_boton(VENTANA, boton_ajustes)
            dibujar_boton(VENTANA, boton_estadisticas)
            dibujar_boton(VENTANA, boton_salir)
            dibujar_boton(VENTANA, boton_bajar_volumen)
            dibujar_boton(VENTANA, boton_subir_volumen)

        # ... (Resto de estados: registro, login, juego, etc. se mantienen igual)
        elif estado_actual == "registro":
            nuevo_estado, usuario_obtenido = mostrar_pantalla_registro(VENTANA, ANCHO_VENTANA, ALTO_VENTANA, fuente_titulo, fuente_ajustes, fuente_info, crear_boton_texto, dibujar_boton, ruta_json_usuarios)
            if nuevo_estado == "menu": usuario_actual = usuario_obtenido; nombre_jugador = usuario_obtenido; estado_actual = "menu"
            else: estado_actual = nuevo_estado
        elif estado_actual == "login":
            nuevo_estado, usuario_obtenido = mostrar_pantalla_login(VENTANA, ANCHO_VENTANA, ALTO_VENTANA, fuente_titulo, fuente_ajustes, fuente_info, crear_boton_texto, dibujar_boton, ruta_json_usuarios)
            if nuevo_estado == "menu": usuario_actual = usuario_obtenido; nombre_jugador = usuario_obtenido; estado_actual = "menu"
            else: estado_actual = nuevo_estado
        elif estado_actual == "seleccion_juego":
            resultado_seleccion = mostrar_pantalla_seleccion(VENTANA)
            if resultado_seleccion: dificultad_seleccionada, tematica_seleccionada = resultado_seleccion; detener_musica(); iniciar_musica_partida(); estado_actual = "juego"
            else: estado_actual = "menu"
        elif estado_actual == "juego":
            # Cargar config para saber si Modo TDAH está activo
            modo_tdah = False
            if os.path.exists(ruta_config):
                try:
                    with open(ruta_config, 'r', encoding='utf-8') as f:
                        cfg = json.load(f)
                        modo_tdah = cfg.get("modo_tdah", False)
                except Exception as e:
                    print(f"Error al cargar config: {e}")

            nuevo_estado, _ = iniciar_juego(VENTANA, dificultad_seleccionada, tematica_seleccionada, get_volumen(), ANCHO_VENTANA, ALTO_VENTANA, fondo_juego_escalado, nombre_jugador, ruta_json_usuarios, modo_tdah)
            if nuevo_estado == "menu": detener_musica(); iniciar_musica()
            estado_actual = nuevo_estado
        elif estado_actual == "ajustes":
            estado_actual = mostrar_pantalla_ajustes(VENTANA, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA, ruta_config)
        elif estado_actual == "guia":
            estado_actual = mostrar_pantalla_guia(VENTANA, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA)
        elif estado_actual == "estadisticas":
            estado_actual = mostrar_pantalla_estadisticas(VENTANA, nombre_jugador, ruta_json_usuarios, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA)

        pygame.display.update()