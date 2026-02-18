import pygame

"""Módulo de creación y gestión de componentes genéricos de UI (Botones e Inputs)."""

def crear_boton(x, y, ancho, alto, texto, fuente, color_base, color_hover, color_texto=(255, 255, 255), radio_borde=10):
    boton = {
        "rect": pygame.Rect(x, y, ancho, alto),
        "texto": texto,
        "fuente": fuente,
        "color_base": color_base,
        "color_hover": color_hover,
        "color_texto": color_texto,
        "radio_borde": radio_borde,
        "color_actual": color_base,
        "hovered": False
    }
    return boton

def dibujar_boton(superficie, boton):
    sombra_rect = boton["rect"].copy()
    sombra_rect.x += 4
    sombra_rect.y += 4
    pygame.draw.rect(superficie, (20, 20, 20), sombra_rect, border_radius=boton["radio_borde"])

    pygame.draw.rect(superficie, boton["color_actual"], boton["rect"], border_radius=boton["radio_borde"])
    pygame.draw.rect(superficie, (200, 200, 200), boton["rect"], width=2, border_radius=boton["radio_borde"])

    img_texto = boton["fuente"].render(boton["texto"], True, boton["color_texto"])
    rect_texto = img_texto.get_rect(center=boton["rect"].center)
    superficie.blit(img_texto, rect_texto)

def actualizar_boton(boton, posicion_mouse):
    if boton["rect"].collidepoint(posicion_mouse):
        boton["color_actual"] = boton["color_hover"]
        boton["hovered"] = True
    else:
        boton["color_actual"] = boton["color_base"]
        boton["hovered"] = False

def verificar_click_boton(boton, evento):
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if boton["rect"].collidepoint(evento.pos):
            return True
    return False

def crear_input_box(x, y, ancho, alto, fuente, color_activo, color_inactivo, texto_inicial=""):
    input_box = {
        "rect": pygame.Rect(x, y, ancho, alto),
        "fuente": fuente,
        "color_activo": color_activo,
        "color_inactivo": color_inactivo,
        "color_actual": color_inactivo,
        "texto": texto_inicial,
        "activo": False
    }
    
    if input_box["activo"] == True:
        input_box["color_actual"] = color_activo
    else:
        input_box["color_actual"] = color_inactivo
    
    return input_box

def manejar_evento_input(input_box, evento):
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if input_box["rect"].collidepoint(evento.pos):
            if input_box["activo"] == True:
                input_box["activo"] = False
            else:
                input_box["activo"] = True
        else:
            input_box["activo"] = False
        
        if input_box["activo"] == True:
            input_box["color_actual"] = input_box["color_activo"]
        else:
            input_box["color_actual"] = input_box["color_inactivo"]
    
    if evento.type == pygame.KEYDOWN:
        if input_box["activo"]:
            if evento.key == pygame.K_RETURN:
                return input_box["texto"] 
            elif evento.key == pygame.K_BACKSPACE:
                input_box["texto"] = input_box["texto"][:-1]
            else:
                if len(input_box["texto"]) < 50: 
                    input_box["texto"] += evento.unicode
    return None

def dibujar_input_box(superficie, input_box):
    pygame.draw.rect(superficie, (255, 255, 255), input_box["rect"], border_radius=5)
    pygame.draw.rect(superficie, input_box["color_actual"], input_box["rect"], width=3, border_radius=5)
    
    img_texto = input_box["fuente"].render(input_box["texto"], True, (0, 0, 0))
    superficie.blit(img_texto, (input_box["rect"].x + 10, input_box["rect"].y + (input_box["rect"].height - img_texto.get_height()) // 2))

def crear_switch(x, y, ancho, alto, estado_inicial, fuente, colores):
    radio_handle = (alto // 2) - 4
    x_off = x + radio_handle + 4
    x_on = x + ancho - radio_handle - 4
    
    x_inicio = x_off
    if estado_inicial == True:
        x_inicio = x_on
    
    switch = {
        "rect": pygame.Rect(x, y, ancho, alto),
        "activo": estado_inicial,
        "x_actual": float(x_inicio),
        "x_objetivo": float(x_inicio),
        "x_off": float(x_off),
        "x_on": float(x_on),
        "y_centro": y + (alto // 2),
        "radio_handle": radio_handle,
        "fuente": fuente,
        "colores": colores,
        "hovered": False
    }
    return switch

def actualizar_switch(switch, posicion_mouse):
    if switch["rect"].collidepoint(posicion_mouse):
        switch["hovered"] = True
    else:
        switch["hovered"] = False
    
    distancia = switch["x_objetivo"] - switch["x_actual"]
    if abs(distancia) > 0.1:
        switch["x_actual"] += distancia * 0.2

def dibujar_switch(superficie, switch):
    if switch["activo"] == True:
        color_fondo = switch["colores"]["on"]
        txt = "ON"
    else:
        color_fondo = switch["colores"]["off"]
        txt = "OFF"
    
    sombra_rect = switch["rect"].copy()
    sombra_rect.y += 2
    pygame.draw.rect(superficie, (20, 20, 20), sombra_rect, border_radius=switch["rect"].height // 2)
    
    pygame.draw.rect(superficie, color_fondo, switch["rect"], border_radius=switch["rect"].height // 2)
    pygame.draw.rect(superficie, (220, 220, 220), switch["rect"], width=2, border_radius=switch["rect"].height // 2)
    
    color_txt = (255, 255, 255)
    img_txt = switch["fuente"].render(txt, True, color_txt)
    
    if switch["activo"] == True:
        pos_txt = (switch["rect"].x + 15, switch["y_centro"] - img_txt.get_height() // 2)
    else:
        pos_txt = (switch["rect"].right - img_txt.get_width() - 15, switch["y_centro"] - img_txt.get_height() // 2)
    
    superficie.blit(img_txt, pos_txt)

    color_handle = (255, 255, 255)
    if switch["hovered"] == True:
        pygame.draw.circle(superficie, (255, 255, 255, 100), (int(switch["x_actual"]), switch["y_centro"]), switch["radio_handle"] + 3)
        
    pygame.draw.circle(superficie, color_handle, (int(switch["x_actual"]), switch["y_centro"]), switch["radio_handle"])
    pygame.draw.circle(superficie, (200, 200, 200), (int(switch["x_actual"]), switch["y_centro"]), switch["radio_handle"], width=1)

def verificar_click_switch(switch, evento):
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if switch["rect"].collidepoint(evento.pos):
            if switch["activo"] == True:
                switch["activo"] = False
            else:
                switch["activo"] = True
            
            if switch["activo"] == True:
                switch["x_objetivo"] = switch["x_on"]
            else:
                switch["x_objetivo"] = switch["x_off"]
                
            return True
    return False
