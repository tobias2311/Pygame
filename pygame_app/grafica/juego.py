import pygame
import random
from grafica.componentes import crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton

def inicializar_estado_juego(preguntas, config_juego, tematica, dificultad):
    """
    Prepara el estado inicial filtrado por temática y dificultad.
    """
    # 1. Definir puntaje por respuesta según dificultad elegida
    puntos_por_acierto = 1
    puntos_filtro_csv = 1 # El que buscamos en el CSV
    
    if dificultad == "pro":
        puntos_por_acierto = 2
        puntos_filtro_csv = 2
    elif dificultad == "experto":
        puntos_por_acierto = 5
        puntos_filtro_csv = 3 # En el CSV el max es 3

    # 2. Filtrar preguntas
    preguntas_filtradas = []
    for p in preguntas:
        if p["categoria"].lower() == tematica.lower():
            if p["puntos"] == puntos_filtro_csv:
                preguntas_filtradas.append(p)
    
    if len(preguntas_filtradas) < 5:
        for p in preguntas:
            if p["categoria"].lower() == tematica.lower() and p not in preguntas_filtradas:
                preguntas_filtradas.append(p)

    random.shuffle(preguntas_filtradas)
    cantidad = config_juego.get("cantidad_preguntas", 12)
    lista_juego = preguntas_filtradas[:cantidad]

    return {
        "preguntas": lista_juego,
        "indice_actual": 0,
        "puntaje": 0,
        "correctas": 0,
        "finalizado": False,
        "botones_opciones": [],
        "dificultad": dificultad,
        "puntos_acierto": puntos_por_acierto,
        "pantalla_final": False
    }

def generar_botones_opciones(ancho_p, alto_p, opciones, fuentes, colores):
    """
    Crea los botones de opciones dinámicamente.
    """
    botones = []
    ancho_btn = 600
    alto_btn = 70
    x_centro = ancho_p // 2
    y_inicio = 350
    
    for i in range(len(opciones)):
        col = i % 2
        fila = i // 2
        
        x = x_centro - ancho_btn - 20 if col == 0 else x_centro + 20
        y = y_inicio + (fila * (alto_btn + 20))
        
        btn = crear_boton(
            x = x,
            y = y,
            ancho = ancho_btn,
            alto = alto_btn,
            texto = opciones[i],
            fuente = fuentes["cuerpo"],
            color_base = colores["azul_oscuro"],
            color_hover = colores["celeste"],
            color_texto = colores["blanco"],
            radio_borde = 10
        )
        botones.append(btn)
    
    return botones

def generar_botones_vol_juego(ancho_p, alto_p, d_vol, colores, fuente):
    """Genera los botones de volumen para la pantalla de juego."""
    btn_mas = crear_boton(
        int((ancho_p * d_vol["boton_mas"]["x_relativo"]) - (d_vol["boton_mas"]["ancho"] // 2)),
        int((alto_p * d_vol["boton_mas"]["y_relativo"]) - (d_vol["boton_mas"]["alto"] // 2)),
        d_vol["boton_mas"]["ancho"], d_vol["boton_mas"]["alto"], d_vol["boton_mas"]["texto"],
        fuente, colores[d_vol["boton_mas"]["color_base"]], colores[d_vol["boton_mas"]["color_hover"]]
    )
    btn_menos = crear_boton(
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
    return {"vol_mas": btn_mas, "vol_menos": btn_menos, "mute": btn_mute}

def mostrar_pantalla_juego(pantalla, recursos, fuentes, colores, estado_juego, pos_mouse, eventos, botones_vol, estado_vol):
    """Dibuja y gestiona la lógica de la pantalla de juego."""
    ancho_p = pantalla.get_width()
    alto_p = pantalla.get_height()
    
    # 1. Fondo
    fondo_juego = recursos["fondos"]["juego"]
    pantalla.blit(fondo_juego, (0, 0))

    # --- CONTROLES DE VOLUMEN ---
    for clave in botones_vol:
        actualizar_boton(botones_vol[clave], pos_mouse)
        dibujar_boton(pantalla, botones_vol[clave])

    # --- PANTALLA DE FEEDBACK FINAL ---
    if estado_juego["pantalla_final"]:
        sup_titulo = fuentes["titulo"].render("¡FIN DE LA PARTIDA!", True, colores["amarillo"])
        rect_titulo = sup_titulo.get_rect(center=(ancho_p // 2, 150))
        pantalla.blit(sup_titulo, rect_titulo)

        txt_puntos = f"Puntaje Total: {estado_juego['puntaje']}"
        txt_resumen = f"Respondiste bien {estado_juego['correctas']} de {len(estado_juego['preguntas'])} preguntas"
        
        sup_puntos = fuentes["subtitulo"].render(txt_puntos, True, colores["blanco"])
        sup_resumen = fuentes["cuerpo"].render(txt_resumen, True, colores["celeste"])
        
        pantalla.blit(sup_puntos, sup_puntos.get_rect(center=(ancho_p // 2, 300)))
        pantalla.blit(sup_resumen, sup_resumen.get_rect(center=(ancho_p // 2, 400)))

        btn_volver = crear_boton(ancho_p//2 - 150, 550, 300, 80, "VOLVER AL MENÚ", fuentes["cuerpo"], colores["azul_oscuro"], colores["celeste"])
        actualizar_boton(btn_volver, pos_mouse)
        dibujar_boton(pantalla, btn_volver)

        for evento in eventos:
            if verificar_click_boton(btn_volver, evento):
                return "menu"
            
            # Click en volumen (en pantalla final también)
            if verificar_click_boton(botones_vol["vol_mas"], evento):
                estado_vol["nivel"] = min(1.0, estado_vol["nivel"] + 0.1)
                estado_vol["mute"] = False
                pygame.mixer.music.set_volume(estado_vol["nivel"])
            if verificar_click_boton(botones_vol["vol_menos"], evento):
                estado_vol["nivel"] = max(0.0, estado_vol["nivel"] - 0.1)
                estado_vol["mute"] = False
                pygame.mixer.music.set_volume(estado_vol["nivel"])
            if verificar_click_boton(botones_vol["mute"], evento):
                estado_vol["mute"] = not estado_vol["mute"]
                pygame.mixer.music.set_volume(0.0 if estado_vol["mute"] else estado_vol["nivel"])
        return None

    # --- LÓGICA DE PREGUNTAS ---
    if estado_juego["indice_actual"] >= len(estado_juego["preguntas"]):
        estado_juego["pantalla_final"] = True
        return None

    pregunta_actual = estado_juego["preguntas"][estado_juego["indice_actual"]]
    
    sup_enunciado = fuentes["subtitulo"].render(pregunta_actual["enunciado"], True, colores["blanco"])
    rect_enunciado = sup_enunciado.get_rect(center=(ancho_p // 2, 200))
    pantalla.blit(sup_enunciado, rect_enunciado)

    if not estado_juego["botones_opciones"]:
        estado_juego["botones_opciones"] = generar_botones_opciones(ancho_p, alto_p, pregunta_actual["opciones"], fuentes, colores)

    for btn in estado_juego["botones_opciones"]:
        actualizar_boton(btn, pos_mouse)
        dibujar_boton(pantalla, btn)

    # UI Superior
    texto_puntos = f"Puntaje: {estado_juego['puntaje']}"
    sup_puntos = fuentes["info"].render(texto_puntos, True, colores["amarillo"])
    pantalla.blit(sup_puntos, (50, 100))

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
        
        # Click volumen
        if verificar_click_boton(botones_vol["vol_mas"], evento):
            estado_vol["nivel"] = min(1.0, estado_vol["nivel"] + 0.1)
            estado_vol["mute"] = False
            pygame.mixer.music.set_volume(estado_vol["nivel"])
        if verificar_click_boton(botones_vol["vol_menos"], evento):
            estado_vol["nivel"] = max(0.0, estado_vol["nivel"] - 0.1)
            estado_vol["mute"] = False
            pygame.mixer.music.set_volume(estado_vol["nivel"])
        if verificar_click_boton(botones_vol["mute"], evento):
            estado_vol["mute"] = not estado_vol["mute"]
            pygame.mixer.music.set_volume(0.0 if estado_vol["mute"] else estado_vol["nivel"])

        # Click en opciones
        for i in range(len(estado_juego["botones_opciones"])):
            btn = estado_juego["botones_opciones"][i]
            if verificar_click_boton(btn, evento):
                if pregunta_actual["opciones"][i] == pregunta_actual["respuesta_correcta"]:
                    estado_juego["puntaje"] += estado_juego["puntos_acierto"]
                    estado_juego["correctas"] += 1
                estado_juego["indice_actual"] += 1
                estado_juego["botones_opciones"] = [] 
                return None
    return None
