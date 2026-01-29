from datos_minijuego import generar_matriz_frutas
from funciones_basicas import limpiar_pantalla
import time

def crear_visibles(tam=4):
    matriz = []
    for i in range(tam):
        fila = []
        for j in range(tam):
            fila.append(False)
        matriz.append(fila)
    return matriz

def mostrar_tablero(tablero, visibles, ocultar=True):
    print("   " + "  ".join(str(i) for i in range(4)))
    for i in range(4):
        fila = []
        for j in range(4):
            if visibles[i][j] or not ocultar:
                fila.append(tablero[i][j])
            else:
                fila.append("⬜")
        print(f"{i}  " + " ".join(fila))

def tablero_completo(visibles):  # verifica que se descubrieron todas las frutas
    for fila in visibles:
        if not all(fila):
            return False
    return True

# RECURSIVA
def pedir_coordenada(mensaje, visibles):
    entrada = input(mensaje).strip().lower()
    

    partes = entrada.split()
    if len(partes) != 2:
        print("Formato inválido. Usá: fila columna (ej: 1 2)")
        return pedir_coordenada(mensaje, visibles)
    try:
        fila = int(partes[0])
        col = int(partes[1])
        if fila < 0 or fila >= 4 or col < 0 or col >= 4:
            print("Coordenadas fuera de rango.")
            return pedir_coordenada(mensaje, visibles)
        if visibles[fila][col]:
            print("Ya está descubierta.")
            return pedir_coordenada(mensaje, visibles)
        return fila, col
    except ValueError:
        print("Debés ingresar números.")
        return pedir_coordenada(mensaje, visibles)

# ORDENAMIENTO BURBUJA
def contar_y_ordenar_frutas(tablero):
    frutas = ["🍎", "🍌", "🍓", "🍇"]
    cantidades = [0, 0, 0, 0]

    for i in range(4):
        for j in range(4):
            fruta = tablero[i][j]
            for k in range(len(frutas)):
                if fruta == frutas[k]:
                    cantidades[k] += 1

    # Ordenamiento burbuja (de mayor a menor)
    for i in range(len(cantidades)):
        for j in range(0, len(cantidades) - i - 1):
            if cantidades[j] < cantidades[j + 1]:
                cantidades[j], cantidades[j + 1] = cantidades[j + 1], cantidades[j]
                frutas[j], frutas[j + 1] = frutas[j + 1], frutas[j]

    print("\nFrutas ordenadas por cantidad:")
    for i in range(len(frutas)):
        print(frutas[i], ":", cantidades[i])

def juego_memoria():
    intentos = 1
    puntos = 0

    tablero = generar_matriz_frutas()  # debería generar matriz 4x4 con 8 pares mezclados
    visibles = crear_visibles()

    limpiar_pantalla()

    while intentos > 0:
        mostrar_tablero(tablero, visibles)
        print(f"Puntos: {puntos} | Intentos restantes: {intentos} | Escribí (exit) para salir")

        fila1, col1 = pedir_coordenada("Primera coordenada (fila col): ", visibles)
      
        visibles[fila1][col1] = True

        limpiar_pantalla()
        mostrar_tablero(tablero, visibles)

        fila2, col2 = pedir_coordenada("Segunda coordenada (fila col): ", visibles)
        
        visibles[fila2][col2] = True

        limpiar_pantalla()
        mostrar_tablero(tablero, visibles)

        if tablero[fila1][col1] == tablero[fila2][col2]:
            print("¡Correcto! ✅")
            puntos += 1
        else:
            print("Incorrecto ❌")
            visibles[fila1][col1] = False
            visibles[fila2][col2] = False
            intentos -= 1

        time.sleep(1.5)

        if tablero_completo(visibles):
            print("¡Ganaste! 🎉")
            mostrar_tablero(tablero, visibles, ocultar=False)
            print(f"Puntos totales: {puntos}")
            contar_y_ordenar_frutas(tablero)
            return

        limpiar_pantalla()

    print("Te quedaste sin intentos.")
    print("Este era el tablero:")
    mostrar_tablero(tablero, visibles, ocultar=False)
    print(f"Puntos totales: {puntos}")
    contar_y_ordenar_frutas(tablero)