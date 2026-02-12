import pygame
from grafica.componentes import crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton

def generar_botones_menu(ancho_p, alto_p, conf_menu, colores, fuente):
    """
    Crea los botones del menú basándose en la configuración.
    """
    # BOTÓN INICIO
    datos_inicio = conf_menu["boton_inicio"]
    btn_inicio = crear_boton(
        x = int((ancho_p * datos_inicio["x_relativo"]) - (datos_inicio["ancho"] // 2)),
        y = int((alto_p * datos_inicio["y_relativo"]) - (datos_inicio["alto"] // 2)),
        ancho = datos_inicio["ancho"],
        alto = datos_inicio["alto"],
        texto = datos_inicio["texto"],
        fuente = fuente,
        color_base = colores[datos_inicio["color_base"]],
        color_hover = colores[datos_inicio["color_hover"]],
        color_texto = colores[datos_inicio["color_texto"]],
        radio_borde = datos_inicio["radio_borde"]
    )

    # BOTÓN CONFIGURACIÓN
    datos_config = conf_menu["boton_config"]
    btn_config = crear_boton(
        x = int((ancho_p * datos_config["x_relativo"]) - (datos_config["ancho"] // 2)),
        y = int((alto_p * datos_config["y_relativo"]) - (datos_config["alto"] // 2)),
        ancho = datos_config["ancho"],
        alto = datos_config["alto"],
        texto = datos_config["texto"],
        fuente = fuente,
        color_base = colores[datos_config["color_base"]],
        color_hover = colores[datos_config["color_hover"]],
        color_texto = colores[datos_config["color_texto"]],
        radio_borde = datos_config["radio_borde"]
    )

    # BOTÓN SALIR
    datos_salir = conf_menu["boton_salir"]
    btn_salir = crear_boton(
        x = int((ancho_p * datos_salir["x_relativo"]) - (datos_salir["ancho"] // 2)),
        y = int((alto_p * datos_salir["y_relativo"]) - (datos_salir["alto"] // 2)),
        ancho = datos_salir["ancho"],
        alto = datos_salir["alto"],
        texto = datos_salir["texto"],
        fuente = fuente,
        color_base = colores[datos_salir["color_base"]],
        color_hover = colores[datos_salir["color_hover"]],
        color_texto = colores[datos_salir["color_texto"]],
        radio_borde = datos_salir["radio_borde"]
    )

    # BOTONES VOLUMEN
    d_vol = conf_menu["controles_volumen"]
    
    btn_vol_mas = crear_boton(
        int((ancho_p * d_vol["boton_mas"]["x_relativo"]) - (d_vol["boton_mas"]["ancho"] // 2)),
        int((alto_p * d_vol["boton_mas"]["y_relativo"]) - (d_vol["boton_mas"]["alto"] // 2)),
        d_vol["boton_mas"]["ancho"], d_vol["boton_mas"]["alto"], d_vol["boton_mas"]["texto"],
        fuente, colores[d_vol["boton_mas"]["color_base"]], colores[d_vol["boton_mas"]["color_hover"]]
    )

    btn_vol_menos = crear_boton(
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

    return {
        "inicio": btn_inicio,
        "config": btn_config,
        "salir": btn_salir,
        "vol_mas": btn_vol_mas,
        "vol_menos": btn_vol_menos,
        "mute": btn_mute
    }

def mostrar_menu(pantalla, recursos, fuentes, colores, botones, pos_mouse, eventos, estado_vol):
    """
    Dibuja y gestiona la pantalla del menú principal.
    Retorna el nombre de la siguiente pantalla o None si no hay cambio.
    """
    # 1. Dibujar Fondo
    fondo_menu = recursos["fondos"]["menu"]
    pantalla.blit(fondo_menu, (0, 0))
    
    # 2. Lógica de botones principales
    actualizar_boton(botones["inicio"], pos_mouse)
    actualizar_boton(botones["config"], pos_mouse)
    actualizar_boton(botones["salir"], pos_mouse)
    actualizar_boton(botones["vol_mas"], pos_mouse)
    actualizar_boton(botones["vol_menos"], pos_mouse)
    actualizar_boton(botones["mute"], pos_mouse)

    dibujar_boton(pantalla, botones["inicio"])
    dibujar_boton(pantalla, botones["config"])
    dibujar_boton(pantalla, botones["salir"])
    dibujar_boton(pantalla, botones["vol_mas"])
    dibujar_boton(pantalla, botones["vol_menos"])
    dibujar_boton(pantalla, botones["mute"])

    # 3. Mostrar Nivel de Volumen
    texto_vol = f"Vol: {int(estado_vol['nivel'] * 100)}%"
    if estado_vol["mute"]: texto_vol = "MUTE"
    sup_vol = fuentes["info"].render(texto_vol, True, colores["blanco"])
    pantalla.blit(sup_vol, (pantalla.get_width() - 150, pantalla.get_height() - 100))

    # 4. Manejar Eventos
    for evento in eventos:
        if verificar_click_boton(botones["inicio"], evento):
            return "juego"
        if verificar_click_boton(botones["config"], evento):
            return "configuracion"
        if verificar_click_boton(botones["salir"], evento):
            return "salir"
            
        # Controles de Volumen
        if verificar_click_boton(botones["vol_mas"], evento):
            estado_vol["nivel"] = min(1.0, estado_vol["nivel"] + 0.1)
            estado_vol["mute"] = False
            pygame.mixer.music.set_volume(estado_vol["nivel"])
        if verificar_click_boton(botones["vol_menos"], evento):
            estado_vol["nivel"] = max(0.0, estado_vol["nivel"] - 0.1)
            estado_vol["mute"] = False
            pygame.mixer.music.set_volume(estado_vol["nivel"])
        if verificar_click_boton(botones["mute"], evento):
            estado_vol["mute"] = not estado_vol["mute"]
            pygame.mixer.music.set_volume(0.0 if estado_vol["mute"] else estado_vol["nivel"])
            
    return None
