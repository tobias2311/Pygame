import pygame
from grafica.componentes import crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton

"""Módulo para la visualización y gestión de la pantalla de selección de temática y dificultad."""

def generar_botones_seleccion(ancho_p, alto_p, conf_seleccion, fuentes, colores):
    layout = conf_seleccion["layout"]
    ancho_btn = layout["ancho_btn"]
    alto_btn = layout["alto_btn"]
    
    temas = conf_seleccion["tematicas"]
    botones_temas = []
    x_temas = int(ancho_p * layout["x_temas_rel"])
    y_inicio = int(alto_p * layout["y_inicio_rel"])
    
    for i in range(len(temas)):
        tema = temas[i]
        y = y_inicio + (i * (alto_btn + 20))
        btn = crear_boton(
            x = x_temas,
            y = y,
            ancho = ancho_btn,
            alto = alto_btn,
            texto = tema,
            fuente = fuentes["cuerpo"],
            color_base = colores["azul_oscuro"],
            color_hover = colores["celeste"],
            color_texto = colores["blanco"],
            radio_borde = 10
        )
        botones_temas.append({"btn": btn, "valor": tema})

    dificultades = conf_seleccion["dificultades"]
    botones_dif = []
    x_dif = int(ancho_p * layout["x_dif_rel"])
    
    for i in range(len(dificultades)):
        dif = dificultades[i]
        y = y_inicio + (i * (alto_btn + 20))
        btn = crear_boton(
            x = x_dif,
            y = y,
            ancho = ancho_btn,
            alto = alto_btn,
            texto = dif["texto"],
            fuente = fuentes["cuerpo"],
            color_base = colores["azul_oscuro"],
            color_hover = colores["celeste"],
            color_texto = colores["blanco"],
            radio_borde = 10
        )
        botones_dif.append({"btn": btn, "valor": dif["valor"]})

    d_btn_comenzar = layout["boton_comenzar"]
    btn_comenzar = crear_boton(
        x = int((ancho_p * d_btn_comenzar["x_rel"]) - (d_btn_comenzar["ancho"] // 2)),
        y = int((alto_p * d_btn_comenzar["y_rel"]) - (d_btn_comenzar["alto"] // 2)),
        ancho = d_btn_comenzar["ancho"],
        alto = d_btn_comenzar["alto"],
        texto = "COMENZAR",
        fuente = fuentes["subtitulo"],
        color_base = colores["verde"],
        color_hover = colores["celeste"],
        color_texto = colores["blanco"],
        radio_borde = 15
    )
    
    return {
        "temas": botones_temas,
        "dificultades": botones_dif,
        "comenzar": btn_comenzar,
        "config": conf_seleccion 
    }

def mostrar_seleccion(pantalla, recursos, fuentes, colores, botones, pos_mouse, eventos, seleccion_actual):
    layout = botones["config"]["layout"]
    
    fondo = recursos["fondos"]["menu"]
    pantalla.blit(fondo, (0, 0))

    x_temas = int(pantalla.get_width() * layout["x_temas_rel"])
    x_dif = int(pantalla.get_width() * layout["x_dif_rel"])
    y_titulos = int(pantalla.get_height() * (layout["y_inicio_rel"] - 0.1))

    sup_tema = fuentes["subtitulo"].render("TEMÁTICA", True, colores["amarillo"])
    pantalla.blit(sup_tema, (x_temas, y_titulos))

    sup_dif = fuentes["subtitulo"].render("DIFICULTAD", True, colores["amarillo"])
    pantalla.blit(sup_dif, (x_dif, y_titulos))

    for item in botones["temas"]:
        btn = item["btn"]
        actualizar_boton(btn, pos_mouse)
        
        if seleccion_actual["tematica"] == item["valor"]:
            btn["color_actual"] = colores["celeste"]
        dibujar_boton(pantalla, btn)

    for item in botones["dificultades"]:
        btn = item["btn"]
        actualizar_boton(btn, pos_mouse)
        
        if seleccion_actual["dificultad"] == item["valor"]:
            btn["color_actual"] = colores["celeste"]
        dibujar_boton(pantalla, btn)

    hay_seleccion = seleccion_actual["tematica"] != "" and seleccion_actual["dificultad"] != ""
    if hay_seleccion:
        actualizar_boton(botones["comenzar"], pos_mouse)
        dibujar_boton(pantalla, botones["comenzar"])

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
        
        for item in botones["temas"]:
            if verificar_click_boton(item["btn"], evento):
                seleccion_actual["tematica"] = item["valor"]
        
        for item in botones["dificultades"]:
            if verificar_click_boton(item["btn"], evento):
                seleccion_actual["dificultad"] = item["valor"]
       
        if hay_seleccion and verificar_click_boton(botones["comenzar"], evento):
            return "iniciar_juego"

    return None
