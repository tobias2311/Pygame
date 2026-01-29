import time
from colorama import *
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear') # Mejorado para compatibilidad con Windows y Linux/macOS
    print(Fore.RED + f"ESTAS JUGANDO.. {Fore.WHITE + Back.RED}🔥💎DESAFIO MENTAL💎🔥\n" + Style.RESET_ALL)

def crear_loading():
    limpiar_pantalla()
    load_text = "LOADING" # Renombrado para claridad
    for i in range(3):
        agregar_puntos_loading(load_text)
        quitar_puntos_loading(load_text)

def agregar_puntos_loading(load_text):
    temp_load = load_text 
    for j in range(3):
        temp_load += "."
        print(Fore.LIGHTMAGENTA_EX + temp_load + Style.RESET_ALL)
        time.sleep(0.08)
        limpiar_pantalla()
                
def quitar_puntos_loading(load_text): 
    temp_load = load_text + "..." 
    for j in range(3):
        temp_load = temp_load[:-1]
        print(Fore.LIGHTMAGENTA_EX + temp_load + Style.RESET_ALL)
        time.sleep(0.2)
        limpiar_pantalla()          

def loading_quieto():
    print(Fore.LIGHTMAGENTA_EX + "\nLOADING..." + Style.RESET_ALL)
    time.sleep(1.5)
    