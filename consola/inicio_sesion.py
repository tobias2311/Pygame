import json
from colorama import *
from funciones import abrir_menu
from funciones_basicas import limpiar_pantalla 
from funciones_minimas import  ruta_archivo
import time

def iniciar_sesion():
    with open(ruta_archivo, "r") as archivo:
        datos = json.load(archivo)
        
    limpiar_pantalla()
    print(Fore.YELLOW + "Seleccioná una casilla.\n" + Style.RESET_ALL)
    titulo = print(Back.GREEN + f"Usuario  - {'Nombre':<10}|{'Puntaje Maximo':<20}|{'Ultimo Puntaje':<15}|{'Winrate':<20}" + Style.RESET_ALL)
    
    for intervalo in datos:
        user = datos[intervalo]
        nombre = user["nombre"]
        puntaje = user["ultimo_puntaje"]
        puntaje_max = user["puntaje_max"]
        winrate = user["porcentaje_winrate"]
        porcentaje = Fore.CYAN + Back.BLACK + "%" 
        rango = user["rango"]
        barra = Fore.CYAN + "|" + Fore.BLACK
        
        if nombre == "":
            print(Fore.BLACK  + f"{intervalo} - {"disponible":<10}{barra}{puntaje_max:<20}{barra}{puntaje:<15}{barra}{winrate} - {rango} " + Style.RESET_ALL)
        else:
            print(Fore.CYAN + f"{intervalo} - {nombre:<10}|{puntaje_max:<20}|{puntaje:<15}|{winrate}{porcentaje} - {rango} " + Style.RESET_ALL)
    print(Fore.YELLOW + "-" * 80 + Style.RESET_ALL )
    eleccion_jugador = abrir_menu_eleccion(datos)
    respuesta_del_menu(eleccion_jugador, datos)
     
def pedir_contra(nombre, contraseña, datos):
    intentos = 3
    print(Back.RED + "Contraseña (oculta):", contraseña_tachada(contraseña) + Style.RESET_ALL)
    while intentos > 0:
        contraseña_ingresada = input(Fore.BLACK + "CONTRASEÑA: " + Style.RESET_ALL)
        if contraseña_ingresada == contraseña:
            limpiar_pantalla()
            print(Fore.YELLOW + f"¡Bienvenido {nombre}!\n" + Style.RESET_ALL)
            
            with open(ruta_archivo, "w") as archivo:
                json.dump(datos, archivo, indent=4)
                          
            abrir_menu(nombre)
            break
        else:
            intentos -= 1
            print(f"Incorrecta. Te quedan {intentos} intentos.")
    print("Te quedaste sin intentos...")
    iniciar_sesion()

def contraseña_tachada(contraseña):
    return contraseña[0] + "*" * (len(contraseña) - 1)

def abrir_juego():
    with open(ruta_archivo, "r") as archivo:
        datos = json.load(archivo)

    
    while True:
        espacio_disponible = False
        for i in datos:
            user = datos[i]
            if user["nombre"] == "": 
                espacio_disponible = True 
                break 

        print(Fore.BLUE + "A- INICIAR SESION" + Style.RESET_ALL)
        
        if espacio_disponible: 
            print(Fore.BLUE + "B- REGISTRARSE\n" + Style.RESET_ALL)
        else:
            print(Fore.BLACK + "B- REGISTRARSE (no disponible)\n" + Style.RESET_ALL)

        inicio_registro = input("Elección: ").lower()

        match inicio_registro:
            case "a":
                limpiar_pantalla()
                iniciar_sesion()
            case "b":
                if espacio_disponible:
                    limpiar_pantalla()
                    registrarse(datos)
                else:
                    limpiar_pantalla()
                    print(Fore.YELLOW + "No hay espacios disponibles para registrarse!" + Style.RESET_ALL)    
            case _:
                limpiar_pantalla()
                print("¡Elegí una opción válida! (a/b)")

def abrir_menu_eleccion(datos):

    print("seleccionar usuario")
    print("Enter para volver ..\n")

    while True:
        eleccion_jugador = input(Fore.YELLOW + "Escribi el nombre del jugador: " + Style.RESET_ALL).lower()
        if eleccion_jugador == "":
            abrir_juego()
            
        else:
            for intervalo in datos:
                user = datos[intervalo]
                nombre = user["nombre"]
                contraseña = user["contra"]
                
                if eleccion_jugador == nombre:
                    pedir_contra(nombre,contraseña,datos)
                                 
def respuesta_del_menu(eleccion_jugador, datos):
    match eleccion_jugador:
        case "a":
            elegir_usuario(datos)
        case "b":
            registrarse(datos)
        case "c":
            cerrar_juego()

def cerrar_juego():
    limpiar_pantalla()
    exit()

def registrarse(datos):
    limpiar_pantalla()
    print(Fore.YELLOW + "REGISTRO -- \n" + Style.RESET_ALL)

    nombre = input("Escribí tu nombre de usuario: ")
    contraseña = input("Escribí tu contraseña (acordatela): ")
    limpiar_pantalla()
    print(Fore.BLACK + f"Contraseña ingresada: {contraseña_tachada(contraseña)}" + Style.RESET_ALL)
    confirmar_contraseña = input("Confirmar contraseña: ")

    intentos_confirmacion = 0
    while intentos_confirmacion < 3:
        if confirmar_contraseña != contraseña:
            print("La contraseña no coincide..")
            intentos_confirmacion += 1
            print(f"Te quedan {3 - intentos_confirmacion} intentos!")
            confirmar_contraseña = input("Confirmar contraseña: ")
        else:
            crear_usuario(nombre, contraseña, datos)
            return

    print("Demasiados intentos fallidos.")

def crear_usuario(nombre, contraseña, datos):
    for intervalo in datos:
        user = datos[intervalo]
        if user["nombre"] == "":
            user["nombre"] = nombre
            user["contra"] = contraseña
            with open(ruta_archivo, "w") as archivo:
                json.dump(datos, archivo, indent=4)

            limpiar_pantalla()
            print("Usuario creado exitosamente!")
            time.sleep(1)
            iniciar_sesion()
            return

    print("No hay espacios disponibles para nuevos usuarios.")
    iniciar_sesion()

def elegir_usuario(datos):
    while True:
        eleccion_usuario = input("Elegí el usuario (nombre): ").strip()
        for i in datos:
            user = datos[i]
            nombre = user["nombre"]
            contraseña = user["contra"]
            if eleccion_usuario == nombre:
                pedir_contra(nombre, contraseña, datos)
                return
        print("Tenés que escribir un nombre de usuario válido...")

