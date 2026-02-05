"""
Módulo para las pantallas de UI del juego (selección, ajustes, guía, estadísticas)
"""
import pygame
import sys
import json
import os
from botones import crear_boton_texto, dibujar_boton
from constantes import TEMATICAS, COLORES, ANCHO_VENTANA, ALTO_VENTANA


def mostrar_pantalla_seleccion(ventana):
  
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_opcion = pygame.font.Font(None, 32)
    fuente_info = pygame.font.Font(None, 24)
    
    botones_dificultad = [
        crear_boton_texto("Fácil", fuente_opcion, COLORES["BLANCO"], COLORES["VERDE"], 
                         COLORES["VERDE_OSCURO"], COLORES["VERDE_CLARO"], (50, 250), (150, 60)),
        crear_boton_texto("Pro", fuente_opcion, COLORES["BLANCO"], COLORES["NARANJA"], 
                         COLORES["NARANJA_OSCURO"], COLORES["NARANJA_CLARO"], (400, 250), (150, 60)),
        crear_boton_texto("Experto", fuente_opcion, COLORES["BLANCO"], COLORES["ROJO"], 
                         COLORES["ROJO_OSCURO"], COLORES["ROJO_CLARO"], (750, 250), (150, 60))
    ]
    
    botones_tematica = []
    y_pos = 450
    for tematica in TEMATICAS:
        boton = crear_boton_texto(tematica, fuente_opcion, COLORES["BLANCO"], COLORES["AZUL"], 
                                 COLORES["AZUL_OSCURO"], COLORES["GRIS_CLARO"], (50, y_pos), (300, 60))
        botones_tematica.append(boton)
        y_pos += 80

    dificultad_elegida = None
    tematica_elegida = None
    
    boton_atras = crear_boton_texto("Atrás", fuente_info, COLORES["BLANCO"], COLORES["GRIS"], 
                                   COLORES["GRIS_OSCURO"], COLORES["GRIS_CLARO"], (1300, 700), (150, 50))

    while not (dificultad_elegida and tematica_elegida):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if boton_atras["Rectangulo"].collidepoint(mouse_pos):
                    return None
                for boton in botones_dificultad:
                    if boton["Rectangulo"].collidepoint(mouse_pos):
                        dificultad_elegida = boton["Texto"]
                for boton in botones_tematica:
                    if boton["Rectangulo"].collidepoint(mouse_pos):
                        tematica_elegida = boton["Texto"]
        
        ventana.fill(COLORES["FONDO_OSCURO"])
        
        titulo_dificultad = fuente_titulo.render("Elige la Dificultad:", True, COLORES["BLANCO"])
        ventana.blit(titulo_dificultad, (50, 150))
        
        for boton in botones_dificultad:
            dibujar_boton(ventana, boton)
        
        titulo_tematica = fuente_titulo.render("Elige la Temática:", True, COLORES["BLANCO"])
        ventana.blit(titulo_tematica, (50, 400))
        
        for boton in botones_tematica:
            dibujar_boton(ventana, boton)
        
        dibujar_boton(ventana, boton_atras)
        
        pygame.display.update()
    
    return (dificultad_elegida, tematica_elegida)


def mostrar_pantalla_ajustes(ventana):

    return "menu"


def mostrar_pantalla_guia(ventana, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA):
   
    
    parrafos = [
        ("--- GUÍA DEL JUEGO: COMPLETA LA FRASE ---", COLORES["CYAN"], 60),
        ("Este juego pone a prueba tu conocimiento con frases populares,\ncultura general y deportes.\nTu misión: completar correctamente la frase\no responder bien la pregunta.", COLORES["BLANCO"], 40),
        
        ("1️⃣ Inicio del juego:", COLORES["NARANJA_TEXTO"], 50),
        ("Al iniciar, elegís una temática y una dificultad.\nTemáticas: Frases populares, Cultura general, Deportes.\nDificultades: Fácil, Pro y Experto.", COLORES["BLANCO"], 40),
        
        ("2️⃣ Desarrollo de la partida:", COLORES["NARANJA_TEXTO"], 50),
        ("Se te harán 12 preguntas según la temática y dificultad elegidas.\n\n- Fácil: 4 opciones.\n- Pro: 4 opciones.\n- Experto: sin opciones, escribís toda la frase.", COLORES["BLANCO"], 40),
        
        ("3️⃣ Cómo responder:", COLORES["NARANJA_TEXTO"], 50),
        ("- En modos Fácil/Pro, respondés con la letra (a, b, c o d).\n- En Experto, escribís la frase completa.\n- Si acertás, sumás puntos.\n   ✔ Fácil: +1 punto | Pro: +2 puntos | Experto: +5 puntos", COLORES["BLANCO"], 40),
        
        ("4️⃣ Resultados y final:", COLORES["NARANJA_TEXTO"], 50),
        ("Al terminar las 12 preguntas, verás:\n\n- Tus aciertos y errores.\n- Tu puntaje final guardado en tu perfil.", COLORES["BLANCO"], 40),
        
        ("¡Listo! Ya sabés cómo se juega.", COLORES["CYAN"], 60),
    ]
    
    indice_parrafo = 0
    reloj = pygame.time.Clock()
    
    while indice_parrafo < len(parrafos):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    indice_parrafo += 1
                elif evento.key == pygame.K_ESCAPE:
                    return "menu"
        
        ventana.blit(menu_fondo_escalado, (0, 0))
        
        fuente_titulo_guia = pygame.font.Font(None, 45)
        titulo = fuente_titulo_guia.render("GUÍA DEL JUEGO", True, COLORES["CYAN"])
        ventana.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 280))
        
        if indice_parrafo < len(parrafos):
            texto, color, tamaño = parrafos[indice_parrafo]
            fuente = pygame.font.Font(None, tamaño)
            
            lineas = texto.split('\n')
            y_offset = 350
            
            for linea in lineas:
                if linea.strip():
                    superficie_texto = fuente.render(linea, True, color)
                    x_centro = ANCHO_VENTANA // 2 - superficie_texto.get_width() // 2
                    ventana.blit(superficie_texto, (x_centro, y_offset))
                y_offset += tamaño + 15
        
        fuente_info = pygame.font.Font(None, 30)
        progreso = fuente_info.render(f"ENTER para continuar... ({indice_parrafo + 1}/{len(parrafos)})", True, COLORES["NARANJA_TEXTO"])
        ventana.blit(progreso, (ANCHO_VENTANA // 2 - progreso.get_width() // 2, ALTO_VENTANA - 70))
        
        fuente_escape = pygame.font.Font(None, 28)
        escape_texto = fuente_escape.render("ESC para volver al menú", True, COLORES["NARANJA_TEXTO"])
        ventana.blit(escape_texto, (ANCHO_VENTANA // 2 - escape_texto.get_width() // 2, ALTO_VENTANA - 35))
        
        pygame.display.update()
        reloj.tick(60)
    
    return "menu"


def mostrar_pantalla_estadisticas(ventana, nombre_jugador, ruta_json_usuarios, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA):
   
    
    reloj = pygame.time.Clock()
    
    while True:
        try:
            with open(ruta_json_usuarios, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            datos = {}
        
        estadisticas = datos.get(nombre_jugador, {}).get("estadisticas", {})
        total_puntos = estadisticas.get("total_puntos", 0)
        ultimo_puntaje = estadisticas.get("ultimo_puntaje", 0)
        partidas_jugadas = estadisticas.get("partidas_jugadas", 0)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_RETURN:
                    return "menu"
        
        # Dibujamos el fondo
        ventana.blit(menu_fondo_escalado, (0, 0))
        
        # Título de la pantalla
        fuente_titulo = pygame.font.Font(None, 70)
        titulo = fuente_titulo.render("ESTADÍSTICAS", True, COLORES["CYAN"])
        ventana.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 280))
        
        fuente_info_normal = pygame.font.Font(None, 50)
        
        # Textos de estadísticas
        total_texto = fuente_info_normal.render(f"Puntos Totales: {total_puntos}", True, COLORES["AMARILLO_TEXTO"])
        ventana.blit(total_texto, (ANCHO_VENTANA // 2 - total_texto.get_width() // 2, 380))
        
        ultimo_texto = fuente_info_normal.render(f"Último Puntaje: {ultimo_puntaje}", True, COLORES["NARANJA_TEXTO"])
        ventana.blit(ultimo_texto, (ANCHO_VENTANA // 2 - ultimo_texto.get_width() // 2, 460))
        
        partidas_texto = fuente_info_normal.render(f"Partidas Jugadas: {partidas_jugadas}", True, (200, 100, 255))
        ventana.blit(partidas_texto, (ANCHO_VENTANA // 2 - partidas_texto.get_width() // 2, 540))
        
        # Instrucciones al pie
        fuente_instrucciones = pygame.font.Font(None, 32)
        instrucciones = fuente_instrucciones.render("Presioná ENTER o ESC para volver al menú", True, COLORES["NARANJA_TEXTO"])
        ventana.blit(instrucciones, (ANCHO_VENTANA // 2 - instrucciones.get_width() // 2, ALTO_VENTANA - 60))
        
        pygame.display.update()
        reloj.tick(60)
