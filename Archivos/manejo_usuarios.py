import json
import os
import pygame
import sys


def cargar_datos_usuario(ruta_json):
    """Carga los datos de usuarios desde el archivo JSON"""
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except json.JSONDecodeError:
            return {}
    return {}

def guardar_datos_usuario(ruta_json, datos):
    """Guarda los datos de usuarios en el archivo JSON"""
    with open(ruta_json, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)



def mostrar_pantalla_registro(ventana, ANCHO, ALTO, fuente_titulo, fuente_ajustes, fuente_info, crear_boton_texto, dibujar_boton, ruta_json):
    
    texto_usuario = ""
    texto_contrasena = ""
    texto_confirmar = ""
    input_activo_usuario = False
    input_activo_contrasena = False
    input_activo_confirmar = False
    mensaje_error = ""

    input_box_usuario = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 - 150, 300, 50)
    input_box_contrasena = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 - 50, 300, 50)
    input_box_confirmar = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 50, 300, 50)
    
    boton_registro = crear_boton_texto(
        "Registrarse", fuente_ajustes, (255, 255, 255), (0, 150, 0), (0, 80, 0), (0, 200, 0),
        (ANCHO // 2 - 150, ALTO // 2 + 150), (300, 70)
    )
    boton_volver = crear_boton_texto(
        "Volver", fuente_ajustes, (255, 255, 255), (150, 0, 0), (80, 0, 0), (200, 0, 0),
        (ANCHO // 2 - 150, ALTO // 2 + 250), (300, 70)
    )

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_box_usuario.collidepoint(evento.pos):
                    input_activo_usuario = True
                    input_activo_contrasena = False
                    input_activo_confirmar = False
                elif input_box_contrasena.collidepoint(evento.pos):
                    input_activo_contrasena = True
                    input_activo_usuario = False
                    input_activo_confirmar = False
                elif input_box_confirmar.collidepoint(evento.pos):
                    input_activo_confirmar = True
                    input_activo_usuario = False
                    input_activo_contrasena = False
                else:
                    input_activo_usuario = False
                    input_activo_contrasena = False
                    input_activo_confirmar = False
                
                if boton_registro["Rectangulo"].collidepoint(evento.pos):
                    if not texto_usuario or not texto_contrasena or not texto_confirmar:
                        mensaje_error = "Completa todos los campos."
                    elif texto_contrasena != texto_confirmar:
                        mensaje_error = "Las contraseñas no coinciden."
                    else:
                        datos_usuarios = cargar_datos_usuario(ruta_json)
                        if texto_usuario in datos_usuarios:
                            mensaje_error = "El usuario ya existe."
                        else:
                            datos_usuarios[texto_usuario] = {
                                "contrasena": texto_contrasena,
                                "estadisticas": {
                                    "total_puntos": 0,
                                    "ultimo_puntaje": 0,
                                    "partidas_jugadas": 0
                                }
                            }
                            guardar_datos_usuario(ruta_json, datos_usuarios)
                            return "menu", texto_usuario
                
                if boton_volver["Rectangulo"].collidepoint(evento.pos):
                    return "pre_menu", ""

            if evento.type == pygame.KEYDOWN:
                if input_activo_usuario:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_usuario = texto_usuario[:-1]
                    else:
                        texto_usuario += evento.unicode
                elif input_activo_contrasena:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_contrasena = texto_contrasena[:-1]
                    else:
                        texto_contrasena += evento.unicode
                elif input_activo_confirmar:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_confirmar = texto_confirmar[:-1]
                    else:
                        texto_confirmar += evento.unicode

        ventana.fill((30, 30, 30))
        titulo_texto = fuente_titulo.render("Registrarse", True, (255, 255, 255))
        ventana.blit(titulo_texto, (ANCHO // 2 - titulo_texto.get_width() // 2, 50))

        pygame.draw.rect(ventana, (255, 255, 255) if input_activo_usuario else (100, 100, 100), input_box_usuario, 2)
        pygame.draw.rect(ventana, (255, 255, 255) if input_activo_contrasena else (100, 100, 100), input_box_contrasena, 2)
        pygame.draw.rect(ventana, (255, 255, 255) if input_activo_confirmar else (100, 100, 100), input_box_confirmar, 2)
        
        texto_render_usuario = fuente_info.render(texto_usuario, True, (255, 255, 255))
        ventana.blit(texto_render_usuario, (input_box_usuario.x + 5, input_box_usuario.y + 5))
        
        texto_render_contrasena = fuente_info.render("*" * len(texto_contrasena), True, (255, 255, 255))
        ventana.blit(texto_render_contrasena, (input_box_contrasena.x + 5, input_box_contrasena.y + 5))
        
        texto_render_confirmar = fuente_info.render("*" * len(texto_confirmar), True, (255, 255, 255))
        ventana.blit(texto_render_confirmar, (input_box_confirmar.x + 5, input_box_confirmar.y + 5))

        label_usuario = fuente_info.render("Usuario:", True, (255, 255, 255))
        ventana.blit(label_usuario, (input_box_usuario.x, input_box_usuario.y - 30))
        label_contrasena = fuente_info.render("Contraseña:", True, (255, 255, 255))
        ventana.blit(label_contrasena, (input_box_contrasena.x, input_box_contrasena.y - 30))
        label_confirmar = fuente_info.render("Confirmar:", True, (255, 255, 255))
        ventana.blit(label_confirmar, (input_box_confirmar.x, input_box_confirmar.y - 30))

        if mensaje_error:
            mensaje_error_render = fuente_info.render(mensaje_error, True, (255, 0, 0))
            ventana.blit(mensaje_error_render, (ANCHO // 2 - mensaje_error_render.get_width() // 2, ALTO // 2 + 100))

        dibujar_boton(ventana, boton_registro)
        dibujar_boton(ventana, boton_volver)

        pygame.display.update()

def mostrar_pantalla_login(ventana, ANCHO, ALTO, fuente_titulo, fuente_ajustes, fuente_info, crear_boton_texto, dibujar_boton, ruta_json):
    
    texto_usuario = ""
    texto_contrasena = ""
    input_activo_usuario = False
    input_activo_contrasena = False
    mensaje_error = ""

    input_box_usuario = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 - 100, 300, 50)
    input_box_contrasena = pygame.Rect(ANCHO // 2 - 150, ALTO // 2, 300, 50)
    
    boton_login = crear_boton_texto(
        "Iniciar Sesión", fuente_ajustes, (255, 255, 255), (0, 0, 150), (0, 0, 80), (0, 0, 200),
        (ANCHO // 2 - 150, ALTO // 2 + 100), (300, 70)
    )
    boton_volver = crear_boton_texto(
        "Volver", fuente_ajustes, (255, 255, 255), (150, 0, 0), (80, 0, 0), (200, 0, 0),
        (ANCHO // 2 - 150, ALTO // 2 + 200), (300, 70)
    )

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_box_usuario.collidepoint(evento.pos):
                    input_activo_usuario = True
                    input_activo_contrasena = False
                elif input_box_contrasena.collidepoint(evento.pos):
                    input_activo_contrasena = True
                    input_activo_usuario = False
                else:
                    input_activo_usuario = False
                    input_activo_contrasena = False
                
                if boton_login["Rectangulo"].collidepoint(evento.pos):
                    datos_usuarios = cargar_datos_usuario(ruta_json)
                    if texto_usuario in datos_usuarios and datos_usuarios[texto_usuario]["contrasena"] == texto_contrasena:
                        return "menu", texto_usuario
                    else:
                        mensaje_error = "Usuario o contraseña incorrectos."
                
                if boton_volver["Rectangulo"].collidepoint(evento.pos):
                    return "pre_menu", ""

            if evento.type == pygame.KEYDOWN:
                if input_activo_usuario:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_usuario = texto_usuario[:-1]
                    else:
                        texto_usuario += evento.unicode
                elif input_activo_contrasena:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_contrasena = texto_contrasena[:-1]
                    else:
                        texto_contrasena += evento.unicode

        ventana.fill((30, 30, 30))
        titulo_texto = fuente_titulo.render("Iniciar Sesión", True, (255, 255, 255))
        ventana.blit(titulo_texto, (ANCHO // 2 - titulo_texto.get_width() // 2, 50))

        pygame.draw.rect(ventana, (255, 255, 255) if input_activo_usuario else (100, 100, 100), input_box_usuario, 2)
        pygame.draw.rect(ventana, (255, 255, 255) if input_activo_contrasena else (100, 100, 100), input_box_contrasena, 2)
        
        texto_render_usuario = fuente_info.render(texto_usuario, True, (255, 255, 255))
        ventana.blit(texto_render_usuario, (input_box_usuario.x + 5, input_box_usuario.y + 5))
        
        texto_render_contrasena = fuente_info.render("*" * len(texto_contrasena), True, (255, 255, 255))
        ventana.blit(texto_render_contrasena, (input_box_contrasena.x + 5, input_box_contrasena.y + 5))

        label_usuario = fuente_info.render("Usuario:", True, (255, 255, 255))
        ventana.blit(label_usuario, (input_box_usuario.x, input_box_usuario.y - 30))
        label_contrasena = fuente_info.render("Contraseña:", True, (255, 255, 255))
        ventana.blit(label_contrasena, (input_box_contrasena.x, input_box_contrasena.y - 30))

        if mensaje_error:
            mensaje_error_render = fuente_info.render(mensaje_error, True, (255, 0, 0))
            ventana.blit(mensaje_error_render, (ANCHO // 2 - mensaje_error_render.get_width() // 2, ALTO // 2 + 50))

        dibujar_boton(ventana, boton_login)
        dibujar_boton(ventana, boton_volver)

        pygame.display.update()
