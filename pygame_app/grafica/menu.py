from grafica.componentes import crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton
from logica.sonido import procesar_eventos_volumen

"""Módulo encargado de gestionar el menú principal y la navegación inicial."""

def generar_botones_menu(ancho_p, alto_p, conf_menu, colores, fuente):
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
    
    datos_ranking = conf_menu["boton_ranking"]
    btn_ranking = crear_boton(
        x = int((ancho_p * datos_ranking["x_relativo"]) - (datos_ranking["ancho"] // 2)),
        y = int((alto_p * datos_ranking["y_relativo"]) - (datos_ranking["alto"] // 2)),
        ancho = datos_ranking["ancho"],
        alto = datos_ranking["alto"],
        texto = datos_ranking["texto"],
        fuente = fuente,
        color_base = colores[datos_ranking["color_base"]],
        color_hover = colores[datos_ranking["color_hover"]],
        color_texto = colores[datos_ranking["color_texto"]],
        radio_borde = datos_ranking["radio_borde"]
    )

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
        "ranking": btn_ranking,
        "config": btn_config,
        "salir": btn_salir,
        "vol_mas": btn_vol_mas,
        "vol_menos": btn_vol_menos,
        "mute": btn_mute
    }

def mostrar_menu(pantalla, recursos, fuentes, colores, botones, pos_mouse, eventos, estado_vol):
    fondo_menu = recursos["fondos"]["menu"]
    pantalla.blit(fondo_menu, (0, 0))
    
    for clave in botones:
        actualizar_boton(botones[clave], pos_mouse)
        dibujar_boton(pantalla, botones[clave])

    texto_vol = f"Vol: {int(estado_vol['nivel'] * 100)}%"
    if estado_vol["mute"]: texto_vol = "MUTE"
    sup_vol = fuentes["info"].render(texto_vol, True, colores["blanco"])
    pantalla.blit(sup_vol, (pantalla.get_width() - 150, pantalla.get_height() - 100))

    for evento in eventos:
        if verificar_click_boton(botones["inicio"], evento):
            return "juego"
        if verificar_click_boton(botones["ranking"], evento):
            return "ranking"
        if verificar_click_boton(botones["config"], evento):
            return "configuracion"
        if verificar_click_boton(botones["salir"], evento):
            return "salir"
            
        procesar_eventos_volumen(evento, botones, estado_vol)
            
    return None
