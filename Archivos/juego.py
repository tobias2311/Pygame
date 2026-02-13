"""
Módulo para la lógica central del juego (preguntas, respuestas, puntajes)
"""
import pygame
import sys
import random
import json
import os
from botones import crear_boton_texto, dibujar_boton
from cargar_datos import cargar_preguntas_desde_csv
from musica import subir_volumen, bajar_volumen, set_volumen
from constantes import ANCHO_VENTANA, ALTO_VENTANA, COLORES, NUM_PREGUNTAS, PUNTOS_POR_DIFICULTAD


def iniciar_juego(ventana, dificultad, tematica, volumen_actual, ANCHO_VENTANA, ALTO_VENTANA, 
                  fondo_juego_escalado, nombre_jugador="", ruta_json_usuarios="", modo_tdah=False):
   
    fuente_info = pygame.font.Font(None, 24)
    fuente_pregunta = pygame.font.Font(None, 50)
    fuente_opciones = pygame.font.Font(None, 36)
    fuente_feedback = pygame.font.Font(None, 48)

    boton_subir_volumen = crear_boton_texto(
        texto="+", fuente=fuente_info, color_texto=COLORES["BLANCO"], color_fondo=COLORES["VERDE_CLARO"],
        color_borde=COLORES["VERDE_OSCURO"], color_fondo_hover=(50, 255, 50), 
        posicion=(ANCHO_VENTANA - 70, 20), dimension=(50, 50)
    )
    boton_bajar_volumen = crear_boton_texto(
        texto="-", fuente=fuente_info, color_texto=COLORES["BLANCO"], color_fondo=COLORES["ROJO_CLARO"],
        color_borde=COLORES["ROJO_OSCURO"], color_fondo_hover=(255, 50, 50), 
        posicion=(ANCHO_VENTANA - 130, 20), dimension=(50, 50)
    )
    boton_salir_juego = crear_boton_texto(
        texto="Salir", fuente=fuente_info, color_texto=COLORES["BLANCO"], color_fondo=COLORES["GRIS"],
        color_borde=COLORES["GRIS_OSCURO"], color_fondo_hover=COLORES["GRIS_CLARO"], 
        posicion=(ANCHO_VENTANA - 150, ALTO_VENTANA - 70), dimension=(130, 50)
    )

    preguntas_raw = cargar_preguntas_desde_csv()
    preguntas = [p for p in preguntas_raw if p["categoria"].lower() == tematica.lower()]

    if not preguntas:
        return "menu", volumen_actual

    puntaje_total = 0
    preguntas_a_usar = random.sample(preguntas, min(NUM_PREGUNTAS, len(preguntas)))
    
    # Temporizador Global para Modo TDAH (60 segundos para toda la partida)
    tiempo_inicio_partida = pygame.time.get_ticks()
    tiempo_limite_total = 60 * 1000 # 60 segundos en ms
    
    aciertos_consecutivos = 0
    mensajes_motivadores = ["¡Vas muy bien!", "¡Excelente racha!", "¡Seguí así!", "¡Sos un genio!", "¡Increíble!"]

    for pregunta in preguntas_a_usar:
        estado_pregunta, nuevo_volumen = mostrar_pregunta(
            ventana, pregunta, dificultad, tematica, volumen_actual, ANCHO_VENTANA, ALTO_VENTANA,
            fondo_juego_escalado, boton_bajar_volumen, boton_subir_volumen, boton_salir_juego, 
            modo_tdah=modo_tdah, tiempo_inicio_partida=tiempo_inicio_partida, tiempo_limite_total=tiempo_limite_total
        )
        volumen_actual = nuevo_volumen
        
        if estado_pregunta == "menu":
            return "menu", volumen_actual
        elif estado_pregunta == "tiempo_agotado":
            # Si se acaba el tiempo global, terminamos la partida
            break
        elif estado_pregunta == "correcto":
            puntaje_total += PUNTOS_POR_DIFICULTAD[dificultad]
            aciertos_consecutivos += 1
            if modo_tdah and aciertos_consecutivos % 3 == 0:
                mostrar_mensaje_animo(ventana, random.choice(mensajes_motivadores), ANCHO_VENTANA, ALTO_VENTANA)
        else:
            aciertos_consecutivos = 0
    
    mostrar_tablero_puntuacion(ventana, puntaje_total, ANCHO_VENTANA, ALTO_VENTANA, nombre_jugador, ruta_json_usuarios)
    
    return "menu", volumen_actual


def mostrar_pregunta(ventana, pregunta, dificultad, tematica, volumen_actual, ANCHO_VENTANA, ALTO_VENTANA,
                     fondo_juego_escalado, boton_bajar_volumen, boton_subir_volumen, boton_salir_juego, 
                      modo_tdah=False, tiempo_inicio_partida=0, tiempo_limite_total=60000):
   
    pygame.key.set_repeat(200, 50)
    
    fuente_pregunta = pygame.font.Font(None, 50)
    fuente_opciones = pygame.font.Font(None, 36)
    fuente_info = pygame.font.Font(None, 24)
    fuente_feedback = pygame.font.Font(None, 48)
    fuente_timer = pygame.font.Font(None, 60) # Fuente más grande para el temporizador
    
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
        
        for i in range(len(pregunta["opciones"])):
            opcion = pregunta["opciones"][i]
            x_pos, y_pos = posiciones[i]
            boton = crear_boton_texto(opcion, fuente_opciones, COLORES["BLANCO"],
                                      COLORES["AZUL"], COLORES["AZUL_OSCURO"], COLORES["GRIS_CLARO"],
                                      (x_pos, y_pos), (ancho_boton, alto_boton))
            botones_opciones.append(boton)
    
    # Eliminado temporizador por pregunta para usar el global
    
    while pregunta_activa:
        # Si hay feedback y pasó el tiempo, retornar resultado
        if feedback_activo and (pygame.time.get_ticks() - feedback_inicio_tiempo > 1500):
            return resultado_pregunta, volumen_actual

        # Lógica del temporizador global
        if modo_tdah and not feedback_activo:
            tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_partida
            tiempo_restante_ms = max(0, tiempo_limite_total - tiempo_transcurrido)
            if tiempo_restante_ms <= 0:
                feedback_activo = True
                resultado_pregunta = "tiempo_agotado"
                feedback_texto = "¡Tiempo finalizado!"
                feedback_color = COLORES["ROJO_FEEDBACK"]
                feedback_inicio_tiempo = pygame.time.get_ticks()

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
                                    feedback_color = COLORES["VERDE_FEEDBACK"] if es_correcto else COLORES["ROJO_FEEDBACK"]
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
        superficie_info = fuente_info.render(info_texto, True, COLORES["BLANCO"])
        ventana.blit(superficie_info, (10, 10))
        
        # Botones de control (volumen y salir)
        dibujar_boton(ventana, boton_bajar_volumen)
        dibujar_boton(ventana, boton_subir_volumen)
        dibujar_boton(ventana, boton_salir_juego)

        # Texto de la pregunta
        color_pregunta = COLORES["AMARILLO_TEXTO"]
        superficie_pregunta = fuente_pregunta.render(pregunta["enunciado"], True, color_pregunta)
        rect_pregunta = superficie_pregunta.get_rect(center=(ANCHO_VENTANA // 2, 150))
        ventana.blit(superficie_pregunta, rect_pregunta)

        # Opciones de respuesta
        if dificultad == "Experto":
            pygame.draw.rect(ventana, COLORES["BLANCO"] if input_activo else (200, 200, 200), rect_input, 2)
            superficie_texto = fuente_opciones.render(respuesta_usuario, True, COLORES["BLANCO"])
            ventana.blit(superficie_texto, (rect_input.x + 5, rect_input.y + 5))
        else:
            # Dibujar botones de opciones para Fácil y Pro
            for boton in botones_opciones:
                dibujar_boton(ventana, boton)

        # Dibujar temporizador global si Modo TDAH está activo
        if modo_tdah:
            tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_partida
            tiempo_restante_seg = max(0, (tiempo_limite_total - tiempo_transcurrido) // 1000)
            color_timer = COLORES["BLANCO"] if tiempo_restante_seg > 10 else COLORES["ROJO_FEEDBACK"]
            sup_timer = fuente_timer.render(f"Tiempo Partida: {tiempo_restante_seg}s", True, color_timer)
            ventana.blit(sup_timer, (ANCHO_VENTANA // 2 - sup_timer.get_width() // 2, 60))

        # Feedback (si está activo)
        if feedback_activo:
            superficie_feedback = fuente_feedback.render(feedback_texto, True, feedback_color)
            rect_feedback = superficie_feedback.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
            ventana.blit(superficie_feedback, rect_feedback)
        
        pygame.display.update()
    
    return "menu", volumen_actual


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

    boton_volver = crear_boton_texto("Volver al Menú", fuente_boton, COLORES["BLANCO"],
                                     COLORES["AZUL"], COLORES["AZUL_OSCURO"], COLORES["GRIS_CLARO"],
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

        ventana.fill(COLORES["FONDO_OSCURO"])
        
        superficie_titulo = fuente_titulo.render(titulo_texto, True, COLORES["BLANCO"])
        rect_titulo = superficie_titulo.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 100))
        ventana.blit(superficie_titulo, rect_titulo)
        
        superficie_puntos = fuente_puntos.render(puntos_texto, True, COLORES["AMARILLO_TEXTO"])
        rect_puntos = superficie_puntos.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        ventana.blit(superficie_puntos, rect_puntos)

        dibujar_boton(ventana, boton_volver)

        pygame.display.update()

def mostrar_mensaje_animo(ventana, mensaje, ANCHO, ALTO):
    """Muestra un mensaje motivacional temporal"""
    fuente = pygame.font.Font(None, 60)
    superficie = fuente.render(mensaje, True, (0, 255, 255))
    rect = superficie.get_rect(center=(ANCHO // 2, ALTO // 2 + 200))
    
    # Animación simple (subir un poco)
    for i in range(30):
        # Redibujar fondo en esa zona (o simplificar con un delay)
        ventana.blit(superficie, rect)
        pygame.display.update(rect)
        pygame.time.delay(30)
