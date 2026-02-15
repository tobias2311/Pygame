import pygame

"""Módulo encargado de la gestión de volumen y procesamiento de eventos sonoros."""

def actualizar_volumen_global(estado_vol):
    """Establece el volumen del mezclador de Pygame según el estado mute y el nivel actual."""
    vol_final = 0.0
    if estado_vol["mute"] == True:
        vol_final = 0.0
    else:
        vol_final = estado_vol["nivel"]
    
    pygame.mixer.music.set_volume(vol_final)

def procesar_eventos_volumen(evento, botones_vol, estado_vol):
    """Procesa las interacciones del usuario con los botones de control de sonido."""
    from grafica.componentes import verificar_click_boton
    hubo_cambio = False

    if verificar_click_boton(botones_vol["vol_mas"], evento) == True:
        if estado_vol["nivel"] < 1.0:
            estado_vol["nivel"] = estado_vol["nivel"] + 0.1
            if estado_vol["nivel"] > 1.0:
                estado_vol["nivel"] = 1.0
        estado_vol["mute"] = False
        hubo_cambio = True

    if verificar_click_boton(botones_vol["vol_menos"], evento) == True:
        if estado_vol["nivel"] > 0.0:
            estado_vol["nivel"] = estado_vol["nivel"] - 0.1
            if estado_vol["nivel"] < 0.0:
                estado_vol["nivel"] = 0.0
        estado_vol["mute"] = False
        hubo_cambio = True

    if verificar_click_boton(botones_vol["mute"], evento) == True:
        if estado_vol["mute"] == True:
            estado_vol["mute"] = False
        else:
            estado_vol["mute"] = True
        hubo_cambio = True

    if hubo_cambio == True:
        actualizar_volumen_global(estado_vol)

    return hubo_cambio
