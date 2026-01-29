import random

def generar_matriz_frutas():
    frutas = ["🍎", "🍌", "🍓", "🍇"]
    
    # Todas las combinaciones posibles de 4 impares positivos que suman 16
    combinaciones_validas = [
        [1, 3, 5, 7],
        [1, 5, 3, 7],
        [3, 1, 7, 5]
        ]

    cantidades = random.choice(combinaciones_validas)
    random.shuffle(cantidades)  # para que no siempre quede la misma fruta con la misma cantidad

    seleccionadas = []
    for i in range(len(frutas)):
        for _ in range(cantidades[i]):
            seleccionadas.append(frutas[i])

    random.shuffle(seleccionadas)

    matriz = []
    for i in range(0, 16, 4):
        matriz.append(seleccionadas[i:i+4])

    return matriz