import pygame
from grafica.componentes import crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton
from logica.usuarios import obtener_ranking

def generar_botones_ranking(ancho_p, alto_p, conf_ranking, colores, fuente):
    """
    Crea los botones para la pantalla de ranking.
    """
    datos_volver = conf_ranking["boton_volver"]
    btn_volver = crear_boton(
        x = int((ancho_p * datos_volver["x_relativo"]) - (datos_volver["ancho"] // 2)),
        y = int((alto_p * datos_volver["y_relativo"]) - (datos_volver["alto"] // 2)),
        ancho = datos_volver["ancho"],
        alto = datos_volver["alto"],
        texto = datos_volver["texto"],
        fuente = fuente,
        color_base = colores[datos_volver["color_base"]],
        color_hover = colores[datos_volver["color_hover"]],
        color_texto = colores[datos_volver["color_texto"]],
        radio_borde = datos_volver["radio_borde"]
    )
    return {"volver": btn_volver}

def mostrar_ranking(pantalla, recursos, fuentes, colores, botones, pos_mouse, eventos, conf_ranking):
    """
    Dibuja la pantalla de ranking con los mejores puntajes.
    """
    # 1. Dibujar Fondo
    fondo = recursos["fondos"]["menu"]
    pantalla.blit(fondo, (0, 0))
    
    # overlay oscuro para legibilidad
    overlay = pygame.Surface((pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    pantalla.blit(overlay, (0, 0))

    # 2. Título
    txt_titulo = conf_ranking["titulo"]
    sup_titulo = fuentes["titulo"].render(txt_titulo, True, colores["amarillo"])
    rect_titulo = sup_titulo.get_rect(center=(pantalla.get_width() // 2, 100))
    pantalla.blit(sup_titulo, rect_titulo)

    # 3. Obtener y Mostrar Datos
    top_usuarios = obtener_ranking(3)
    
    ancho_p = pantalla.get_width()
    y_ini = int(pantalla.get_height() * conf_ranking["y_inicio_rel"])
    alto_fila = conf_ranking["alto_fila"]
    
    # Encabezados
    fuente_h = fuentes["subtitulo"]
    sup_name_h = fuente_h.render("USUARIO", True, colores["celeste"])
    sup_score_h = fuente_h.render("PUNTAJE", True, colores["celeste"])
    
    pantalla.blit(sup_name_h, (ancho_p // 2 - 300, y_ini - 60))
    pantalla.blit(sup_score_h, (ancho_p // 2 + 100, y_ini - 60))

    # Filas de datos
    fuente_d = fuentes["cuerpo"]
    for i in range(len(top_usuarios)):
        u = top_usuarios[i]
        color_fila = colores["blanco"]
        if i == 0: color_fila = colores["amarillo"] # Oro para el 1ero
        
        txt_nombre = f"{i+1}. {u['nombre']}"
        txt_puntos = str(u["puntaje_maximo"])
        
        sup_n = fuente_d.render(txt_nombre, True, color_fila)
        sup_p = fuente_d.render(txt_puntos, True, color_fila)
        
        y_fila = y_ini + (i * alto_fila)
        pantalla.blit(sup_n, (ancho_p // 2 - 300, y_fila))
        pantalla.blit(sup_p, (ancho_p // 2 + 100, y_fila))

    # 4. Botón Volver
    actualizar_boton(botones["volver"], pos_mouse)
    dibujar_boton(pantalla, botones["volver"])

    # 5. Eventos
    for evento in eventos:
        if verificar_click_boton(botones["volver"], evento):
            return "menu"
            
    return None
