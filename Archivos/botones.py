import pygame

def crear_boton_texto(texto, fuente, color_texto, color_fondo, color_borde, color_fondo_hover, posicion, dimension):
    """Crea un diccionario que representa un botón con texto"""
    ancho, alto = dimension
    x, y = posicion
    
    # Renderizar el texto
    superficie_texto = fuente.render(texto, True, color_texto)
    
    # Crear el rectángulo del botón
    rectangulo = pygame.Rect(x, y, ancho, alto)
    
    return {
        "Texto": texto,
        "Fuente": fuente,
        "ColorTexto": color_texto,
        "ColorFondo": color_fondo,
        "ColorBorde": color_borde,
        "ColorFondoHover": color_fondo_hover,
        "Posicion": posicion,
        "Dimension": dimension,
        "Rectangulo": rectangulo,
        "SuperficieTexto": superficie_texto
    }

def dibujar_boton(ventana, boton):
    """Dibuja un botón en la ventana"""
    rectangulo = boton["Rectangulo"]
    color_fondo = boton["ColorFondo"]
    color_borde = boton["ColorBorde"]
    superficie_texto = boton["SuperficieTexto"]
    
    # Dibujar el fondo del botón
    pygame.draw.rect(ventana, color_fondo, rectangulo)
    # Dibujar el borde
    pygame.draw.rect(ventana, color_borde, rectangulo, 3)
    
    # Calcular posición del texto para centrarlo
    texto_rect = superficie_texto.get_rect(center=rectangulo.center)
    ventana.blit(superficie_texto, texto_rect)
