import pygame
import os
from grafica.componentes import (
    crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton,
    crear_switch, dibujar_switch, actualizar_switch, verificar_click_switch
)
from logica.cargar_archivos import guardar_datos_json

"""Módulo para la visualización y gestión de la pantalla de configuración."""

def generar_botones_config(ancho_p, alto_p, conf_ui_config, colores, fuente, config_juego):
    """Crea los botones y switch para la pantalla de configuración usando los datos del JSON."""
    d_tdah = conf_ui_config["boton_tdah"]
    estado_tdah = config_juego.get("estado_tdah", False)
    
    colores_switch = {
        "on": colores["verde"],
        "off": colores["rojo"],
        "handle": colores["blanco"],
        "texto": colores["blanco"]
    }
    
    switch_tdah = crear_switch(
        x = int((ancho_p * d_tdah["x_relativo"]) - (120 // 2)), 
        y = int((alto_p * d_tdah["y_relativo"]) - (50 // 2)),
        ancho = 120,
        alto = 50,
        estado_inicial = estado_tdah,
        fuente = fuente,
        colores = colores_switch
    )
    
    btn_tdah = switch_tdah
    
    d_volver = conf_ui_config["boton_volver"]
    btn_volver = crear_boton(
        x = int((ancho_p * d_volver["x_relativo"]) - (d_volver["ancho"] // 2)),
        y = int((alto_p * d_volver["y_relativo"]) - (d_volver["alto"] // 2)),
        ancho = d_volver["ancho"],
        alto = d_volver["alto"],
        texto = d_volver["texto"],
        fuente = fuente,
        color_base = colores[d_volver["color_base"]],
        color_hover = colores[d_volver["color_hover"]],
        color_texto = colores[d_volver["color_texto"]],
        radio_borde = d_volver["radio_borde"]
    )
    
    return {
        "tdah": btn_tdah,
        "volver": btn_volver
    }

def mostrar_configuracion(pantalla, recursos, fuentes, colores, botones, pos_mouse, eventos, config_completa, layout_config):
    """Dibuja y gestiona la pantalla de configuración."""
    ancho_p = pantalla.get_width()
    
    pantalla.blit(recursos["fondos"]["menu"], (0, 0))
    
    sup_titulo = fuentes["titulo"].render("CONFIGURACIÓN", True, colores["blanco"])
    pantalla.blit(sup_titulo, sup_titulo.get_rect(center=(ancho_p // 2, 150)))
    
    desc_tdah = "Activa el cronómetro y mensajes de motivación para mayor enfoque."
    sup_desc = fuentes["info"].render(desc_tdah, True, colores["gris"])
    pantalla.blit(sup_desc, sup_desc.get_rect(center=(ancho_p // 2, 530)))
    
    for clave in botones:
        if clave == "tdah":
            actualizar_switch(botones[clave], pos_mouse)
            dibujar_switch(pantalla, botones[clave])
        else:
            actualizar_boton(botones[clave], pos_mouse)
            dibujar_boton(pantalla, botones[clave])
        
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
        
        if verificar_click_switch(botones["tdah"], evento):
            nuevo_estado = botones["tdah"]["activo"]
            config_completa["juego"]["estado_tdah"] = nuevo_estado
            
            ruta_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            ruta_config = os.path.join(ruta_base, "data", "config.json")
            guardar_datos_json(ruta_config, config_completa)
            
        if verificar_click_boton(botones["volver"], evento):
            return "menu"
                
    return None
