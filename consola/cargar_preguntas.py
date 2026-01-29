from colorama import *

def cargar_preguntas_desde_csv(preguntas="preguntas_juego.csv"):
    preguntas_cargadas = []
 
    with open(preguntas, 'r', encoding='utf-8') as archivo_csv:
        lineas = archivo_csv.readlines()

        encabezados = lineas[0].strip().split(',')

        for linea in lineas[1:]:  
            datos = linea.strip().split(',')

            if len(datos) != len(encabezados):
                continue

            enunciado = datos[encabezados.index('enunciado')].strip()
            opciones = [
                datos[encabezados.index('opcion1')].strip(),
                datos[encabezados.index('opcion2')].strip(),
                datos[encabezados.index('opcion3')].strip(),
                datos[encabezados.index('opcion4')].strip()
            ]
            respuesta_correcta = datos[encabezados.index('respuesta_correcta')].strip()
            categoria = datos[encabezados.index('categoria')].strip()
            puntos = int(datos[encabezados.index('puntos')].strip())

            pregunta_dict = {
                "enunciado": enunciado,
                "opciones": opciones,
                "respuesta_correcta": respuesta_correcta,
                "categoria": categoria,
                "puntos": puntos
            }
            preguntas_cargadas.append(pregunta_dict)

    return preguntas_cargadas
