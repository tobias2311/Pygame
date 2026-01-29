from colorama import *
import json
from funciones_basicas import limpiar_pantalla
from boss import extraer_boost
from datos import ruta_archivo, respuestas

# PRINTEA EL ENUNCIADO CON LAS OPCIONES (DEPENDE)     
def printear_enunciado(pregunta): 
    print("Pregunta:")
    print(Fore.BLUE + pregunta["enunciado"] + Style.RESET_ALL)
    print() 
    
def printear_respuestas(dificultad, pregunta): 
    respuesta_correcta_opcion = ""
    if dificultad != "Experto":
        for j in range(len(respuestas)):
            print(f"({respuestas[j]}) {pregunta["opciones"][j]}")
            if pregunta["opciones"][j] == pregunta["respuesta_correcta"]:
                respuesta_correcta_opcion = respuestas[j]
    else:
        print(Fore.LIGHTCYAN_EX + "Recorda: escribi la respuesta exacta, sin opciones multiples." + Style.RESET_ALL)
    return respuesta_correcta_opcion

def preguntar_por_respuesta(respuesta_correcta_opcion, dificultad, pregunta, jefe):
        puntaje_ganado = 0
        boost = extraer_boost(jefe)  
        if boost == 25:
            color = Fore.GREEN
        else:
            color = Fore.RED
        
        respuesta_usuario = validar_respuesta(dificultad)
        
        if respuesta_usuario == respuesta_correcta_opcion: 
            if jefe != "" and jefe != "pierde":
                print(color + f"Sumando el boost del {boost}% por vencer al {jefe}" + Style.RESET_ALL)
            if dificultad == "Facil":
                print(Fore.GREEN + "¡Correcto!" + Style.RESET_ALL)
            puntaje_ganado = calcular_puntaje(dificultad, pregunta) # Calcula el puntaje
            
        elif respuesta_usuario == pregunta["respuesta_correcta"]:
            if jefe != "" and jefe != "pierde":
                print(color + f"Sumando el boost del {boost}% por vencer al {jefe}" + Style.RESET_ALL)
                puntaje_ganado = pregunta["puntos"] * 5
            else:
                puntaje_ganado = - (pregunta["puntos"] - 1)    
            if dificultad == "Facil":
                print(Fore.YELLOW  + "Siguiente..." + Style.RESET_ALL)     
            
        else:
            puntaje_ganado = - (pregunta["puntos"] - 1)
            if dificultad == "Facil":
                print(Fore.RED + f"Incorrecto. La respuesta correcta era: ({respuesta_correcta_opcion}) {pregunta['respuesta_correcta']}" + Style.RESET_ALL)
        return puntaje_ganado # aca devolvemos el puntaje ganado por pregunta

# VALIDA QUE LA RESPUESTA SE VALIDA
def validar_respuesta(dificultad):
    try:
        if dificultad != "Experto":
            while True:
                print(Fore.YELLOW + "Elegí una opción válida (a, b, c, d)." + Style.RESET_ALL)
                respuesta_usuario = input("\nTu respuesta: ").lower()

                if respuesta_usuario in respuestas:
                    return respuesta_usuario
                else:
                    print(Fore.RED + "Opción inválida. Intentá de nuevo." + Style.RESET_ALL)
        else:
            respuesta_usuario = input("\nTu respuesta: ")
            return respuesta_usuario

    except Exception as e:
        print(Fore.RED + f"Error inesperado al leer la respuesta: {e}" + Style.RESET_ALL)
              
# CALCULA EL PUNTAJE
def calcular_puntaje(dificultad, pregunta):
    
    if dificultad == "Facil": 
        puntaje = pregunta["puntos"] * 0.75
    elif dificultad == "Pro":
        puntaje = pregunta["puntos"] * 1.96
    else: 
        puntaje = 0
    
    return puntaje    
  
# TERIMNAR JUEGO, Muestra puntaje y guarda estadisticas
def terminar_juego(puntaje_acumulado, respuestas_correctas, total_preguntas_tematica, nombre, tiempo):          
    limpiar_pantalla()
    print(f"Tu puntaje fue de: {puntaje_acumulado:.2f}") 
    print(Fore.YELLOW + f"Juego TERMINADO! Acertaste {respuestas_correctas} de {total_preguntas_tematica} preguntas en {tiempo:.0f} segundos⌚ !!" + Style.RESET_ALL)

    calcular_y_guardar_estadisticas(puntaje_acumulado, respuestas_correctas, total_preguntas_tematica, nombre)
    
    input("\nENTER para volver al menu...")
    limpiar_pantalla()
    
def calcular_y_guardar_estadisticas(puntaje_acumulado, respuestas_correctas, total_preguntas_tematica, nombre):
    with open(ruta_archivo, "r") as archivo:
        datos = json.load(archivo)
        
        for intervalo in datos:
            user = datos[intervalo]
            nombre_user = user["nombre"]
            if nombre_user == nombre:
                
                user["ultimo_puntaje"] = round(puntaje_acumulado,2)
                user["total_respuestas_correctas"] += respuestas_correctas
                user["total_puntaje_acumulado"] += puntaje_acumulado
                user["total_de_veces_jugadas"] += 1
                user["total_aciertos"] += respuestas_correctas
                user["total_errores"] += (total_preguntas_tematica - respuestas_correctas)
                if puntaje_acumulado > user["puntaje_max"]: 
                    user["puntaje_max"] = puntaje_acumulado
                
                total_de_veces_jugadas = user["total_de_veces_jugadas"] 
                total_aciertos = user["total_aciertos"]
                
                preguntas_respondidas_en_total = (total_de_veces_jugadas * total_preguntas_tematica)    
                if preguntas_respondidas_en_total > 0:
                    winrate = (total_aciertos / preguntas_respondidas_en_total) * 100
                else:
                    winrate = 0
                user["porcentaje_winrate"] = round(winrate, 1)  
                
                if user["total_de_veces_jugadas"] >= 5:
                    if user["porcentaje_winrate"] < 20:
                        user["rango"] = "Bronce🥉"
                    elif user["porcentaje_winrate"] < 40:
                        user["rango"] = "Plata🥈"
                    elif user["porcentaje_winrate"] < 60:
                        user["rango"] = "Oro🥇"
                    else:
                        user["rango"] = "Leyenda💎"       
              
                with open(ruta_archivo, "w") as archivo:
                    json.dump(datos, archivo, indent= 4)

