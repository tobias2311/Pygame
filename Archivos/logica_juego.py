import pygame
import sys
import random
import json
import os
from botones import crear_boton_texto, dibujar_boton
from cargar_datos import cargar_preguntas_desde_csv
from musica import subir_volumen, bajar_volumen, set_volumen

def mostrar_pantalla_seleccion(ventana):
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_opcion = pygame.font.Font(None, 32)
    fuente_info = pygame.font.Font(None, 24)
    
    botones_dificultad = [
        crear_boton_texto("Fácil", fuente_opcion, (255, 255, 255), (0, 150, 0), (0, 80, 0), (0, 200, 0), (50, 250), (150, 60)),
        crear_boton_texto("Pro", fuente_opcion, (255, 255, 255), (255, 150, 0), (200, 80, 0), (255, 200, 0), (400, 250), (150, 60)),
        crear_boton_texto("Experto", fuente_opcion, (255, 255, 255), (150, 0, 0), (80, 0, 0), (200, 0, 0), (750, 250), (150, 60))
    ]
    
    tematicas = ["Cultura General", "Frases Deportivas", "Frases Populares"]
    botones_tematica = []
    y_pos = 450
    for tematica in tematicas:
        boton = crear_boton_texto(tematica, fuente_opcion, (255, 255, 255), (0, 0, 255), (0, 0, 139), (128, 128, 128), (50, y_pos), (300, 60))
        botones_tematica.append(boton)
        y_pos += 80

    dificultad_elegida = None
    tematica_elegida = None
    
    boton_atras = crear_boton_texto("Atrás", fuente_info, (255, 255, 255), (100, 100, 100), (50, 50, 50), (150, 150, 150), (1300, 700), (150, 50))

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
        
        ventana.fill((30, 30, 30))
        
        titulo_dificultad = fuente_titulo.render("Elige la Dificultad:", True, (255, 255, 255))
        ventana.blit(titulo_dificultad, (50, 150))
        
        for boton in botones_dificultad:
            dibujar_boton(ventana, boton)
        
        titulo_tematica = fuente_titulo.render("Elige la Temática:", True, (255, 255, 255))
        ventana.blit(titulo_tematica, (50, 400))
        
        for boton in botones_tematica:
            dibujar_boton(ventana, boton)
        
        dibujar_boton(ventana, boton_atras)
        
        pygame.display.update()
    
    return (dificultad_elegida, tematica_elegida)

def iniciar_juego(ventana, dificultad, tematica, volumen_actual, ANCHO_VENTANA, ALTO_VENTANA, fondo_juego_escalado, nombre_jugador="", ruta_json_usuarios=""):
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_info = pygame.font.Font(None, 24)
    fuente_pregunta = pygame.font.Font(None, 50)
    fuente_opciones = pygame.font.Font(None, 36)
    fuente_feedback = pygame.font.Font(None, 48)

    boton_subir_volumen = crear_boton_texto(
        texto="+", fuente=fuente_info, color_texto=(255, 255, 255), color_fondo=(0, 200, 0),
        color_borde=(0, 100, 0), color_fondo_hover=(50, 255, 50), posicion=(ANCHO_VENTANA - 70, 20), dimension=(50, 50)
    )
    boton_bajar_volumen = crear_boton_texto(
        texto="-", fuente=fuente_info, color_texto=(255, 255, 255), color_fondo=(200, 0, 0),
        color_borde=(100, 0, 0), color_fondo_hover=(255, 50, 50), posicion=(ANCHO_VENTANA - 130, 20), dimension=(50, 50)
    )
    boton_salir_juego = crear_boton_texto(
        texto="Salir", fuente=fuente_info, color_texto=(255, 255, 255), color_fondo=(100, 100, 100),
        color_borde=(50, 50, 50), color_fondo_hover=(150, 150, 150), posicion=(ANCHO_VENTANA - 150, ALTO_VENTANA - 70), dimension=(130, 50)
    )

    preguntas_raw = cargar_preguntas_desde_csv()
    preguntas = [p for p in preguntas_raw if p["categoria"].lower() == tematica.lower()]

    if not preguntas:
        return "menu", volumen_actual

    puntaje_total = 0
    num_preguntas = 12
    preguntas_a_usar = random.sample(preguntas, min(num_preguntas, len(preguntas)))
    
    for pregunta in preguntas_a_usar:
        estado_pregunta, nuevo_volumen = mostrar_pregunta(
            ventana, pregunta, dificultad, tematica, volumen_actual, ANCHO_VENTANA, ALTO_VENTANA,
            fondo_juego_escalado, boton_bajar_volumen, boton_subir_volumen, boton_salir_juego
        )
        volumen_actual = nuevo_volumen
        
        if estado_pregunta == "menu":
            return "menu", volumen_actual
        elif estado_pregunta == "correcto":
            puntaje_total += int(pregunta["puntos"])
    
    mostrar_tablero_puntuacion(ventana, puntaje_total, ANCHO_VENTANA, ALTO_VENTANA, nombre_jugador, ruta_json_usuarios)
    
    return "menu", volumen_actual

def mostrar_pregunta(ventana, pregunta, dificultad, tematica, volumen_actual, ANCHO_VENTANA, ALTO_VENTANA,
                     fondo_juego_escalado, boton_bajar_volumen, boton_subir_volumen, boton_salir_juego):
    pygame.key.set_repeat(200, 50)
    
    fuente_pregunta = pygame.font.Font(None, 50)
    fuente_opciones = pygame.font.Font(None, 36)
    fuente_info = pygame.font.Font(None, 24)
    fuente_feedback = pygame.font.Font(None, 48)
    
    respuesta_usuario = ""
    input_activo = False
    
    rect_input = pygame.Rect(0, 200, 300, 50)
    rect_input.centerx = ANCHO_VENTANA // 2

    pregunta_activa = True
    feedback_activo = False
    feedback_texto = ""
    feedback_color = (0, 0, 0)
    feedback_inicio_tiempo = 0
    resultado_pregunta = None
    
    # Crear botones de opciones una sola vez si no es Experto
    botones_opciones = []
    if dificultad in ["Fácil", "Pro"]:
        y_pos_primera_fila = 300 
        y_pos_segunda_fila = 450 
        
        ancho_boton = 350
        alto_boton = 100
        espacio_entre_botones = 120
        ancho_total = (2 * ancho_boton) + espacio_entre_botones
        
        x_pos_columna_1 = (ANCHO_VENTANA // 2) - (ancho_total // 2)
        x_pos_columna_2 = x_pos_columna_1 + ancho_boton + espacio_entre_botones

        posiciones = [
            (x_pos_columna_1, y_pos_primera_fila),
            (x_pos_columna_2, y_pos_primera_fila),
            (x_pos_columna_1, y_pos_segunda_fila),
            (x_pos_columna_2, y_pos_segunda_fila)
        ]
        
        for i, opcion in enumerate(pregunta["opciones"]):
            x_pos, y_pos = posiciones[i]
            boton = crear_boton_texto(opcion, fuente_opciones, (255, 255, 255),
                                      (0, 0, 255), (0, 0, 139), (128, 128, 128),
                                      (x_pos, y_pos), (ancho_boton, alto_boton))
            botones_opciones.append(boton)
    
    while pregunta_activa:
        # Si hay feedback y pasó el tiempo, retornar resultado
        if feedback_activo and (pygame.time.get_ticks() - feedback_inicio_tiempo > 1500):
            return resultado_pregunta, volumen_actual

        # Procesar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir", volumen_actual
            
            # Eventos del mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                
                # Botones de controles (volumen y salir)
                if boton_bajar_volumen["Rectangulo"].collidepoint(mouse_pos):
                    set_volumen(bajar_volumen())
                elif boton_subir_volumen["Rectangulo"].collidepoint(mouse_pos):
                    set_volumen(subir_volumen())
                elif boton_salir_juego["Rectangulo"].collidepoint(mouse_pos):
                    return "menu", volumen_actual
                
                # Responder pregunta (si no hay feedback activo)
                elif not feedback_activo:
                    if dificultad in ["Fácil", "Pro"]:
                        # Verificar clicks en botones de opciones
                        for boton in botones_opciones:
                            if boton["Rectangulo"].collidepoint(mouse_pos):
                                es_correcto = boton["Texto"].lower() == pregunta["respuesta_correcta"].lower()
                                
                                if dificultad == "Fácil":
                                    # En Fácil, mostrar feedback y esperar
                                    feedback_activo = True
                                    resultado_pregunta = "correcto" if es_correcto else "incorrecto"
                                    feedback_texto = "¡Correcto!" if es_correcto else "Incorrecto..."
                                    feedback_color = (0, 255, 0) if es_correcto else (255, 0, 0)
                                    feedback_inicio_tiempo = pygame.time.get_ticks()
                                else:
                                    # En Pro, retornar inmediatamente
                                    resultado_pregunta = "correcto" if es_correcto else "incorrecto"
                                    return resultado_pregunta, volumen_actual
                    
                    elif dificultad == "Experto":
                        # Activar input de texto en Experto
                        if rect_input.collidepoint(evento.pos):
                            input_activo = not input_activo

            # Eventos del teclado (solo para Experto)
            elif evento.type == pygame.KEYDOWN and input_activo:
                if evento.key == pygame.K_BACKSPACE:
                    respuesta_usuario = respuesta_usuario[:-1]
                elif evento.key == pygame.K_RETURN:
                    es_correcto = respuesta_usuario.strip().lower() == pregunta["respuesta_correcta"].lower()
                    return ("correcto" if es_correcto else "incorrecto"), volumen_actual
                else:
                    respuesta_usuario += evento.unicode
        
        # DIBUJADO
        ventana.blit(fondo_juego_escalado, (0, 0))
        
        # Info de dificultad y temática
        info_texto = f"Dificultad: {dificultad} | Temática: {tematica}"
        superficie_info = fuente_info.render(info_texto, True, (255, 255, 255))
        ventana.blit(superficie_info, (10, 10))
        
        # Botones de control (volumen y salir)
        dibujar_boton(ventana, boton_bajar_volumen)
        dibujar_boton(ventana, boton_subir_volumen)
        dibujar_boton(ventana, boton_salir_juego)

        # Texto de la pregunta
        color_pregunta = (255, 255, 0)
        superficie_pregunta = fuente_pregunta.render(pregunta["enunciado"], True, color_pregunta)
        rect_pregunta = superficie_pregunta.get_rect(center=(ANCHO_VENTANA // 2, 150))
        ventana.blit(superficie_pregunta, rect_pregunta)

        # Opciones de respuesta
        if dificultad == "Experto":
            pygame.draw.rect(ventana, (255, 255, 255) if input_activo else (200, 200, 200), rect_input, 2)
            superficie_texto = fuente_opciones.render(respuesta_usuario, True, (255, 255, 255))
            ventana.blit(superficie_texto, (rect_input.x + 5, rect_input.y + 5))
        else:
            # Dibujar botones de opciones para Fácil y Pro
            for boton in botones_opciones:
                dibujar_boton(ventana, boton)

        # Feedback (si está activo)
        if feedback_activo:
            superficie_feedback = fuente_feedback.render(feedback_texto, True, feedback_color)
            rect_feedback = superficie_feedback.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
            ventana.blit(superficie_feedback, rect_feedback)
        
        pygame.display.update()
    
    return "menu", volumen_actual

def mostrar_pantalla_ajustes(ventana):
    return "menu"

def mostrar_pantalla_guia(ventana, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA):
    """Muestra la guía del juego con párrafos que avanzan al presionar Enter"""
    
    parrafos = [
        ("--- GUÍA DEL JUEGO: COMPLETA LA FRASE ---", (0, 255, 255), 70),
        ("Este juego pone a prueba tu conocimiento con frases populares,\ncultura general y deportes.\nTu misión: completar correctamente la frase\no responder bien la pregunta.", (200, 100, 255), 48),
        
        ("1️⃣ Inicio del juego:", (255, 165, 0), 60),
        ("Al iniciar, elegís una temática y una dificultad.\nTemáticas: Frases populares, Cultura general, Deportes.\nDificultades: Fácil, Pro y Experto.", (200, 100, 255), 48),
        
        ("2️⃣ Desarrollo de la partida:", (255, 165, 0), 60),
        ("Se te harán 12 preguntas según la temática y dificultad elegidas.\n\n- Fácil: 4 opciones.\n- Pro: 4 opciones.\n- Experto: sin opciones, escribís toda la frase.", (200, 100, 255), 48),
        
        ("3️⃣ Cómo responder:", (255, 165, 0), 60),
        ("- En modos Fácil/Pro, respondés con la letra (a, b, c o d).\n- En Experto, escribís la frase completa.\n- Si acertás, sumás puntos. Si fallás, se restaran puntos.\n   ✔ Fácil: +1 punto\n   ✔ Pro: +2 puntos\n   ✔ Experto: +5 puntos", (200, 100, 255), 48),
        
        ("4️⃣ Resultados y final del juego:", (255, 165, 0), 60),
        ("Al terminar las 12 preguntas, verás:\n\n- Tus aciertos y errores.\n- Tu puntaje final.\n- El promedio de tiempo que tardaste por pregunta.", (200, 100, 255), 48),
        
        ("¡Listo! Ya sabés cómo se juega.", (0, 255, 255), 60),
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
        
        fuente_titulo_guia = pygame.font.Font(None, 36)
        titulo = fuente_titulo_guia.render("GUÍA DEL JUEGO", True, (0, 255, 255))
        ventana.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 30))
        
        if indice_parrafo < len(parrafos):
            texto, color, tamaño = parrafos[indice_parrafo]
            fuente = pygame.font.Font(None, tamaño)
            
            lineas = texto.split('\n')
            y_offset = 150
            
            for linea in lineas:
                if linea.strip():
                    superficie_texto = fuente.render(linea, True, color)
                    x_centro = ANCHO_VENTANA // 2 - superficie_texto.get_width() // 2
                    ventana.blit(superficie_texto, (x_centro, y_offset))
                y_offset += tamaño + 20
        
        fuente_info = pygame.font.Font(None, 40)
        progreso = fuente_info.render(f"Presioná ENTER para continuar... ({indice_parrafo + 1}/{len(parrafos)})", True, (255, 165, 0))
        ventana.blit(progreso, (ANCHO_VENTANA // 2 - progreso.get_width() // 2, ALTO_VENTANA - 50))
        
        fuente_escape = pygame.font.Font(None, 36)
        escape_texto = fuente_escape.render("ESC para volver al menú", True, (255, 165, 0))
        ventana.blit(escape_texto, (ANCHO_VENTANA // 2 - escape_texto.get_width() // 2, ALTO_VENTANA - 20))
        
        pygame.display.update()
        reloj.tick(60)
    
    return "menu"

def mostrar_pantalla_estadisticas(ventana, nombre_jugador, ruta_json_usuarios, menu_fondo_escalado, ANCHO_VENTANA, ALTO_VENTANA):
    """Muestra las estadísticas del jugador: total de puntos, último puntaje y partidas jugadas"""
    
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
        
        ventana.blit(menu_fondo_escalado, (0, 0))
        
        fuente_titulo = pygame.font.Font(None, 70)
        titulo = fuente_titulo.render("ESTADÍSTICAS", True, (0, 255, 255))
        ventana.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 40))
        
        fuente_info_normal = pygame.font.Font(None, 50)
        
        total_texto = fuente_info_normal.render(f"Puntos Totales: {total_puntos}", True, (255, 255, 0))
        ventana.blit(total_texto, (ANCHO_VENTANA // 2 - total_texto.get_width() // 2, 220))
        
        ultimo_texto = fuente_info_normal.render(f"Último Puntaje: {ultimo_puntaje}", True, (255, 165, 0))
        ventana.blit(ultimo_texto, (ANCHO_VENTANA // 2 - ultimo_texto.get_width() // 2, 330))
        
        partidas_texto = fuente_info_normal.render(f"Partidas Jugadas: {partidas_jugadas}", True, (200, 100, 255))
        ventana.blit(partidas_texto, (ANCHO_VENTANA // 2 - partidas_texto.get_width() // 2, 440))
        
        fuente_instrucciones = pygame.font.Font(None, 32)
        instrucciones = fuente_instrucciones.render("Presioná ENTER o ESC para volver al menú", True, (255, 165, 0))
        ventana.blit(instrucciones, (ANCHO_VENTANA // 2 - instrucciones.get_width() // 2, ALTO_VENTANA - 80))
        
        pygame.display.update()
        reloj.tick(60)

def mostrar_tablero_puntuacion(ventana, puntaje, ANCHO_VENTANA, ALTO_VENTANA, nombre_jugador="", ruta_json_usuarios=""):
    import menu_juego
    
    if not nombre_jugador:
        nombre_jugador = menu_juego.usuario_actual
    if not ruta_json_usuarios:
        ruta_json_usuarios = menu_juego.ruta_json_usuarios
    
    if nombre_jugador and ruta_json_usuarios:
        try:
            if os.path.exists(ruta_json_usuarios):
                with open(ruta_json_usuarios, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
            else:
                datos = {}
            
            if nombre_jugador not in datos:
                datos[nombre_jugador] = {"contrasena": ""}
            
            if "estadisticas" not in datos[nombre_jugador]:
                datos[nombre_jugador]["estadisticas"] = {
                    "total_puntos": 0,
                    "ultimo_puntaje": 0,
                    "partidas_jugadas": 0
                }
            
            stats = datos[nombre_jugador]["estadisticas"]
            stats["total_puntos"] += puntaje
            stats["ultimo_puntaje"] = puntaje
            stats["partidas_jugadas"] += 1
            
            with open(ruta_json_usuarios, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
        except Exception as e:
            pass
    
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_puntos = pygame.font.Font(None, 64)
    fuente_boton = pygame.font.Font(None, 32)
    
    titulo_texto = "¡Juego Terminado!"
    puntos_texto = f"Puntuación final: {puntaje} puntos"

    boton_volver = crear_boton_texto("Volver al Menú", fuente_boton, (255, 255, 255),
                                     (0, 0, 255), (0, 0, 139), (128, 128, 128),
                                     (ANCHO_VENTANA // 2 - 150, ALTO_VENTANA // 2 + 100), (300, 80))

    tablero_activo = True
    while tablero_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver["Rectangulo"].collidepoint(evento.pos):
                    tablero_activo = False

        ventana.fill((30, 30, 30))
        
        superficie_titulo = fuente_titulo.render(titulo_texto, True, (255, 255, 255))
        rect_titulo = superficie_titulo.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 100))
        ventana.blit(superficie_titulo, rect_titulo)
        
        superficie_puntos = fuente_puntos.render(puntos_texto, True, (255, 255, 0))
        rect_puntos = superficie_puntos.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        ventana.blit(superficie_puntos, rect_puntos)

        dibujar_boton(ventana, boton_volver)

        pygame.display.update()
