from colorama import *
import time
import random
from funciones_basicas import limpiar_pantalla, loading_quieto

def matchear_boss(enunciados_boss):
    matchear = random.randint(1, 2)
    if matchear == 1:
        boss = enunciados_boss["dr_insano"]
    else:
        boss = enunciados_boss["jefe_gonza"]
    return boss    

def printear_jefe(jefe, mensaje, bienvenida):
    jefe_cerrado = jefe["dibujo"]
    jefe_abierto = jefe["dibujo_abierto"]
    for i in range(6, 0, -1):
        nombre_jefe = jefe["nombre"]
        limpiar_pantalla()
        print(Fore.YELLOW + f"\r⏳ {bienvenida} {nombre_jefe} en {i} segundos... " + Style.RESET_ALL)
        print(jefe_cerrado)
        print(f"\n{mensaje}")
        time.sleep(0.5)
        limpiar_pantalla()
        print(Fore.YELLOW + f"\r⏳ {bienvenida} {nombre_jefe} en {i} segundos... " + Style.RESET_ALL)
        print(jefe_abierto)
        print(f"{mensaje}")
        time.sleep(0.2)

def empezar_boss(nombre,enunciados_boss, puntaje_total_juego):
    limpiar_pantalla()
    jefe = matchear_boss(enunciados_boss)
    bienvenida = "Esta por aparecer"
    mensaje = ""
    printear_jefe(jefe, mensaje, bienvenida)
    print(Fore.RED + f"\n{jefe['nombre']}: estas listo {nombre}?" + Style.RESET_ALL)
    loading_quieto()
    time.sleep(3)
    limpiar_pantalla()
    jefe = preguntas_boss(enunciados_boss, jefe["nombre"], puntaje_total_juego)
    return jefe

def preguntas_boss(enunciados_boss, jefe, puntaje_total_juego):
    preguntas = []
    categoria = Fore.BLUE + "" + Style.RESET_ALL
    cara = ""
    for clave in enunciados_boss:
        if enunciados_boss[clave]["nombre"] == jefe:
            preguntas = enunciados_boss[clave]["preguntas"]
            categoria = enunciados_boss[clave]["categoria"]
            cara = enunciados_boss[clave]["dibujo"]
            break

    if preguntas:
        pregunta = random.choice(preguntas)
        print(Fore.RED + f"{cara}\n {Fore.BLUE} Experto en: {categoria} \n" + Style.RESET_ALL)
        enunciado = pregunta["enunciado"]
        print(Fore.RED + enunciado + Style.RESET_ALL)
        print()
        respuesta = input(Fore.YELLOW + "A ver que tan bueno sos 🤣: " + Style.RESET_ALL)
        if respuesta == pregunta["respuesta_correcta"]:
            print(Fore.GREEN + "EXCELENTE !\n" + Style.RESET_ALL)
            if jefe == "jefe_gonza":
                print(Fore.GREEN + "Obtenes un boost de +25% por pregunta! " + Style.RESET_ALL)
                extraer_boost(jefe)
            else:
                print(Fore.GREEN + "Obtenes un boost de +35% por pregunta! " + Style.RESET_ALL)
                extraer_boost(jefe)
           
        else:
            respuesta_incorrecta_boss(cara)
            retornar_puntaje(puntaje_total_juego)
            jefe = "pierde"
            
    return jefe

def extraer_boost(jefe):
    if jefe == "jefe_gonza":
       boost = 25
    else:
        boost = 35
    return boost            

def respuesta_incorrecta_boss(cara):
    limpiar_pantalla()

    respuesta = Fore.RED + "\nRESPUESTA INCORRECTA👿🤣❗ "
    agregar = "JA"
    for i in range(11):
        print(f"\n {cara} \n")
        print(respuesta)
        respuesta = respuesta + agregar
        time.sleep(0.1)
        limpiar_pantalla()
    
    Style.RESET_ALL   

def retornar_puntaje(puntaje_total_juego):
    
    puntaje_perdido = puntaje_total_juego * 0.25
    print(Fore.YELLOW + f"\n Acabas de perder el 25% del puntaje sumado 💔😢")
    input(Fore.YELLOW + "\nEnter.." + Style.RESET_ALL)
    return puntaje_perdido
