#ruta_archivo = "Preguntas_y_Respuestas/Archivos/archivos.json"
#ruta_archivo = "Archivos/archivos.json"

import os
from cargar_preguntas import cargar_preguntas_desde_csv
from colorama import *

respuestas = ("a", "b", "c", "d")
# Ruta absoluta al archivo archivos.json en la misma carpeta
ruta_archivo = os.path.join(os.path.dirname(__file__), "archivos.json")

respuestas_correctas = 0
puntaje_acumulado = 0.00   

total_respuestas_correctas = 0
total_puntaje_acumulado = 0
total_de_veces_jugadas = 0
total_aciertos = 0
total_errores = 0
puntaje_max = 0
porcentaje_winrate = 0 
ultimo_puntaje = 0

# LECTURA ---
todas_las_preguntas_del_csv = cargar_preguntas_desde_csv()
preguntas_cultura_general = [
    pregunta for pregunta in todas_las_preguntas_del_csv if pregunta["categoria"] == "Cultura general"
]
preguntas_frases_deportivas = [
    pregunta for pregunta in todas_las_preguntas_del_csv if pregunta["categoria"] == "Frases deportivas"
]
preguntas_frases_populares = [
    pregunta for pregunta in todas_las_preguntas_del_csv if pregunta["categoria"] == "Frases populares"
]
# ---------

enunciados_boss = {
    "dr_insano": {
        "nombre": "Dr.Insano👿",
        "dibujo": Fore.RED + """" 
            \ __________ /      
             · --.  .-- ·
            | (o)/  \(o) |
            |     /\     |        
            \__|IIIIII|__/
             | \IIIIII/ |
             \__________/          
        """ + Style.RESET_ALL, 
        "dibujo_abierto": Fore.RED +""""
            \ __________ /      
             · --.  .-- ·
            | (o)/  \(o) |
            |     /\     |        
            \__|IIIIII|__/
             | |      | |
             | \IIIIII/ |
             \__________/          
        """ + Style.RESET_ALL, 
        "porcentaje": 30,
        "categoria": "Razonamiento matemático",
        "preguntas": [
            {
                "enunciado": "Si Juan tiene el doble de edad que Ana y la suma de sus edades es 36, entonces la edad de Ana es...",
                "opciones": ["10", "12", "14", "18"],
                "respuesta_correcta": "12",
                "puntos": 2
            },
            {
                "enunciado": "Un número más su triple da 48. Ese número es...",
                "opciones": ["12", "16", "18", "24"],
                "respuesta_correcta": "12",
                "puntos": 2
            },
            {
                "enunciado": "Un número multiplicado por 6 da 72. Ese número es...",
                "opciones": ["10", "12", "14", "16"],
                "respuesta_correcta": "12",
                "puntos": 1
            },
            {
                "enunciado": "Si restás 15 a un número y el resultado es 5, ese número es...",
                "opciones": ["10", "15", "20", "25"],
                "respuesta_correcta": "20",
                "puntos": 1
            },
            {
                "enunciado": "Si duplicás un número y le sumás 10, da 34. ¿Cuál es el número?",
                "opciones": ["10", "11", "12", "13"],
                "respuesta_correcta": "12",
                "puntos": 2
            }
        ]
    },
    "jefe_gonza": {
        "nombre": "Profesor Gonza👨‍🎓",
        "dibujo":Fore.GREEN + """"
            ,--.       ,--.
           ((O ))-._.-(( O))
            \__/       \__/
            /   _______   \.
           | _||  __.  ||_ |
           \___\_______/___/        
        """ + Style.RESET_ALL, 
        "dibujo_abierto":Fore.GREEN +""""
            ,--.       ,--.
           ((O ))-._.-(( O))
            \__/       \__/
            /   _______   \.
           | _||       ||_ |
           |   |  ( )  |   |
           \___\_______/___/       
        """+ Style.RESET_ALL, 
        "porcentaje": 35,
        "categoria": "Programacion",
        "preguntas": [
        {
            "enunciado": "¿Que tipo de dato **no permite elementos repetidos**?",
            "opciones": ["list", "tuple", "set", "dict"],
            "respuesta_correcta": "set",
            "puntos": 2
        },
        {
            "enunciado": "¿Qué estructura es **inmutable**?",
            "opciones": ["list", "tuple", "set", "dict"],
            "respuesta_correcta": "tuple",
            "puntos": 2
        },
        {
            "enunciado": "¿Qué palabra clave se usa para **definir una función** en Python?",
            "opciones": ["def", "fun", "function", "lambda"],
            "respuesta_correcta": "def",
            "puntos": 1
        },
        {
            "enunciado": "¿Cuál es el resultado del tipo de dato de `type(True)`?",
            "opciones": ["bool", "str", "int", "list"],
            "respuesta_correcta": "bool",
            "puntos": 2
        },
        {
            "enunciado": "¿Qué letra representa comúnmente a una **variable iteradora** en un bucle `for`?",
            "opciones": ["x", "i", "v", "z"],
            "respuesta_correcta": "i",
            "puntos": 1
        }
        ]
    }
}
