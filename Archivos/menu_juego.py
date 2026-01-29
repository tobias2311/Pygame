import pygame
import sys
import os
from logica_juego import (
    mostrar_pantalla_seleccion, iniciar_juego, mostrar_pantalla_ajustes,
    mostrar_pantalla_guia, mostrar_pantalla_estadisticas
)
from manejo_usuarios import mostrar_pantalla_registro, mostrar_pantalla_login
from botones import crear_boton_texto, dibujar_boton
from musica import iniciar_musica, detener_musica, get_volumen, set_volumen, subir_volumen, bajar_volumen

# Variables globales
usuario_actual = None
ruta_json_usuarios = ""
menu_fondo_escalado = None
ANCHO_VENTANA = 1400
ALTO_VENTANA = 800
PROJ_ROOT = os.path.dirname(os.path.dirname(__file__))

def main():
    global usuario_actual, ruta_json_usuarios, menu_fondo_escalado
    
    pygame.init()
    VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Quiz Game")
    
    ruta_json_usuarios = os.path.join(PROJ_ROOT, "datos_usuario.json")
    
    menu_fondo = pygame.image.load(os.path.join(PROJ_ROOT, "TP PYGAME", "Bocetos", "menu.png")) if os.path.exists(os.path.join(PROJ_ROOT, "TP PYGAME", "Bocetos", "menu.png")) else pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    menu_fondo_escalado = pygame.transform.scale(menu_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
    
    try:
        fondo_juego = pygame.image.load(os.path.join(PROJ_ROOT, "TP PYGAME", "Bocetos", "juego.png")) if os.path.exists(os.path.join(PROJ_ROOT, "TP PYGAME", "Bocetos", "juego.png")) else pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    except:
        fondo_juego = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    fondo_juego_escalado = pygame.transform.scale(fondo_juego, (ANCHO_VENTANA, ALTO_VENTANA))
    
    try:
        nombre_juego_img = pygame.image.load(os.path.join(PROJ_ROOT, "TP PYGAME", "Bocetos", "titulo.png")) if os.path.exists(os.path.join(PROJ_ROOT, "TP PYGAME", "Bocetos", "titulo.png")) else None
        if nombre_juego_img:
            nombre_juego_img = pygame.transform.scale(nombre_juego_img, (600, 200))
    except:
        nombre_juego_img = None
    
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_ajustes = pygame.font.Font(None, 36)
    fuente_info = pygame.font.Font(None, 28)
    
    global usuario_actual
    usuario_actual = None
    
    estado_actual = "pre_menu"
    nombre_jugador = ""
    dificultad_seleccionada = ""
    tematica_seleccionada = ""
    
    boton_comenzar_juego = crear_boton_texto("Comenzar Juego", fuente_ajustes, (255, 255, 255),
                                             (0, 150, 0), (0, 100, 0), (0, 200, 0),
                                             (50, 300), (250, 80))
    boton_guia = crear_boton_texto("Guía", fuente_ajustes, (255, 255, 255),
                                   (0, 0, 255), (0, 0, 139), (0, 0, 200),
                                   (50, 420), (250, 80))
    boton_estadisticas = crear_boton_texto("Estadísticas", fuente_ajustes, (255, 255, 255),
                                          (255, 0, 255), (150, 0, 150), (255, 100, 255),
                                          (50, 540), (250, 80))
    boton_ajustes = crear_boton_texto("Ajustes", fuente_ajustes, (255, 255, 255),
                                     (150, 150, 0), (100, 100, 0), (200, 200, 0),
                                     (1100, 300), (250, 80))
    boton_salir = crear_boton_texto("Salir", fuente_ajustes, (255, 255, 255),
                                   (150, 0, 0), (100, 0, 0), (200, 0, 0),
                                   (1100, 420), (250, 80))
    boton_bajar_volumen = crear_boton_texto("-", fuente_info, (255, 255, 255),
                                           (200, 0, 0), (100, 0, 0), (255, 50, 50),
                                           (1100, 540), (50, 50))
    boton_subir_volumen = crear_boton_texto("+", fuente_info, (255, 255, 255),
                                           (0, 200, 0), (0, 100, 0), (50, 255, 50),
                                           (1160, 540), (50, 50))
    
    boton_login = crear_boton_texto("Iniciar Sesión", fuente_ajustes, (255, 255, 255),
                                   (0, 0, 150), (0, 0, 80), (0, 0, 200),
                                   (450, 400), (250, 80))
    boton_registro = crear_boton_texto("Registrarse", fuente_ajustes, (255, 255, 255),
                                      (0, 150, 0), (0, 80, 0), (0, 200, 0),
                                      (750, 400), (250, 80))
    
    set_volumen(0.5)
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                
                if estado_actual == "pre_menu":
                    if boton_login["Rectangulo"].collidepoint(mouse_pos):
                        estado_actual = "login"
                    if boton_registro["Rectangulo"].collidepoint(mouse_pos):
                        estado_actual = "registro"
                
                elif estado_actual == "menu":
                    if boton_comenzar_juego["Rectangulo"].collidepoint(mouse_pos):
                        estado_actual = "seleccion_juego"
                    if boton_guia["Rectangulo"].collidepoint(mouse_pos):
                        estado_actual = "guia"
                    if boton_estadisticas["Rectangulo"].collidepoint(mouse_pos):
                        estado_actual = "estadisticas"
                    if boton_ajustes["Rectangulo"].collidepoint(mouse_pos):
                        estado_actual = "ajustes"
                    if boton_salir["Rectangulo"].collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    if boton_bajar_volumen["Rectangulo"].collidepoint(mouse_pos):
                        set_volumen(bajar_volumen())
                    if boton_subir_volumen["Rectangulo"].collidepoint(mouse_pos):
                        set_volumen(subir_volumen())
        
        if estado_actual == "pre_menu":
            VENTANA.blit(menu_fondo_escalado, (0, 0))
            
            titulo = fuente_titulo.render("Quiz Game", True, (255, 0, 255))
            VENTANA.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 100))
            
            dibujar_boton(VENTANA, boton_login)
            dibujar_boton(VENTANA, boton_registro)
        
        elif estado_actual == "registro":
            detener_musica()
            nuevo_estado, usuario_obtenido = mostrar_pantalla_registro(
                VENTANA, ANCHO_VENTANA, ALTO_VENTANA, fuente_titulo,
                fuente_ajustes, fuente_info, crear_boton_texto, dibujar_boton, ruta_json_usuarios
            )
            if nuevo_estado == "menu":
                usuario_actual = usuario_obtenido
                nombre_jugador = usuario_obtenido
                iniciar_musica()  # Iniciar música después de registrarse
                estado_actual = "menu"
            else:
                estado_actual = nuevo_estado
        
        elif estado_actual == "login":
            detener_musica()
            nuevo_estado, usuario_obtenido = mostrar_pantalla_login(
                VENTANA, ANCHO_VENTANA, ALTO_VENTANA, fuente_titulo,
                fuente_ajustes, fuente_info, crear_boton_texto, dibujar_boton, ruta_json_usuarios
            )
            if nuevo_estado == "menu":
                usuario_actual = usuario_obtenido
                nombre_jugador = usuario_obtenido
                iniciar_musica()  # Iniciar música después de iniciar sesión
                estado_actual = "menu"
            else:
                estado_actual = nuevo_estado
        
        elif estado_actual == "menu":
            #iniciar_musica_menu()
            VENTANA.blit(menu_fondo_escalado, (0, 0))
            if nombre_juego_img:
                VENTANA.blit(nombre_juego_img, (400, 50))
            if nombre_jugador:
                mensaje_bienvenida = fuente_info.render(f"¡Bienvenido, {nombre_jugador}!", True, (255, 255, 0))
                VENTANA.blit(mensaje_bienvenida, (ANCHO_VENTANA // 2 - mensaje_bienvenida.get_width() // 2, 10))
            volumen_porcentaje = int(get_volumen() * 100)
            volumen_texto = fuente_info.render(f"Volumen: {volumen_porcentaje}%", True, (255, 255, 255))
            VENTANA.blit(volumen_texto, (ANCHO_VENTANA - 250, 25))
            dibujar_boton(VENTANA, boton_comenzar_juego)
            dibujar_boton(VENTANA, boton_guia)
            dibujar_boton(VENTANA, boton_ajustes)
            dibujar_boton(VENTANA, boton_estadisticas)
            dibujar_boton(VENTANA, boton_salir)
            dibujar_boton(VENTANA, boton_bajar_volumen)
            dibujar_boton(VENTANA, boton_subir_volumen)
        
        elif estado_actual == "seleccion_juego":
            resultado_seleccion = mostrar_pantalla_seleccion(VENTANA)
            if resultado_seleccion:
                dificultad_seleccionada, tematica_seleccionada = resultado_seleccion
                estado_actual = "juego"
            else:
                estado_actual = "menu"
        
        elif estado_actual == "juego":
            #iniciar_musica_juego()
            estado_actual, _ = iniciar_juego(VENTANA, dificultad_seleccionada, tematica_seleccionada,
                                             get_volumen(), ANCHO_VENTANA, ALTO_VENTANA, fondo_juego_escalado,
                                             nombre_jugador, ruta_json_usuarios)
        
        elif estado_actual == "ajustes":
            estado_actual = mostrar_pantalla_ajustes(VENTANA)
        
        elif estado_actual == "guia":
            estado_actual = mostrar_pantalla_guia(VENTANA, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA)
        
        elif estado_actual == "estadisticas":
            estado_actual = mostrar_pantalla_estadisticas(VENTANA, nombre_jugador, ruta_json_usuarios, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA)
        
        pygame.display.update()

if __name__ == "__main__":
    main()
