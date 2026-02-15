import random

"""Módulo encargado de la lógica de procesamiento de la partida."""

def inicializar_estado_juego(preguntas, config_juego, tematica, dificultad):
    """Genera el estado inicial de una partida filtrando preguntas por temática y dificultad."""
    puntos_por_acierto = config_juego.get("puntos_facil", 1)
    puntos_filtro_csv = 1
    
    if dificultad == "pro":
        puntos_por_acierto = config_juego.get("puntos_pro", 2)
        puntos_filtro_csv = 2
    elif dificultad == "experto":
        puntos_por_acierto = config_juego.get("puntos_experto", 5)
        puntos_filtro_csv = 3
    
    preguntas_filtradas = []
    for p in preguntas:
        if p["categoria"].lower() == tematica.lower() and p["puntos"] == puntos_filtro_csv:
            preguntas_filtradas.append(p)
    
    cantidad_objetivo = config_juego.get("cantidad_preguntas", 12)
    
    if len(preguntas_filtradas) < cantidad_objetivo:
        for p in preguntas:
            if p["categoria"].lower() == tematica.lower():
                existe = False
                for pf in preguntas_filtradas:
                    if pf["enunciado"] == p["enunciado"]:
                        existe = True
                        break
                if existe == False:
                    preguntas_filtradas.append(p)
                    if len(preguntas_filtradas) >= cantidad_objetivo:
                        break

    random.shuffle(preguntas_filtradas)
    lista_juego = preguntas_filtradas[:cantidad_objetivo]

    return {
        "preguntas": lista_juego,
        "indice_actual": 0,
        "puntaje": 0,
        "correctas": 0,
        "finalizado": False,
        "botones_opciones": [],
        "dificultad": dificultad,
        "puntos_acierto": puntos_por_acierto,
        "pantalla_final": False,
        "input_box": None,
        "tdah_activo": config_juego.get("estado_tdah", False),
        "tiempo_total": config_juego.get("tiempo_partida_tdah", 60),
        "tiempo_restante": config_juego.get("tiempo_partida_tdah", 60),
        "ultimo_tick": 0,
        "racha_actual": 0,
        "mensaje_racha": "",
        "timer_mensaje": 0,
        "mensajes_motivadores": []
    }

def verificar_respuesta(estado_juego, respuesta_usuario, respuesta_correcta):
    """Valida la respuesta del usuario y actualiza el puntaje en el estado del juego."""
    es_correcta = False
    if respuesta_usuario.strip().lower() == respuesta_correcta.strip().lower():
        estado_juego["puntaje"] = estado_juego["puntaje"] + estado_juego["puntos_acierto"]
        estado_juego["correctas"] = estado_juego["correctas"] + 1
        estado_juego["racha_actual"] = estado_juego["racha_actual"] + 1
        es_correcta = True
        
        if estado_juego.get("tdah_activo", False) == True:
            if estado_juego["racha_actual"] > 0 and estado_juego["racha_actual"] % 3 == 0:
                indice_msg = random.randint(0, len(estado_juego["mensajes_motivadores"]) - 1)
                estado_juego["mensaje_racha"] = estado_juego["mensajes_motivadores"][indice_msg]
                estado_juego["timer_mensaje"] = 60 
    else:
        estado_juego["racha_actual"] = 0
        estado_juego["mensaje_racha"] = ""
        estado_juego["timer_mensaje"] = 0    
    estado_juego["indice_actual"] = estado_juego["indice_actual"] + 1
    estado_juego["botones_opciones"] = []
    estado_juego["input_box"] = None
    
    return es_correcta
