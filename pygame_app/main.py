import pygame
import sys
import os

# Agregamos el directorio raíz al path para importar correctamente los módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logica.cargar_archivos import cargar_configuracion
from grafica.carga_recursos import cargar_recursos_graficos, cargar_fuentes
from grafica.componentes import Boton

def inicializar_ventana(config_ventana):
    """
    Configura la ventana usando los valores del JSON.
    """
    ancho = config_ventana["ancho"]
    alto = config_ventana["alto"]
    titulo = config_ventana["titulo"]
    
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption(titulo)
    return pantalla

def main():
    # 1. Inicialización de Pygame
    pygame.init()
    pygame.mixer.init()

    # 2. Carga de Configuración
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_config = os.path.join(ruta_base, "data", "config.json")
    config = cargar_configuracion(ruta_config)

    conf_ventana = config["ventana"]
    colores = config["colores"]
    conf_menu = config["ui"]["menu_principal"]
    conf_fuentes = config["fuentes"]
    
    # 3. Configuración de la Ventana
    pantalla = inicializar_ventana(conf_ventana)
    ancho_p = pantalla.get_width()
    alto_p = pantalla.get_height()

    # 4. Carga de Recursos
    recursos = cargar_recursos_graficos()
    fuentes = cargar_fuentes(conf_fuentes)
    fuente_botones = fuentes["subtitulo"]

    # 5. Creación de Botones (Manual y Directa desglosando el JSON)
    # Extraemos manualmente los datos de cada botón del diccionario para evitar bucles complejos
    
    # BOTÓN INICIO
    datos_inicio = conf_menu["boton_inicio"]
    btn_inicio = Boton(
        x = int((ancho_p * datos_inicio["x_relativo"]) - (datos_inicio["ancho"] // 2)),
        y = int((alto_p * datos_inicio["y_relativo"]) - (datos_inicio["alto"] // 2)),
        ancho = datos_inicio["ancho"],
        alto = datos_inicio["alto"],
        texto = datos_inicio["texto"],
        fuente = fuente_botones,
        color_base = colores[datos_inicio["color_base"]],
        color_hover = colores[datos_inicio["color_hover"]],
        color_texto = colores[datos_inicio["color_texto"]],
        radio_borde = datos_inicio["radio_borde"]
    )

    # BOTÓN CONFIGURACIÓN
    datos_config = conf_menu["boton_config"]
    btn_config = Boton(
        x = int((ancho_p * datos_config["x_relativo"]) - (datos_config["ancho"] // 2)),
        y = int((alto_p * datos_config["y_relativo"]) - (datos_config["alto"] // 2)),
        ancho = datos_config["ancho"],
        alto = datos_config["alto"],
        texto = datos_config["texto"],
        fuente = fuente_botones,
        color_base = colores[datos_config["color_base"]],
        color_hover = colores[datos_config["color_hover"]],
        color_texto = colores[datos_config["color_texto"]],
        radio_borde = datos_config["radio_borde"]
    )

    # BOTÓN SALIR
    datos_salir = conf_menu["boton_salir"]
    btn_salir = Boton(
        x = int((ancho_p * datos_salir["x_relativo"]) - (datos_salir["ancho"] // 2)),
        y = int((alto_p * datos_salir["y_relativo"]) - (datos_salir["alto"] // 2)),
        ancho = datos_salir["ancho"],
        alto = datos_salir["alto"],
        texto = datos_salir["texto"],
        fuente = fuente_botones,
        color_base = colores[datos_salir["color_base"]],
        color_hover = colores[datos_salir["color_hover"]],
        color_texto = colores[datos_salir["color_texto"]],
        radio_borde = datos_salir["radio_borde"]
    )

    # 6. Loop Principal
    corriendo = True
    while corriendo == True:
        pos_mouse = pygame.mouse.get_pos()
        
        # --- Gestión de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            # Verificamos clicks uno por uno
            if btn_inicio.fue_clicado(evento) == True:
                print("Iniciando juego...")
            
            if btn_config.fue_clicado(evento) == True:
                print("Abriendo configuración...")
                
            if btn_salir.fue_clicado(evento) == True:
                corriendo = False

        # --- Lógica de Actualización ---
        btn_inicio.actualizar(pos_mouse)
        btn_config.actualizar(pos_mouse)
        btn_salir.actualizar(pos_mouse)

        # --- Dibujado ---
        fondo_menu = recursos["fondos"]["menu"]
        pantalla.blit(fondo_menu, (0, 0))
        
        # Título
        sup_titulo = fuentes["titulo"].render(conf_ventana["titulo"].upper(), True, colores["blanco"])
        rect_titulo = sup_titulo.get_rect(center=(ancho_p // 2, alto_p // 5))
        pantalla.blit(sup_titulo, rect_titulo)

        # Dibujamos cada botón manualmente
        btn_inicio.dibujar(pantalla)
        btn_config.dibujar(pantalla)
        btn_salir.dibujar(pantalla)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
