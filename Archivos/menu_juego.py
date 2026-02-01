import pygame
import sys
import os

from logica_juego import (
    mostrar_pantalla_seleccion,
    iniciar_juego,
    mostrar_pantalla_ajustes,
    mostrar_pantalla_guia,
    mostrar_pantalla_estadisticas
)
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

ANCHO_VENTANA = 1400
ALTO_VENTANA = 800
PROJ_ROOT = os.path.dirname(os.path.dirname(__file__))


def main():
    global usuario_actual, ruta_json_usuarios, menu_fondo_escalado

    pygame.init()
    pygame.mixer.init()

    VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Desafio Mental")

    set_volumen(0.5)
    iniciar_musica()

    ruta_json_usuarios = os.path.join(PROJ_ROOT, "datos_usuario.json")

   # ---------------- FONDOS (MÉTODO ORIGINAL RESTAURADO) ----------------
    nombre_archivo_fondo = "menu_ia.png"
    nombre_archivo_juego = "juego_ia.png" # Nombre del fondo de aventura

    # --- CARGA FONDO MENÚ (Tu lógica exacta) ---
    ruta_posible = os.path.join(os.path.dirname(__file__), "Bocetos", nombre_archivo_fondo)
    if os.path.exists(ruta_posible):
        menu_fondo = pygame.image.load(ruta_posible)
    else:
        ruta_alternativa = os.path.join(PROJ_ROOT, "Bocetos", nombre_archivo_fondo)
        if os.path.exists(ruta_alternativa):
            menu_fondo = pygame.image.load(ruta_alternativa)
        else:
            menu_fondo = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
            menu_fondo.fill((50, 50, 50))

    menu_fondo_escalado = pygame.transform.scale(menu_fondo, (ANCHO_VENTANA, ALTO_VENTANA))

    # --- CARGA FONDO JUEGO (Mismo método que el anterior) ---
    ruta_juego_posible = os.path.join(os.path.dirname(__file__), "Bocetos", nombre_archivo_juego)
    if os.path.exists(ruta_juego_posible):
        fondo_juego = pygame.image.load(ruta_juego_posible)
    else:
        # Intento con ruta alternativa usando PROJ_ROOT
        ruta_juego_alternativa = os.path.join(PROJ_ROOT, "Bocetos", nombre_archivo_juego)
        if os.path.exists(ruta_juego_alternativa):
            fondo_juego = pygame.image.load(ruta_juego_alternativa)
        else:
            # Fallback a juego.png por si acaso
            ruta_juego_viejo = os.path.join(os.path.dirname(__file__), "Bocetos", "juego.png")
            if os.path.exists(ruta_juego_viejo):
                fondo_juego = pygame.image.load(ruta_juego_viejo)
            else:
                fondo_juego = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
                fondo_juego.fill((30, 30, 30))

    fondo_juego_escalado = pygame.transform.scale(fondo_juego, (ANCHO_VENTANA, ALTO_VENTANA))
    # ---------------- FUENTES ----------------
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_ajustes = pygame.font.Font(None, 36)
    fuente_info = pygame.font.Font(None, 28)

    # ---------------- ESTADOS Y BOTONES ----------------
    estado_actual = "pre_menu"
    nombre_jugador = ""
    dificultad_seleccionada = ""
    tematica_seleccionada = ""

    # Botones (mantengo tus coordenadas originales)
    boton_comenzar_juego = crear_boton_texto("Comenzar Juego", fuente_ajustes, (255, 255, 255), (0, 150, 0), (0, 100, 0), (0, 200, 0), (50, 300), (250, 80))
    boton_guia = crear_boton_texto("Guía", fuente_ajustes, (255, 255, 255), (0, 0, 255), (0, 0, 139), (0, 0, 200), (50, 420), (250, 80))
    boton_estadisticas = crear_boton_texto("Estadísticas", fuente_ajustes, (255, 255, 255), (255, 0, 255), (150, 0, 150), (255, 100, 255), (50, 540), (250, 80))
    boton_ajustes = crear_boton_texto("Ajustes", fuente_ajustes, (255, 255, 255), (150, 150, 0), (100, 100, 0), (200, 200, 0), (1100, 300), (250, 80))
    boton_salir = crear_boton_texto("Salir", fuente_ajustes, (255, 255, 255), (150, 0, 0), (100, 0, 0), (200, 0, 0), (1100, 420), (250, 80))
    boton_bajar_volumen = crear_boton_texto("-", fuente_info, (255, 255, 255), (200, 0, 0), (100, 0, 0), (255, 50, 50), (1100, 540), (50, 50))
    boton_subir_volumen = crear_boton_texto("+", fuente_info, (255, 255, 255), (0, 200, 0), (0, 100, 0), (50, 255, 50), (1160, 540), (50, 50))
    boton_login = crear_boton_texto("Iniciar Sesión", fuente_ajustes, (255, 255, 255), (0, 0, 150), (0, 0, 80), (0, 0, 200), (450, 400), (250, 80))
    boton_registro = crear_boton_texto("Registrarse", fuente_ajustes, (255, 255, 255), (0, 150, 0), (0, 80, 0), (0, 200, 0), (750, 400), (250, 80))

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
            # Comentamos el render del título porque la imagen ya lo tiene
            # titulo = fuente_titulo.render("Desafio Mental", True, (255, 0, 255))
            # VENTANA.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 100))
            dibujar_boton(VENTANA, boton_login)
            dibujar_boton(VENTANA, boton_registro)

        elif estado_actual == "menu":
            if not pygame.mixer.music.get_busy(): iniciar_musica()
            VENTANA.blit(menu_fondo_escalado, (0, 0))
            
            # (Aquí también podrías comentar la imagen de 'titulo.png' si la estabas usando)
            
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
            nuevo_estado, _ = iniciar_juego(VENTANA, dificultad_seleccionada, tematica_seleccionada, get_volumen(), ANCHO_VENTANA, ALTO_VENTANA, fondo_juego_escalado, nombre_jugador, ruta_json_usuarios)
            if nuevo_estado == "menu": detener_musica(); iniciar_musica()
            estado_actual = nuevo_estado
        elif estado_actual == "ajustes":
            estado_actual = mostrar_pantalla_ajustes(VENTANA)
        elif estado_actual == "guia":
            estado_actual = mostrar_pantalla_guia(VENTANA, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA)
        elif estado_actual == "estadisticas":
            estado_actual = mostrar_pantalla_estadisticas(VENTANA, nombre_jugador, ruta_json_usuarios, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA)

        pygame.display.update()

if __name__ == "__main__":
    main()