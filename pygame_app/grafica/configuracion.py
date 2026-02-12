import pygame
from grafica.componentes import crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton

def generar_botones_config(ancho_p, alto_p, conf_ui_config, colores, fuente):
    """
    Crea los botones para la pantalla de configuración usando los datos del JSON.
    """
    
    # Solo queda el botón Volver (los de volumen se movieron al menú/juego)
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
        "volver": btn_volver
    }

def mostrar_configuracion(pantalla, recursos, fuentes, colores, botones, pos_mouse, eventos):
    """
    Dibuja y gestiona la pantalla de configuración.
    """
    ancho_p = pantalla.get_width()
    
    # 1. Fondo
    pantalla.blit(recursos["fondos"]["menu"], (0, 0))
    
    # 2. Título
    sup_titulo = fuentes["titulo"].render("CONFIGURACIÓN", True, colores["blanco"])
    pantalla.blit(sup_titulo, sup_titulo.get_rect(center=(ancho_p // 2, 150)))
    
    # 3. Mensaje Provisorio (Aquí irá el modo TDAH)
    sup_msg = fuentes["subtitulo"].render("PRÓXIMAMENTE: MODO TDAH", True, colores["celeste"])
    pantalla.blit(sup_msg, sup_msg.get_rect(center=(ancho_p // 2, 400)))
    
    # 4. Actualizar y Dibujar Botones
    for clave in botones:
        actualizar_boton(botones[clave], pos_mouse)
        dibujar_boton(pantalla, botones[clave])
        
    # 5. Manejo de Eventos
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
        
        # Click en Volver
        if verificar_click_boton(botones["volver"], evento):
            return "menu"
                
    return None
