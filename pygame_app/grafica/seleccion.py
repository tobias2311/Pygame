import pygame
from grafica.componentes import crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton

def generar_botones_seleccion(ancho_p, alto_p, fuentes, colores):
    """
    Crea los botones para elegir temática y dificultad.
    """
    x_centro = ancho_p // 2
    ancho_btn = 350
    alto_btn = 60

    # Botones de Temática
    tematicas = ["Cultura general", "Frases deportivas", "Frases populares"]
    botones_temas = []
    for i, tema in enumerate(tematicas):
        btn = crear_boton(
            x = x_centro - 400,
            y = 350 + (i * 80),
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

    # Botones de Dificultad
    dificultades = [
        {"texto": "Fácil", "valor": "facil"},
        {"texto": "Pro", "valor": "pro"},
        {"texto": "Experto", "valor": "experto"}
    ]
    botones_dif = []
    for i, dif in enumerate(dificultades):
        btn = crear_boton(
            x = x_centro + 50,
            y = 350 + (i * 80),
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

    # Botón Comenzar
    btn_comenzar = crear_boton(
        x = x_centro - 150,
        y = 650,
        ancho = 300,
        alto = 80,
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
        "comenzar": btn_comenzar
    }

def mostrar_seleccion(pantalla, recursos, fuentes, colores, botones, pos_mouse, eventos, seleccion_actual):
    """
    Dibuja y gestiona la pantalla de selección.
    """
    # 1. Fondo
    fondo = recursos["fondos"]["menu"]
    pantalla.blit(fondo, (0, 0))

    # 2. Títulos auxiliares
    sup_tema = fuentes["subtitulo"].render("TEMÁTICA", True, colores["amarillo"])
    pantalla.blit(sup_tema, (pantalla.get_width() // 2 - 400, 280))

    sup_dif = fuentes["subtitulo"].render("DIFICULTAD", True, colores["amarillo"])
    pantalla.blit(sup_dif, (pantalla.get_width() // 2 + 50, 280))

    # 3. Dibujar Botones de Temas
    for item in botones["temas"]:
        btn = item["btn"]
        # Resaltar si está seleccionado
        if seleccion_actual["tematica"] == item["valor"]:
            btn["color_actual"] = colores["celeste"]
        else:
            actualizar_boton(btn, pos_mouse)
        dibujar_boton(pantalla, btn)

    # 4. Dibujar Botones de Dificultad
    for item in botones["dificultades"]:
        btn = item["btn"]
        # Resaltar si está seleccionado
        if seleccion_actual["dificultad"] == item["valor"]:
            btn["color_actual"] = colores["celeste"]
        else:
            actualizar_boton(btn, pos_mouse)
        dibujar_boton(pantalla, btn)

    # 5. Dibujar Botón Comenzar (solo si ambos están elegidos)
    hay_seleccion = seleccion_actual["tematica"] != "" and seleccion_actual["dificultad"] != ""
    if hay_seleccion:
        actualizar_boton(botones["comenzar"], pos_mouse)
        dibujar_boton(pantalla, botones["comenzar"])

    # 6. Manejo de Eventos
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
        
        # Click en Temas
        for item in botones["temas"]:
            if verificar_click_boton(item["btn"], evento):
                seleccion_actual["tematica"] = item["valor"]
        
        # Click en Dificultades
        for item in botones["dificultades"]:
            if verificar_click_boton(item["btn"], evento):
                seleccion_actual["dificultad"] = item["valor"]

        # Click en Comenzar
        if hay_seleccion and verificar_click_boton(botones["comenzar"], evento):
            return "iniciar_juego"

    return None
