import pygame

# Módulo de creación y gestión de componentes genéricos de UI (Botones e Inputs).

def crear_boton(x, y, ancho, alto, texto, fuente, color_base, color_hover, color_texto=(255, 255, 255), radio_borde=10):
    """Inicializa la estructura de datos para un botón."""
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
    """Renderiza el botón en la superficie con efectos de sombra y borde."""
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
    """Actualiza visualmente el botón según la posición del cursor."""
    if boton["rect"].collidepoint(posicion_mouse):
        boton["color_actual"] = boton["color_hover"]
        boton["hovered"] = True
    else:
        boton["color_actual"] = boton["color_base"]
        boton["hovered"] = False

def verificar_click_boton(boton, evento):
    """Valida si se ha producido un clic izquierdo dentro del área del botón."""
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if boton["rect"].collidepoint(evento.pos):
            return True
    return False

def crear_input_box(x, y, ancho, alto, fuente, color_activo, color_inactivo, texto_inicial=""):
    """Inicializa la estructura de datos para un campo de entrada de texto."""
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
    """Procesa eventos de mouse y teclado para la entrada de texto."""
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
    """Renderiza la caja de entrada de texto en la superficie."""
    pygame.draw.rect(superficie, (255, 255, 255), input_box["rect"], border_radius=5)
    pygame.draw.rect(superficie, input_box["color_actual"], input_box["rect"], width=3, border_radius=5)
    
    img_texto = input_box["fuente"].render(input_box["texto"], True, (0, 0, 0))
    superficie.blit(img_texto, (input_box["rect"].x + 10, input_box["rect"].y + (input_box["rect"].height - img_texto.get_height()) // 2))
