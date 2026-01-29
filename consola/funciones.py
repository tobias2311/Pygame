from datos import enunciados_boss
import time
from colorama import Fore, Style
from funciones_minimas import *
from boss import empezar_boss, retornar_puntaje
from datos import preguntas_cultura_general,preguntas_frases_deportivas,preguntas_frases_populares
import random
from funciones_basicas import loading_quieto,crear_loading
from minijuego import *

def abrir_menu(nombre):

    while True:
        
        print(Fore.RED + "-- DESAFIO MENTAL --" + Style.RESET_ALL)
        print("""
1 - Comenzar Juego.
2 - Guia.
3 - Estadisticas.
4 - Mini Juego.
5 - Salir.""")
       
        respuesta = input(Fore.LIGHTGREEN_EX + "Elegi una opcion: " + Style.RESET_ALL)

        match respuesta:
            case "1":
                comenzar_juego(nombre)
            case "2":
                abrir_guia()
            case "3":
                abrir_ajustes(nombre)
            case "4":
                juego_memoria()
            case "5":
                break
            case _:
                print("Elegi una opcion valida")
                time.sleep(1)
                limpiar_pantalla()
            
# PARTE DEL MENU

def comenzar_juego(nombre):

    limpiar_pantalla()
    puntaje_acumulado = 0.00
    tematica = elegir_tematica()
    dificultad = elegir_dificultad()

    limpiar_pantalla()
    print(Fore.RED + f"\ntematica elegida {Fore.CYAN + tematica + Fore.RED}🤔 en {Fore.GREEN + dificultad + Style.RESET_ALL} ❗ " + Style.RESET_ALL)
    time.sleep(3)
    crear_loading()
    limpiar_pantalla()

    iniciar_juego(dificultad, tematica, puntaje_acumulado, nombre)
                   
def elegir_tematica():
    print(Fore.CYAN + "Tematicas Disponibles: " + Style.RESET_ALL)
    print("""
    A- Deportes.
    B- Cultura General.
    C- Frases Populares.""")
    while True:
        tematica = input(Fore.YELLOW + "\nelegi con (a, b, c): " + Style.RESET_ALL)
        match tematica:
            case "a":
                tematica = "Deportes"
                break
            case "b":
                tematica = "Cultura General"
                break
            case "c":
                tematica = "Frases Populares"
                break
            case _:
                print("Elegi una opcion valida! ")              
    return tematica            
              
def elegir_dificultad():
    print(Fore.CYAN + "Dificultades disponibles:" + Style.RESET_ALL)
    print(""" 
    A- Facil.
    B- Pro. 
    C- Experto.""" + Style.RESET_ALL)

    while True:
        dificultad = input(Fore.YELLOW + "\nelegi con (a, b, c): " + Style.RESET_ALL)
        match dificultad:
            case "a":
                dificultad = "Facil"
            case "b":
                dificultad = "Pro"
            case "c":
                dificultad = "Experto"
            case _:
                print(Fore.YELLOW + "Elegi una dificultad valida ! " + Style.RESET_ALL)
        return dificultad
    
def abrir_guia():
    limpiar_pantalla()
    
    print("--- GUIA ---")
    def pausar_y_limpiar():
        input(Fore.LIGHTBLACK_EX + "\nPresioná Enter para continuar..." + Style.RESET_ALL)
        limpiar_pantalla()
    
    limpiar_pantalla()
    
    print(Fore.CYAN + "--- GUÍA DEL JUEGO: COMPLETA LA FRASE ---" + Style.RESET_ALL)
    print("Este juego pone a prueba tu conocimiento con frases populares, cultura general y deportes.")
    print("Tu misión: completar correctamente la frase o responder bien la pregunta.")
    pausar_y_limpiar()

    print(Fore.YELLOW + "1️⃣ Inicio del juego:" + Style.RESET_ALL)
    print("Al iniciar, elegís una temática y una dificultad.")
    print("Temáticas: Frases populares, Cultura general, Deportes.")
    print("Dificultades: Fácil, Pro y Experto.")
    pausar_y_limpiar()

    print(Fore.YELLOW + "2️⃣ Desarrollo de la partida:" + Style.RESET_ALL)
    print("Se te harán 12 preguntas según la temática y dificultad elegidas.")
    print("- Fácil: 4 opciones.")
    print("- Pro: 4 opciones.")
    print("- Experto: sin opciones, escribís toda la frase.")
    pausar_y_limpiar()

    print(Fore.YELLOW + "3️⃣ Cómo responder:" + Style.RESET_ALL)
    print("- En modos Fácil/Pro, respondés con la letra (a, b, c o d).")
    print("- En Experto, escribís la frase completa.")
    print("- Si acertás, sumás puntos. Si fallás, se restaran puntos.")
    print("   ✔ Fácil: +1 punto\n   ✔ Pro: +2 puntos\n   ✔ Experto: +5 puntos")
    pausar_y_limpiar()

    print(Fore.YELLOW + "4️⃣ Resultados y final del juego:" + Style.RESET_ALL)
    print("Al terminar las 12 preguntas, verás:")
    print("- Tus aciertos y errores.")
    print("- Tu puntaje final.")
    print("- El promedio de tiempo que tardaste por pregunta.")
    pausar_y_limpiar()

    limpiar_pantalla()
    print(Fore.MAGENTA + "--- GUÍA RÁPIDA: JEFES DEL JUEGO ---" + Style.RESET_ALL)
    print("✔ Cada vez que acertás 3 preguntas seguidas, aparece un JEFE.")
    print("✔ Hay 2 tipos: uno de razonamiento matemático y otro de programación.")
    pausar_y_limpiar()

    print("✅ Si acertás la pregunta del jefe:")
    print("- Ganás un BOOST de puntaje:")
    print("   🧠 Razonamiento: +35%")
    print("   💻 Programación: +25%")
    print("- El boost se mantiene hasta que falles una pregunta.")
    pausar_y_limpiar()

    print("❌ Si fallás:")
    print("- Perdés el boost.")
    print("- Tenés que volver a acertar 3 seguidas para otro intento.")
    pausar_y_limpiar()

    print(Fore.CYAN + "¡Listo! Ya sabés cómo se juega." + Style.RESET_ALL)
    input(Fore.LIGHTBLACK_EX + "\nPresioná Enter para volver al menú..." + Style.RESET_ALL)
    limpiar_pantalla()

def abrir_ajustes(nombre):
    limpiar_pantalla()
    
    with open(ruta_archivo, "r") as archivo:
        datos = json.load(archivo)
        
    print(Fore.YELLOW +  "--- AJUSTES ---" + Style.RESET_ALL)
    
    for intervalo in datos:
        user = datos[intervalo]
        nombre_us = user["nombre"]
        if nombre == nombre_us:
            print(Fore.RED + f"stats de {nombre} maestria: {user["rango"]}\n" + Style.RESET_ALL)
            print(f"ultimo puntaje: {user["ultimo_puntaje"]}") 
            print(f"respuestas correctas: {user["total_respuestas_correctas"]}")
            print(f"puntaje: {user["total_puntaje_acumulado"]}")
            print(f"veces jugadas: {user["total_de_veces_jugadas"]}")
            print(f"aciertos en total: {user["total_aciertos"]}")
            print(f"errores en total: {user["total_errores"]}")
            print(f"maxima puntuacion: {user["puntaje_max"]}") 
            print(f"porcentaje de winrate: {user["porcentaje_winrate"]}%") 

    input(Fore.YELLOW + "\n ENTER para volver al menu..." + Style.RESET_ALL)
    
    limpiar_pantalla()


def matchear_tematica(tematica):
    
        match tematica:
            case "Frases Populares":
                tematica_preguntas = preguntas_frases_populares
            case "Deportes":
                tematica_preguntas = preguntas_frases_deportivas
            case "Cultura General":
                tematica_preguntas = preguntas_cultura_general    
                
        return tematica_preguntas   

#-   INICIAR JUEGO   - ################################################################################################

def iniciar_juego(dificultad, tematica, puntaje_acumulado_inicial, nombre):
    puntaje_total_juego = puntaje_acumulado_inicial
    respuestas_correctas_juego = 0
    tematica_csv = matchear_tematica(tematica)
    jefe = ""
    inicio = time.time()
    respuestas_ejecutar_boss = 3
    cantidad_respuestas_seguidas = 0
    preguntas = 12

    random.shuffle(tematica_csv)

    for pregunta in tematica_csv[:preguntas]:
        
        puntaje_total_juego, respuestas_correctas_juego, cantidad_respuestas_seguidas, jefe = manejar_pregunta(
            pregunta, dificultad, jefe, cantidad_respuestas_seguidas,
            respuestas_ejecutar_boss, nombre, puntaje_total_juego,
            respuestas_correctas_juego
        )
        loading_quieto()

    final = time.time()
    tiempo = final - inicio

    terminar_juego(puntaje_total_juego, respuestas_correctas_juego, preguntas, nombre, tiempo)

def manejar_pregunta(pregunta, dificultad, jefe, respuestas_seguidas, limite_boss, nombre, puntaje_total, respuestas_correctas):
    limpiar_pantalla()
    printear_enunciado(pregunta)
    respuesta_correcta_opcion = printear_respuestas(dificultad, pregunta)
    puntaje_ganado = preguntar_por_respuesta(respuesta_correcta_opcion, dificultad, pregunta, jefe)

    puntaje_ganado = aplicar_boost_jefe(jefe, puntaje_ganado, puntaje_total)

    if puntaje_ganado > 0:
        respuestas_correctas += 1
        respuestas_seguidas += 1
    else:
        respuestas_seguidas = 0

    if respuestas_seguidas == limite_boss - 1:
        anunciar_boss_cercano()
    elif respuestas_seguidas == limite_boss:
        respuestas_seguidas = 0
        jefe = iniciar_boss(nombre, puntaje_total)
    else:
        jefe = ""

    puntaje_total += puntaje_ganado
    return puntaje_total, respuestas_correctas, respuestas_seguidas, jefe

def aplicar_boost_jefe(jefe, puntaje, puntaje_total):
    match jefe:
        case "jefe_gonza":
            return puntaje * 1.25
        case "dr_insano":
            return puntaje * 1.30
        case "pierde":
            return puntaje_total - retornar_puntaje(puntaje_total)
        case _:
            return puntaje

def anunciar_boss_cercano():
    print(Fore.LIGHTWHITE_EX + "\nse escucha de fondo*" + Style.RESET_ALL)
    print(Fore.LIGHTRED_EX + "HMM interesante... solo una mas para conocernos.. 😡\n" + Style.RESET_ALL)
    input(Fore.YELLOW + "Enter para continuar.. " + Style.RESET_ALL)

def iniciar_boss(nombre, puntaje_total):
    print(Fore.LIGHTRED_EX + "\nAHORA ME TOCA A MI 👀‼ " + Style.RESET_ALL)
    time.sleep(3)
    return empezar_boss(nombre, enunciados_boss, puntaje_total)


   
        

    