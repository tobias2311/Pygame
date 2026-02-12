import pygame

class Boton:
    def __init__(self, x, y, ancho, alto, texto, fuente, color_base, color_hover, color_texto=(255, 255, 255), radio_borde=10):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.fuente = fuente
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.radio_borde = radio_borde
        self.color_actual = color_base
        self.hovered = False

    def dibujar(self, superficie):
        # Dibujar sombra (opcional para estilo premium)
        sombra_rect = self.rect.copy()
        sombra_rect.x += 4
        sombra_rect.y += 4
        pygame.draw.rect(superficie, (20, 20, 20), sombra_rect, border_radius=self.radio_borde)

        # Dibujar botón principal
        pygame.draw.rect(superficie, self.color_actual, self.rect, border_radius=self.radio_borde)
        
        # Dibujar borde sutil
        pygame.draw.rect(superficie, (200, 200, 200), self.rect, width=2, border_radius=self.radio_borde)

        # Renderizar texto
        img_texto = self.fuente.render(self.texto, True, self.color_texto)
        rect_texto = img_texto.get_rect(center=self.rect.center)
        superficie.blit(img_texto, rect_texto)

    def actualizar(self, posicion_mouse):
        """
        Cambia el estado del botón si el mouse está encima.
        """
        if self.rect.collidepoint(posicion_mouse):
            self.color_actual = self.color_hover
            self.hovered = True
        else:
            self.color_actual = self.color_base
            self.hovered = False

    def fue_clicado(self, evento):
        """
        Retorna True si el evento es un click izquierdo sobre el botón.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.hovered:
                return True
        return False

class InputBox:
    def __init__(self, x, y, ancho, alto, fuente, color_activo, color_inactivo, texto_inicial=""):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.fuente = fuente
        self.color_activo = color_activo
        self.color_inactivo = color_inactivo
        self.color_actual = color_inactivo
        self.texto = texto_inicial
        self.activo = False

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace click en el input box
            if self.rect.collidepoint(evento.pos):
                self.activo = not self.activo
            else:
                self.activo = False
            self.color_actual = self.color_activo if self.activo else self.color_inactivo
        
        if evento.type == pygame.KEYDOWN:
            if self.activo:
                if evento.key == pygame.K_RETURN:
                    return self.texto # Retorna el texto al presionar Enter
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                else:
                    # Limitar longitud si es necesario
                    if len(self.texto) < 20: 
                        self.texto += evento.unicode
        return None

    def dibujar(self, superficie):
        # Fondo blanco para el input
        pygame.draw.rect(superficie, (255, 255, 255), self.rect, border_radius=5)
        # Borde de estado
        pygame.draw.rect(superficie, self.color_actual, self.rect, width=3, border_radius=5)
        
        # Renderizar el texto actual
        img_texto = self.fuente.render(self.texto, True, (0, 0, 0))
        superficie.blit(img_texto, (self.rect.x + 10, self.rect.y + (self.rect.height - img_texto.get_height()) // 2))
