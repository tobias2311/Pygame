import pygame
from grafica.componentes import (
    crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton, 
    crear_input_box, manejar_evento_input, dibujar_input_box
)
from logica.sonido import procesar_eventos_volumen
from logica.juego_logica import verificar_respuesta

# Módulo para la visualización y gestión de eventos de la pantalla del juego.

def generar_botones_opciones(ancho_p, alto_p, opciones, fuentes, colores, config_layout):
    """Genera dinámicamente los botones de opciones de respuesta según el layout."""
    botones = []
    l_opt = config_layout["opciones"]
    ancho_btn = l_opt["ancho"]
    alto_btn = l_opt["alto"]
    x_centro = ancho_p // 2
    y_inicio = int(alto_p * l_opt["y_inicio_rel"])
    
    for i in range(len(opciones)):
        col = i % 2     
        fila = i // 2   
        
        mitad_ancho_total = ancho_btn + (l_opt["separacion_x"] // 2)
        if col == 0:
            x = x_centro - mitad_ancho_total
        else:
            x = x_centro + (l_opt["separacion_x"] // 2)

        y = y_inicio + (fila * (alto_btn + l_opt["separacion_y"]))
        
        btn = crear_boton(
            x = x,
            y = y,
            ancho = ancho_btn,
            alto = alto_btn,
            texto = opciones[i],
            fuente = fuentes["cuerpo"],
            color_base = colores["azul_oscuro"],
            color_hover = colores["celeste"],
            color_texto = colores["blanco"],
            radio_borde = 10
        )
        botones.append(btn)
    
    return botones

def generar_botones_vol_juego(ancho_p, alto_p, d_vol, colores, fuente):
    """Crea los botones de control de volumen para la pantalla de juego."""
    btn_mas = crear_boton(
        int((ancho_p * d_vol["boton_mas"]["x_relativo"]) - (d_vol["boton_mas"]["ancho"] // 2)),
        int((alto_p * d_vol["boton_mas"]["y_relativo"]) - (d_vol["boton_mas"]["alto"] // 2)),
        d_vol["boton_mas"]["ancho"], d_vol["boton_mas"]["alto"], d_vol["boton_mas"]["texto"],
        fuente, colores[d_vol["boton_mas"]["color_base"]], colores[d_vol["boton_mas"]["color_hover"]]
    )
    btn_menos = crear_boton(
        int((ancho_p * d_vol["boton_menos"]["x_relativo"]) - (d_vol["boton_menos"]["ancho"] // 2)),
        int((alto_p * d_vol["boton_menos"]["y_relativo"]) - (d_vol["boton_menos"]["alto"] // 2)),
        d_vol["boton_menos"]["ancho"], d_vol["boton_menos"]["alto"], d_vol["boton_menos"]["texto"],
        fuente, colores[d_vol["boton_menos"]["color_base"]], colores[d_vol["boton_menos"]["color_hover"]]
    )
    btn_mute = crear_boton(
        int((ancho_p * d_vol["boton_mute"]["x_relativo"]) - (d_vol["boton_mute"]["ancho"] // 2)),
        int((alto_p * d_vol["boton_mute"]["y_relativo"]) - (d_vol["boton_mute"]["alto"] // 2)),
        d_vol["boton_mute"]["ancho"], d_vol["boton_mute"]["alto"], d_vol["boton_mute"]["texto"],
        fuente, colores[d_vol["boton_mute"]["color_base"]], colores[d_vol["boton_mute"]["color_hover"]]
    )
    return {"vol_mas": btn_mas, "vol_menos": btn_menos, "mute": btn_mute}

def mostrar_pantalla_juego(pantalla, recursos, fuentes, colores, estado_juego, pos_mouse, eventos, botones_vol, estado_vol, config_layout):
    """Dibuja todos los elementos de la interfaz de juego y gestiona clics e inputs."""
    ancho_p = pantalla.get_width()
    alto_p = pantalla.get_height()
    
    fondo_juego = recursos["fondos"]["juego"]
    pantalla.blit(fondo_juego, (0, 0))

    for clave in botones_vol:
        actualizar_boton(botones_vol[clave], pos_mouse)
        dibujar_boton(pantalla, botones_vol[clave])

    if estado_juego["pantalla_final"] == True:
        sup_titulo = fuentes["titulo"].render("¡FIN DE LA PARTIDA!", True, colores["amarillo"])
        rect_titulo = sup_titulo.get_rect(center=(ancho_p // 2, 150))
        pantalla.blit(sup_titulo, rect_titulo)

        txt_puntos = f"Puntaje Total: {estado_juego['puntaje']}"
        txt_resumen = f"Respondiste bien {estado_juego['correctas']} de {len(estado_juego['preguntas'])} preguntas"
        
        sup_puntos = fuentes["subtitulo"].render(txt_puntos, True, colores["blanco"])
        sup_resumen = fuentes["cuerpo"].render(txt_resumen, True, colores["celeste"])
        
        pantalla.blit(sup_puntos, sup_puntos.get_rect(center=(ancho_p // 2, 300)))
        pantalla.blit(sup_resumen, sup_resumen.get_rect(center=(ancho_p // 2, 400)))

        btn_volver = crear_boton(ancho_p//2 - 150, 550, 300, 80, "VOLVER AL MENÚ", fuentes["cuerpo"], colores["azul_oscuro"], colores["celeste"])
        actualizar_boton(btn_volver, pos_mouse)
        dibujar_boton(pantalla, btn_volver)

        for evento in eventos:
            if verificar_click_boton(btn_volver, evento) == True:
                return "podio"
            procesar_eventos_volumen(evento, botones_vol, estado_vol)
        return None

    if estado_juego["indice_actual"] >= len(estado_juego["preguntas"]):
        estado_juego["pantalla_final"] = True
        return None

    pregunta_actual = estado_juego["preguntas"][estado_juego["indice_actual"]]
    
    sup_enunciado = fuentes["subtitulo"].render(pregunta_actual["enunciado"], True, colores["blanco"])
    y_enunciado = int(alto_p * config_layout["enunciado_y_rel"])
    rect_enunciado = sup_enunciado.get_rect(center=(ancho_p // 2, y_enunciado))
    pantalla.blit(sup_enunciado, rect_enunciado)

    if estado_juego["dificultad"] == "experto":
        if estado_juego["input_box"] == None:
            l_input = config_layout["input_experto"]
            y_input = int(alto_p * l_input["y_rel"])
            estado_juego["input_box"] = crear_input_box(
                ancho_p // 2 - (l_input["ancho"] // 2), y_input, l_input["ancho"], l_input["alto"], 
                fuentes["cuerpo"], colores["celeste"], colores["blanco"]
            )
            estado_juego["input_box"]["activo"] = True 
            estado_juego["input_box"]["color_actual"] = colores["celeste"]
        
        dibujar_input_box(pantalla, estado_juego["input_box"])
        
        l_input = config_layout["input_experto"]
        y_instr = int(alto_p * l_input["y_instruccion_rel"])
        sup_instruccion = fuentes["info"].render("Escribe tu respuesta y presiona ENTER", True, colores["celeste"])
        pantalla.blit(sup_instruccion, sup_instruccion.get_rect(center=(ancho_p // 2, y_instr)))
    else:
        if len(estado_juego["botones_opciones"]) == 0:
            estado_juego["botones_opciones"] = generar_botones_opciones(ancho_p, alto_p, pregunta_actual["opciones"], fuentes, colores, config_layout)

        for btn in estado_juego["botones_opciones"]:
            actualizar_boton(btn, pos_mouse)
            dibujar_boton(pantalla, btn)

    texto_puntos = f"Puntaje: {estado_juego['puntaje']}"
    sup_puntos = fuentes["info"].render(texto_puntos, True, colores["amarillo"])
    pos_pts = config_layout["puntaje_pos"]
    pantalla.blit(sup_puntos, (pos_pts[0], pos_pts[1]))

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
        
        procesar_eventos_volumen(evento, botones_vol, estado_vol)

        if estado_juego["dificultad"] == "experto":
            texto_ingresado = manejar_evento_input(estado_juego["input_box"], evento)
            if texto_ingresado != None: 
                verificar_respuesta(estado_juego, texto_ingresado, pregunta_actual["respuesta_correcta"])
                return None
        else:
            for i in range(len(estado_juego["botones_opciones"])):
                btn = estado_juego["botones_opciones"][i]
                if verificar_click_boton(btn, evento) == True:
                    verificar_respuesta(estado_juego, pregunta_actual["opciones"][i], pregunta_actual["respuesta_correcta"])
                    return None
    return None
